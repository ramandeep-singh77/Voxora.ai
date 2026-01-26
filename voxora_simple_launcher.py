#!/usr/bin/env python3
"""
🤟 Voxora.AI - Simple EXE Launcher
Lightweight launcher that starts the Python scripts
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

class VoxoraLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤟 Voxora.AI Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        self.flask_process = None
        self.react_process = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the launcher UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🤟 Voxora.AI", font=("Arial", 28, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="Real-time Sign Language Recognition", font=("Arial", 14))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 11))
        status_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=500, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Voxora.AI", command=self.start_application, width=20)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop", command=self.stop_application, width=15, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.browser_button = ttk.Button(button_frame, text="🌐 Open Browser", command=self.open_browser, width=15, state='disabled')
        self.browser_button.grid(row=0, column=2, padx=5)
        
        # Info text
        info_text = tk.Text(main_frame, height=12, width=70, wrap=tk.WORD, font=("Arial", 10))
        info_text.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        info_content = """Welcome to Voxora.AI! 🤟

This launcher will start the sign language recognition system.

REQUIREMENTS:
• Python 3.8+ with required packages (tensorflow, opencv, flask, etc.)
• Node.js 16+ (for React UI) - Download from nodejs.org
• Webcam for sign detection

WHAT HAPPENS WHEN YOU CLICK START:
1. Checks if Python and Node.js are available
2. Kills any conflicting processes on ports 3000/5000
3. Starts Flask backend (AI model + API) 
4. Starts React frontend (beautiful UI)
5. Opens browser automatically

URLs:
• React UI: http://localhost:3000
• Flask API: http://localhost:5000

INSTRUCTIONS:
1. Click "🚀 Start Voxora.AI"
2. Wait for both services to start (may take 30-60 seconds)
3. Browser will open automatically to http://localhost:3000
4. Allow camera access when prompted
5. Start signing! Hold each sign for 1 second

TROUBLESHOOTING:
• If Python packages are missing, run: pip install -r requirements.txt
• If Node.js is missing, download from: https://nodejs.org
• If ports are busy, the launcher will automatically kill conflicting processes

Click "⏹️ Stop" to close all services when done.
"""
        
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        self.root.update()
        
    def kill_port_processes(self):
        """Kill any processes using our ports"""
        ports = [3000, 5000]
        killed_any = False
        for port in ports:
            try:
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
                            killed_any = True
                        except:
                            pass
            except:
                pass
        
        if killed_any:
            self.update_status("Cleaned up conflicting processes ✅")
            time.sleep(1)
    
    def check_python(self):
        """Check if Python is available"""
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        return False
    
    def check_nodejs(self):
        """Check if Node.js is installed"""
        try:
            result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        return False
    
    def check_python_packages(self):
        """Check if required Python packages are available"""
        required_packages = ['flask', 'cv2', 'tensorflow', 'numpy', 'mediapipe']
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
    
    def start_flask_server(self):
        """Start Flask backend server"""
        try:
            self.update_status("Starting Flask backend (loading AI model)...")
            
            # Get the directory where the launcher is located
            if getattr(sys, 'frozen', False):
                # Running as EXE
                app_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Start Flask using the start_simple.py script
            self.flask_process = subprocess.Popen(
                [sys.executable, "web_app.py"],
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Wait for Flask to start
            time.sleep(8)
            
            if self.flask_process.poll() is None:
                self.update_status("Flask backend started successfully ✅")
                return True
            else:
                stdout, stderr = self.flask_process.communicate()
                messagebox.showerror("Error", f"Flask backend failed to start:\n{stderr}")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Flask backend:\n{str(e)}")
            return False
    
    def start_react_ui(self):
        """Start React frontend"""
        try:
            react_dir = Path("ASL-Hand-sign-language-translator--main")
            
            if not react_dir.exists():
                messagebox.showerror("Error", f"React UI directory not found: {react_dir}")
                return False
            
            self.update_status("Starting React UI...")
            
            # Start React dev server
            self.react_process = subprocess.Popen(
                "npm run dev",
                shell=True,
                cwd=react_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
            # Wait for React to start
            time.sleep(8)
            
            if self.react_process.poll() is None:
                self.update_status("React UI started successfully ✅")
                return True
            else:
                stdout, stderr = self.react_process.communicate()
                messagebox.showerror("Error", f"React UI failed to start:\n{stderr}")
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start React UI:\n{str(e)}")
            return False
    
    def start_application(self):
        """Start the complete application"""
        # Disable start button
        self.start_button.config(state='disabled')
        self.progress.start()
        
        # Check Python
        if not self.check_python():
            messagebox.showerror("Python Required", 
                               "Python is required to run Voxora.AI.\n\n"
                               "Please install Python 3.8+ from:\n"
                               "https://python.org")
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        # Check Python packages
        missing_packages = self.check_python_packages()
        if missing_packages:
            messagebox.showerror("Python Packages Missing", 
                               f"Required Python packages are missing:\n{', '.join(missing_packages)}\n\n"
                               "Please run:\n"
                               "pip install -r requirements.txt")
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        # Check Node.js
        if not self.check_nodejs():
            messagebox.showerror("Node.js Required", 
                               "Node.js is required to run the React UI.\n\n"
                               "Please download and install Node.js from:\n"
                               "https://nodejs.org")
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        self.update_status("Cleaning up existing processes...")
        self.kill_port_processes()
        
        # Start Flask server
        if not self.start_flask_server():
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        # Start React UI
        if not self.start_react_ui():
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        # Wait a moment for everything to stabilize
        time.sleep(3)
        
        # Open browser
        self.open_browser()
        
        # Update UI
        self.progress.stop()
        self.update_status("🎉 Voxora.AI is running! Ready to recognize signs!")
        self.stop_button.config(state='normal')
        self.browser_button.config(state='normal')
        
        messagebox.showinfo("Success!", 
                           "🎉 Voxora.AI is now running!\n\n"
                           "• React UI: http://localhost:3000\n"
                           "• Flask API: http://localhost:5000\n\n"
                           "The browser should open automatically.\n"
                           "Allow camera access when prompted and start signing! 🤟")
    
    def stop_application(self):
        """Stop the application"""
        self.update_status("Stopping services...")
        
        # Kill React process
        if self.react_process and self.react_process.poll() is None:
            self.react_process.terminate()
            try:
                self.react_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.react_process.kill()
        
        # Kill Flask process
        if self.flask_process and self.flask_process.poll() is None:
            self.flask_process.terminate()
            try:
                self.flask_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.flask_process.kill()
        
        # Kill port processes
        self.kill_port_processes()
        
        # Update UI
        self.update_status("Stopped ⏹️")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.browser_button.config(state='disabled')
    
    def open_browser(self):
        """Open browser to the application"""
        try:
            webbrowser.open("http://localhost:3000")
            self.update_status("Browser opened to http://localhost:3000 🌐")
        except Exception as e:
            messagebox.showwarning("Browser", f"Could not open browser automatically.\n\nPlease open: http://localhost:3000")
    
    def run(self):
        """Run the launcher"""
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Voxora.AI?\n\nThis will stop all running services."):
            self.stop_application()
            self.root.destroy()

def main():
    """Main function"""
    try:
        launcher = VoxoraLauncher()
        launcher.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start Voxora.AI Launcher:\n{str(e)}")

if __name__ == "__main__":
    main()