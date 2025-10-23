#!/usr/bin/env python3
"""
Unified system startup script for the Encrypted Analytics-as-a-Service
Starts both backend and frontend servers
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_backend():
    """Start the backend server in a separate process"""
    try:
        print("Starting Backend Server...")
        backend_process = subprocess.Popen([
            sys.executable, "start_backend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give backend time to start
        time.sleep(3)
        
        if backend_process.poll() is None:
            print("Backend server started successfully")
            return backend_process
        else:
            stdout, stderr = backend_process.communicate()
            print(f"Backend server failed to start: {stderr}")
            return None
            
    except Exception as e:
        print(f"Failed to start backend server: {e}")
        return None

def start_frontend():
    """Start the frontend server in a separate process"""
    try:
        print("Starting Frontend Server...")
        frontend_process = subprocess.Popen([
            sys.executable, "start_frontend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give frontend time to start
        time.sleep(2)
        
        if frontend_process.poll() is None:
            print("Frontend server started successfully")
            return frontend_process
        else:
            stdout, stderr = frontend_process.communicate()
            print(f"Frontend server failed to start: {stderr}")
            return None
            
    except Exception as e:
        print(f"Failed to start frontend server: {e}")
        return None

def main():
    """Start both backend and frontend servers"""
    print("Starting Encrypted Analytics-as-a-Service System...")
    print("=" * 60)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("Cannot start system without backend server")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("Cannot start system without frontend server")
        backend_process.terminate()
        sys.exit(1)
    
    print("\nSystem started successfully!")
    print("Backend URL: http://localhost:8000")
    print("Frontend URL: http://localhost:3000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop both servers")
    
    try:
        # Wait for both processes
        while True:
            time.sleep(1)
            
            # Check if either process has died
            if backend_process.poll() is not None:
                print("Backend server stopped unexpectedly")
                break
                
            if frontend_process.poll() is not None:
                print("Frontend server stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\nStopping system...")
        
        # Terminate both processes
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("Backend server stopped")
            
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("Frontend server stopped")
            
        print("System stopped successfully")

if __name__ == "__main__":
    main()
