#!/usr/bin/env python3
"""
Unified backend startup script for the Encrypted Analytics-as-a-Service
Handles all import and path issues properly
"""

import sys
import os
import logging
from pathlib import Path

def main():
    """Start the backend server with proper path handling"""
    try:
        print("Starting Encrypted Analytics-as-a-Service Backend...")
        
        # Get the project root directory
        project_root = Path(__file__).parent
        backend_dir = project_root / "backend"
        
        # Verify backend directory exists
        if not backend_dir.exists():
            print(f"❌ Backend directory not found: {backend_dir}")
            sys.exit(1)
        
        # Add backend directory to Python path
        if str(backend_dir) not in sys.path:
            sys.path.insert(0, str(backend_dir))
        
        # Change to backend directory
        os.chdir(backend_dir)
        
        # Create logs directory if it doesn't exist
        logs_dir = backend_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/startup.log'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        
        logger.info("Backend server starting...")
        
        # Import and run the FastAPI app
        import uvicorn
        
        # Import main after changing directory
        try:
            from backend.main import app
        except ImportError as e:
            print(f"Failed to import main: {e}")
            print("Make sure you're running this script from the project root directory")
            sys.exit(1)
        
        print("Backend server starting on http://0.0.0.0:8000")
        print("API documentation available at http://0.0.0.0:8000/docs")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
            log_level="info",
            reload=False
        )
        
    except KeyboardInterrupt:
        print("\nBackend server stopped by user")
    except Exception as e:
        print(f"Failed to start backend server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()