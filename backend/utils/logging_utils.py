#!/usr/bin/env python3
"""
Logging utilities for the Encrypted Analytics-as-a-Service platform
"""

import time
from typing import Dict, Any, Optional
from functools import wraps

from db.models import LogEntry

def log_operation(operation: str, operation_type: str, client_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
    """
    Log an operation to the database
    
    Args:
        operation: Name of the operation
        operation_type: Type of operation ('computation', 'ml_prediction', 'system')
        client_id: Optional client identifier
        metadata: Optional metadata about the operation
    
    Returns:
        ID of the created log entry
    """
    log_entry = LogEntry(
        operation=operation,
        operation_type=operation_type,
        client_id=client_id,
        metadata=metadata
    )
    
    return log_entry.save()

def log_operation_decorator(operation: str, operation_type: str):
    """
    Decorator to log function execution and measure execution time
    
    Args:
        operation: Name of the operation
        operation_type: Type of operation ('computation', 'ml_prediction', 'system')
    
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract client_id from kwargs if available
            client_id = kwargs.get('client_id')
            
            # Record start time
            start_time = time.time()
            
            try:
                # Execute the function
                result = await func(*args, **kwargs)
                
                # Calculate execution time
                execution_time = time.time() - start_time
                
                # Log successful operation
                log_entry = LogEntry(
                    operation=operation,
                    operation_type=operation_type,
                    status="success",
                    client_id=client_id,
                    metadata={
                        "args": str(args) if args else None,
                        "kwargs": {k: v for k, v in kwargs.items() if k != "client_id"},
                        "result_type": str(type(result))
                    },
                    execution_time=execution_time
                )
                log_entry.save()
                
                return result
                
            except Exception as e:
                # Calculate execution time
                execution_time = time.time() - start_time
                
                # Log failed operation
                log_entry = LogEntry(
                    operation=operation,
                    operation_type=operation_type,
                    status="error",
                    client_id=client_id,
                    metadata={
                        "args": str(args) if args else None,
                        "kwargs": {k: v for k, v in kwargs.items() if k != "client_id"},
                        "error": str(e),
                        "error_type": str(type(e).__name__)
                    },
                    execution_time=execution_time
                )
                log_entry.save()
                
                # Re-raise the exception
                raise
                
        return wrapper
    return decorator

def log_system_event(event_name: str, metadata: Optional[Dict[str, Any]] = None):
    """
    Log a system event
    
    Args:
        event_name: Name of the system event
        metadata: Optional metadata about the event
    
    Returns:
        ID of the created log entry
    """
    log_entry = LogEntry(
        operation=event_name,
        operation_type="system",
        metadata=metadata
    )
    
    return log_entry.save()