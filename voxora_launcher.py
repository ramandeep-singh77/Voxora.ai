#!/usr/bin/env python3
"""
🤟 Voxora.AI - EXE Launcher
Standalone executable launcher for Voxora.AI
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
import json

class VoxoraLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤟 Voxora.AI Launcher")
        self.root.geometry("500x400")
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
        title_label = ttk.Label(main_frame, text="🤟 Voxora.AI", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Real-time Sign Language Recognition", font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Ready to start")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 10))
        status_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
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
        info_text = tk.Text(main_frame, height=10, width=60, wrap=tk.WORD)
        info_text.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        info_content = """Welcome to Voxora.AI! 🤟

This launcher will start the sign language recognition system.

Requirements:
• Node.js (for React UI) - Download from nodejs.org
• Webcam for sign detection

What happens when you click Start:
1. Starts Flask backend (AI model + API)
2. Starts React frontend (beautiful UI)
3. Opens browser automatically

URLs:
• React UI: http://localhost:3000
• Flask API: http://localhost:5000

Instructions:
1. Click "Start Voxora.AI"
2. Wait for both services to start
3. Browser will open automatically
4. Allow camera access when prompted
5. Start signing! Hold each sign for 1 second

Click "Stop" to close all services.
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
                        except:
                            pass
            except:
                pass
    
    def check_nodejs(self):
        """Check if Node.js is installed"""
        try:
            result = subprocess.run("node --version", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        return False
    
    def start_flask_server(self):
        """Start Flask backend server"""
        try:
            self.update_status("Loading AI model...")
            
            # Get the directory where the EXE is located
            if getattr(sys, 'frozen', False):
                # Running as EXE
                app_dir = os.path.dirname(sys.executable)
            else:
                # Running as script
                app_dir = os.path.dirname(os.path.abspath(__file__))
            
            os.chdir(app_dir)
            
            # Import and start Flask app
            sys.path.insert(0, app_dir)
            from web_app import app, load_model
            
            load_model()
            self.update_status("AI model loaded successfully ✅")
            
            # Start Flask in a separate thread
            def run_flask():
                app.run(debug=False, threaded=True, host='127.0.0.1', port=5000, use_reloader=False)
            
            flask_thread = threading.Thread(target=run_flask, daemon=True)
            flask_thread.start()
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start Flask server:\n{str(e)}")
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
                text=True
            )
            
            # Wait a moment for React to start
            time.sleep(5)
            
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
        
        # Check Node.js
        if not self.check_nodejs():
            messagebox.showerror("Node.js Required", 
                               "Node.js is required to run the React UI.\n\n"
                               "Please download and install Node.js from:\n"
                               "https://nodejs.org\n\n"
                               "Then restart this application.")
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
        
        # Wait for Flask to start
        time.sleep(3)
        
        # Start React UI
        if not self.start_react_ui():
            self.start_button.config(state='normal')
            self.progress.stop()
            return
        
        # Wait for React to start
        time.sleep(5)
        
        # Open browser
        self.open_browser()
        
        # Update UI
        self.progress.stop()
        self.update_status("Voxora.AI is running! 🎉")
        self.stop_button.config(state='normal')
        self.browser_button.config(state='normal')
        
        messagebox.showinfo("Success!", 
                           "Voxora.AI is now running!\n\n"
                           "• React UI: http://localhost:3000\n"
                           "• Flask API: http://localhost:5000\n\n"
                           "The browser should open automatically.\n"
                           "Allow camera access when prompted.")
    
    def stop_application(self):
        """Stop the application"""
        self.update_status("Stopping services...")
        
        # Kill React process
        if self.react_process and self.react_process.poll() is None:
            self.react_process.terminate()
            self.react_process.wait()
        
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
        except Exception as e:
            messagebox.showwarning("Browser", f"Could not open browser automatically.\n\nPlease open: http://localhost:3000")
    
    def run(self):
        """Run the launcher"""
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit Voxora.AI?"):
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