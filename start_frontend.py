#!/usr/bin/env python3
"""
Unified frontend startup script for the Encrypted Analytics-as-a-Service
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def main():
    """Start the frontend server"""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent
        frontend_dir = project_root / "frontend"
        
        # Verify frontend directory exists
        if not frontend_dir.exists():
            print(f"❌ Frontend directory not found: {frontend_dir}")
            sys.exit(1)
        
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Set up the server
        PORT = 3000
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("Starting Frontend Server...")
            print(f"Frontend URL: http://localhost:{PORT}")
            print(f"Serving files from: {frontend_dir.absolute()}")
            print("Press Ctrl+C to stop")
            
            # Open browser automatically
            webbrowser.open(f"http://localhost:{PORT}")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nFrontend server stopped by user")
    except Exception as e:
        print(f"Failed to start frontend server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()