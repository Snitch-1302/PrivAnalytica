#!/usr/bin/env python3
"""
Routes for log management and report generation
"""

from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Dict, Any, Optional
import os
import csv
import json
from datetime import datetime
import time

from db.models import get_logs, get_logs_by_operation, get_operation_stats

# Create router
router = APIRouter(prefix="/logs", tags=["logs"])

# Directory for storing generated reports
REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Get all logs with pagination
    
    Args:
        limit: Maximum number of logs to retrieve (1-1000)
        offset: Offset for pagination
        
    Returns:
        List of log entries
    """
    return get_logs(limit=limit, offset=offset)

@router.get("/operation/{operation}", response_model=List[Dict[str, Any]])
async def get_operation_logs(
    operation: str,
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get logs for a specific operation
    
    Args:
        operation: Operation name to filter by
        limit: Maximum number of logs to retrieve (1-1000)
        
    Returns:
        List of log entries for the specified operation
    """
    return get_logs_by_operation(operation=operation, limit=limit)

@router.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """
    Get statistics about operations
    
    Returns:
        Dictionary with operation statistics
    """
    return get_operation_stats()

def generate_csv_report(logs: List[Dict[str, Any]], filename: str):
    """
    Generate CSV report from logs
    
    Args:
        logs: List of log entries
        filename: Output filename
    """
    filepath = os.path.join(REPORTS_DIR, filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        # Define CSV headers
        fieldnames = ['id', 'timestamp', 'operation', 'operation_type', 
                     'client_id', 'status', 'execution_time']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for log in logs:
            # Create a copy of the log without metadata for CSV
            log_copy = {k: v for k, v in log.items() if k != 'metadata'}
            writer.writerow(log_copy)

@router.get("/report/csv")
async def generate_report(
    background_tasks: BackgroundTasks,
    limit: int = Query(1000, ge=1, le=10000),
    operation: Optional[str] = None,
):
    """
    Generate CSV report of logs
    
    Args:
        background_tasks: FastAPI background tasks
        limit: Maximum number of logs to include
        operation: Optional operation to filter by
        
    Returns:
        JSON response with report details
    """
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs_report_{timestamp}.csv"
    
    # Get logs
    if operation:
        logs = get_logs_by_operation(operation=operation, limit=limit)
        filename = f"logs_{operation}_{timestamp}.csv"
    else:
        logs = get_logs(limit=limit)
    
    # Generate report in background
    background_tasks.add_task(generate_csv_report, logs, filename)
    
    return JSONResponse({
        "message": "Report generation started",
        "filename": filename,
        "logs_count": len(logs),
        "download_url": f"/logs/report/download/{filename}"
    })

@router.get("/report/download/{filename}")
async def download_report(filename: str):
    """
    Download a generated report
    
    Args:
        filename: Report filename
        
    Returns:
        File download response
    """
    filepath = os.path.join(REPORTS_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/csv"
    )

@router.get("/report/list", response_model=List[Dict[str, Any]])
async def list_reports():
    """
    List all generated reports
    
    Returns:
        List of report details
    """
    reports = []
    
    for filename in os.listdir(REPORTS_DIR):
        if filename.endswith(".csv"):
            filepath = os.path.join(REPORTS_DIR, filename)
            stats = os.stat(filepath)
            
            reports.append({
                "filename": filename,
                "size_bytes": stats.st_size,
                "created_at": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                "download_url": f"/logs/report/download/{filename}"
            })
    
    # Sort by creation time (newest first)
    reports.sort(key=lambda x: x["created_at"], reverse=True)
    
    return reports