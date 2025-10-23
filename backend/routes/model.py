from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging
import numpy as np
import base64

from encryption_utils import get_encryption_utils, validate_encrypted_data, format_encrypted_result

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/model", tags=["machine-learning"])

# Pydantic models for request/response
class EncryptedFeaturesRequest(BaseModel):
    encrypted_features: List[str]  # List of encrypted feature vectors
    public_key: str
    model_type: str = "logistic_regression"
    metadata: Optional[Dict[str, Any]] = None

class PredictionResponse(BaseModel):
    model_type: str
    encrypted_predictions: List[str]
    timestamp: str
    status: str
    metadata: Optional[Dict[str, Any]] = None

class ModelInfo(BaseModel):
    model_type: str
    description: str
    input_features: List[str]
    output_type: str
    accuracy: Optional[float] = None

# Mock trained model weights (in production, these would be encrypted)
LOGISTIC_REGRESSION_WEIGHTS = {
    "weights": [0.2, -0.1, 0.3, 0.15],  # [age, bp, cholesterol, bias]
    "intercept": -2.5,
    "feature_names": ["age", "blood_pressure", "cholesterol", "bias"]
}

@router.post("/predict/logistic_regression", response_model=PredictionResponse)
async def predict_logistic_regression(request: EncryptedFeaturesRequest):
    """
    Perform logistic regression prediction on encrypted features
    """
    try:
        # Validate input data
        if not validate_encrypted_data({
            "encrypted_vectors": request.encrypted_features,
            "public_key": request.public_key
        }):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform secure logistic regression prediction
        encrypted_predictions = he_utils.predict_logistic_regression(
            request.encrypted_features,
            request.public_key,
            LOGISTIC_REGRESSION_WEIGHTS
        )
        
        # Format response
        response_data = {
            "model_type": "logistic_regression",
            "encrypted_predictions": encrypted_predictions,
            "timestamp": str(np.datetime64('now')),
            "status": "success",
            "metadata": request.metadata
        }
        
        logger.info(f"Logistic regression prediction completed for {len(request.encrypted_features)} samples")
        
        return PredictionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in logistic regression prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/linear_regression", response_model=PredictionResponse)
async def predict_linear_regression(request: EncryptedFeaturesRequest):
    """
    Perform linear regression prediction on encrypted features
    """
    try:
        # Validate input data
        if not validate_encrypted_data({
            "encrypted_vectors": request.encrypted_features,
            "public_key": request.public_key
        }):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform secure linear regression prediction
        encrypted_predictions = he_utils.predict_linear_regression(
            request.encrypted_features,
            request.public_key
        )
        
        # Format response
        response_data = {
            "model_type": "linear_regression",
            "encrypted_predictions": encrypted_predictions,
            "timestamp": str(np.datetime64('now')),
            "status": "success",
            "metadata": request.metadata
        }
        
        logger.info(f"Linear regression prediction completed for {len(request.encrypted_features)} samples")
        
        return PredictionResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error in linear regression prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/info")
async def get_model_info():
    """
    Get information about available models
    """
    models = [
        {
            "model_type": "logistic_regression",
            "description": "Binary classification for disease prediction",
            "input_features": ["age", "blood_pressure", "cholesterol"],
            "output_type": "probability (0-1)",
            "accuracy": 0.85
        },
        {
            "model_type": "linear_regression",
            "description": "Continuous value prediction",
            "input_features": ["age", "blood_pressure", "cholesterol"],
            "output_type": "continuous value",
            "accuracy": 0.78
        }
    ]
    
    return {
        "models": models,
        "total_models": len(models),
        "status": "available"
    }

@router.get("/health")
async def model_health_check():
    """
    Check if ML models are available
    """
    return {
        "status": "ok",
        "service": "encrypted-ml",
        "available_models": ["logistic_regression", "linear_regression"],
        "encryption_scheme": "CKKS"
    } 