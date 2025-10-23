from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import json
import logging
from typing import List, Dict, Any
import numpy as np
from datetime import datetime

# Import routes
from routes.compute import router as compute_router
from routes.model import router as model_router
from routes.logs import router as logs_router

# Configure logging
import os
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Encrypted Analytics-as-a-Service",
    description="Privacy-Preserving Data Analysis Platform using Homomorphic Encryption & Secure ML",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(compute_router)
app.include_router(model_router)
app.include_router(logs_router)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "ok", "service": "encrypted-analytics", "timestamp": datetime.now().isoformat()}

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "message": "Encrypted Analytics-as-a-Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "compute": "/compute/{operation}",
            "upload": "/upload"
        }
    }

@app.post("/upload")
async def upload_encrypted_data(file: UploadFile = File(...)):
    """Upload encrypted data file"""
    try:
        content = await file.read()
        # For now, we'll just acknowledge the upload
        # In a real implementation, you'd validate and store the encrypted data
        return {
            "message": "Encrypted data uploaded successfully",
            "filename": file.filename,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
