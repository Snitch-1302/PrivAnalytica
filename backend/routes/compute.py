from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging

from encryption_utils import get_encryption_utils, validate_encrypted_data, format_encrypted_result

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/compute", tags=["computation"])

# Pydantic models for request/response
class EncryptedDataRequest(BaseModel):
    encrypted_vectors: List[str]
    public_key: str
    metadata: Optional[Dict[str, Any]] = None

class ComputationResponse(BaseModel):
    operation: str
    encrypted_result: str
    timestamp: str
    status: str
    metadata: Optional[Dict[str, Any]] = None

@router.post("/average", response_model=ComputationResponse)
async def compute_average(request: EncryptedDataRequest):
    """
    Compute the average of encrypted vectors using homomorphic encryption
    """
    try:
        # Validate input data
        if not validate_encrypted_data(request.dict()):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform homomorphic average computation
        encrypted_result = he_utils.compute_average(
            request.encrypted_vectors,
            request.public_key
        )
        
        # Format response
        response_data = format_encrypted_result(encrypted_result, "average")
        response_data["metadata"] = request.metadata
        
        logger.info(f"Average computation completed for {len(request.encrypted_vectors)} vectors")
        
        return ComputationResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error computing average: {e}")
        raise HTTPException(status_code=500, detail=f"Computation failed: {str(e)}")

@router.post("/sum", response_model=ComputationResponse)
async def compute_sum(request: EncryptedDataRequest):
    """
    Compute the sum of encrypted vectors using homomorphic encryption
    """
    try:
        # Validate input data
        if not validate_encrypted_data(request.dict()):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform homomorphic sum computation
        encrypted_result = he_utils.compute_sum(
            request.encrypted_vectors,
            request.public_key
        )
        
        # Format response
        response_data = format_encrypted_result(encrypted_result, "sum")
        response_data["metadata"] = request.metadata
        
        logger.info(f"Sum computation completed for {len(request.encrypted_vectors)} vectors")
        
        return ComputationResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error computing sum: {e}")
        raise HTTPException(status_code=500, detail=f"Computation failed: {str(e)}")

@router.post("/variance", response_model=ComputationResponse)
async def compute_variance(request: EncryptedDataRequest):
    """
    Compute the variance of encrypted vectors using homomorphic encryption
    """
    try:
        # Validate input data
        if not validate_encrypted_data(request.dict()):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform homomorphic variance computation
        encrypted_result = he_utils.compute_variance(
            request.encrypted_vectors,
            request.public_key
        )
        
        # Format response
        response_data = format_encrypted_result(encrypted_result, "variance")
        response_data["metadata"] = request.metadata
        
        logger.info(f"Variance computation completed for {len(request.encrypted_vectors)} vectors")
        
        return ComputationResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error computing variance: {e}")
        raise HTTPException(status_code=500, detail=f"Computation failed: {str(e)}")

@router.post("/count", response_model=ComputationResponse)
async def compute_count(request: EncryptedDataRequest):
    """
    Count the number of encrypted vectors
    """
    try:
        # Validate input data
        if not validate_encrypted_data(request.dict()):
            raise HTTPException(status_code=400, detail="Invalid encrypted data format")
        
        # Get encryption utilities
        he_utils = get_encryption_utils()
        
        # Perform count computation
        encrypted_result = he_utils.compute_count(request.encrypted_vectors)
        
        # Format response
        response_data = format_encrypted_result(encrypted_result, "count")
        response_data["metadata"] = request.metadata
        
        logger.info(f"Count computation completed for {len(request.encrypted_vectors)} vectors")
        
        return ComputationResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Error computing count: {e}")
        raise HTTPException(status_code=500, detail=f"Computation failed: {str(e)}")

@router.get("/operations")
async def get_available_operations():
    """
    Get list of available computation operations
    """
    operations = [
        {
            "name": "average",
            "description": "Calculate the mean of encrypted values",
            "endpoint": "/compute/average",
            "method": "POST",
            "input": "List of encrypted vectors + public key",
            "output": "Encrypted average"
        },
        {
            "name": "sum",
            "description": "Calculate the sum of encrypted values",
            "endpoint": "/compute/sum",
            "method": "POST",
            "input": "List of encrypted vectors + public key",
            "output": "Encrypted sum"
        },
        {
            "name": "variance",
            "description": "Calculate the variance of encrypted values",
            "endpoint": "/compute/variance",
            "method": "POST",
            "input": "List of encrypted vectors + public key",
            "output": "Encrypted variance"
        },
        {
            "name": "count",
            "description": "Count the number of encrypted values",
            "endpoint": "/compute/count",
            "method": "POST",
            "input": "List of encrypted vectors + public key",
            "output": "Encrypted count"
        }
    ]
    
    return {
        "operations": operations,
        "total_operations": len(operations),
        "status": "available"
    } 