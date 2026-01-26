#!/usr/bin/env python3
"""
🤟 Voxora.AI - Bulletproof One-Click Launcher
Handles all edge cases and provides clear feedback
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import signal
from pathlib import Path

# Global variables for process management
flask_process = None
react_process = None

def kill_port_processes():
    """Kill any processes using our ports"""
    ports = [3000, 5000]
    for port in ports:
        try:
            # Find processes using the port
            result = subprocess.run(f'netstat -ano | findstr :{port}', 
                                  shell=True, capture_output=True, text=True)
            if result.stdout:
                lines = result.stdout.strip().split('\n')
                pids = set()
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5 and 'LISTENING' in line:
                        pid = parts[-1]
                        if pid.isdigit():
                            pids.add(pid)
                
                for pid in pids:
                    try:
                        subprocess.run(f'taskkill /PID {pid} /F', 
                                     shell=True, capture_output=True)
                        print(f"✅ Killed process {pid} using port {port}")
                    except:
                        pass
        except:
            pass

def check_python_packages():
    """Check if Python packages are installed"""
    required_packages = ['flask', 'flask_cors', 'cv2', 'tensorflow', 'numpy', 'mediapipe', 'openai']
    missing = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def install_python_dependencies():
    """Install Python dependencies with better error handling"""
    print("📦 Installing Python dependencies...")
    
    missing = check_python_packages()
    if not missing:
        print("✅ All Python packages already installed")
        return True
    
    print(f"📦 Installing missing packages: {', '.join(missing)}")
    
    try:
        # Use pip install with specific packages for better success rate
        cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        subprocess.run(cmd, check=True, capture_output=True)
        
        cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--no-cache-dir"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ Python dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies:")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        print(f"\n🔧 Manual fix:")
        print(f"   pip install -r requirements.txt")
        return False

def install_node_dependencies():
    """Install Node.js dependencies"""
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    node_modules = react_dir / "node_modules"
    
    if node_modules.exists() and len(list(node_modules.iterdir())) > 10:
        print("✅ Node.js dependencies already installed")
        return True
    
    print("📦 Installing Node.js dependencies...")
    
    if not react_dir.exists():
        print(f"❌ React directory not found: {react_dir}")
        return False
    
    try:
        # Check if npm is available
        subprocess.run("npm --version", shell=True, check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js from https://nodejs.org")
        return False
    
    try:
        # Change to React directory
        original_dir = os.getcwd()
        os.chdir(react_dir)
        
        # Install dependencies
        result = subprocess.run("npm install", shell=True, check=True, capture_output=True, text=True)
        
        # Change back
        os.chdir(original_dir)
        
        print("✅ Node.js dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies:")
        print(f"   Error: {e.stderr}")
        print(f"\n🔧 Manual fix:")
        print(f"   cd {react_dir}")
        print(f"   npm install")
        return False
    finally:
        # Ensure we're back in the original directory
        try:
            os.chdir(original_dir)
        except:
            pass

def start_flask_server():
    """Start Flask backend server"""
    global flask_process
    print("🚀 Starting Flask backend on http://localhost:5000...")
    
    try:
        # Import here to avoid issues if dependencies aren't installed
        sys.path.insert(0, os.getcwd())
        from web_app import app, load_model
        
        # Load model first
        load_model()
        print("✅ AI model loaded successfully")
        
        # Start Flask app
        app.run(debug=False, threaded=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Flask server error: {e}")
        import traceback
        traceback.print_exc()

def start_react_ui():
    """Start React frontend"""
    global react_process
    print("🎨 Starting React UI on http://localhost:3000...")
    
    react_dir = Path("ASL-Hand-sign-language-translator--main")
    
    try:
        # Change to React directory and start dev server
        original_dir = os.getcwd()
        os.chdir(react_dir)
        
        # Start React dev server using shell=True for Windows compatibility
        react_process = subprocess.Popen(
            "npm run dev",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Change back to original directory
        os.chdir(original_dir)
        
        # Wait for React to start
        time.sleep(8)
        
        if react_process.poll() is None:
            print("✅ React UI started successfully")
            
            # Wait for the process to finish or be interrupted
            try:
                react_process.wait()
            except KeyboardInterrupt:
                print("\n⏹️  Stopping React UI...")
                react_process.terminate()
                react_process.wait()
        else:
            stdout, stderr = react_process.communicate()
            print(f"❌ React UI failed to start:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            
    except Exception as e:
        print(f"❌ React UI error: {e}")
        import traceback
        traceback.print_exc()

def cleanup():
    """Cleanup processes on exit"""
    global flask_process, react_process
    
    if react_process and react_process.poll() is None:
        react_process.terminate()
        react_process.wait()
    
    # Kill any remaining processes on our ports
    kill_port_processes()

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n⏹️  Shutting down Voxora.AI...")
    cleanup()
    sys.exit(0)

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "web_app.py",
        "hand_detector.py", 
        "models/signity_model.h5",
        "requirements.txt",
        "ASL-Hand-sign-language-translator--main/package.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n🔧 Make sure you downloaded the complete project from GitHub")
        return False
    
    return True

def main():
    """Main launcher function"""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print("\n" + "="*60)
    print("  🤟 VOXORA.AI - ONE-CLICK LAUNCHER")
    print("="*60)
    
    # Kill any existing processes on our ports
    print("🧹 Cleaning up any existing processes...")
    kill_port_processes()
    
    # Check requirements
    print("🔍 Checking required files...")
    if not check_requirements():
        input("\nPress Enter to exit...")
        return False
    
    print("✅ All required files found")
    
    # Install dependencies
    print("\n📦 Setting up dependencies...")
    
    if not install_python_dependencies():
        input("\nPress Enter to exit...")
        return False
    
    if not install_node_dependencies():
        input("\nPress Enter to exit...")
        return False
    
    print("\n🚀 Starting Voxora.AI...")
    print("   Flask API: http://localhost:5000")
    print("   React UI:  http://localhost:3000")
    print("\n⚠️  Keep this window open while using the app")
    print("   Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Start Flask server in background thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask server to start...")
    time.sleep(5)
    
    # Open browser
    try:
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:3000")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("   Please open http://localhost:3000 manually")
    
    # Start React UI (this will block until stopped)
    try:
        start_react_ui()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)