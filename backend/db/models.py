#!/usr/bin/env python3
"""
Database models for Encrypted Analytics-as-a-Service
Handles logging and audit trail functionality
"""

import sqlite3
import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "logs.db")

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db_connection():
    """
    Get SQLite database connection
    
    Returns:
        SQLite connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """
    Initialize database tables if they don't exist
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        operation TEXT NOT NULL,
        operation_type TEXT NOT NULL,
        client_id TEXT,
        metadata TEXT,
        status TEXT NOT NULL,
        execution_time REAL
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_PATH}")

class LogEntry:
    """
    Log entry model for tracking operations
    """
    def __init__(
        self,
        operation: str,
        operation_type: str,
        status: str = "success",
        client_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        execution_time: Optional[float] = None
    ):
        self.timestamp = datetime.now().isoformat()
        self.operation = operation
        self.operation_type = operation_type  # 'computation', 'ml_prediction', 'system'
        self.client_id = client_id
        self.metadata = json.dumps(metadata) if metadata else None
        self.status = status
        self.execution_time = execution_time
    
    def save(self) -> int:
        """
        Save log entry to database
        
        Returns:
            ID of the inserted log entry
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO logs (timestamp, operation, operation_type, client_id, metadata, status, execution_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.timestamp,
            self.operation,
            self.operation_type,
            self.client_id,
            self.metadata,
            self.status,
            self.execution_time
        ))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return log_id

def get_logs(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Get logs from database
    
    Args:
        limit: Maximum number of logs to retrieve
        offset: Offset for pagination
        
    Returns:
        List of log entries as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM logs
    ORDER BY timestamp DESC
    LIMIT ? OFFSET ?
    ''', (limit, offset))
    
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse metadata JSON
    for log in logs:
        if log['metadata']:
            try:
                log['metadata'] = json.loads(log['metadata'])
            except json.JSONDecodeError:
                log['metadata'] = {}
    
    return logs

def get_logs_by_operation(operation: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Get logs for a specific operation
    
    Args:
        operation: Operation name to filter by
        limit: Maximum number of logs to retrieve
        
    Returns:
        List of log entries as dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM logs
    WHERE operation = ?
    ORDER BY timestamp DESC
    LIMIT ?
    ''', (operation, limit))
    
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Parse metadata JSON
    for log in logs:
        if log['metadata']:
            try:
                log['metadata'] = json.loads(log['metadata'])
            except json.JSONDecodeError:
                log['metadata'] = {}
    
    return logs

def get_operation_stats() -> Dict[str, Any]:
    """
    Get statistics about operations
    
    Returns:
        Dictionary with operation statistics
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get operation counts
    cursor.execute('''
    SELECT operation, COUNT(*) as count
    FROM logs
    GROUP BY operation
    ORDER BY count DESC
    ''')
    
    operation_counts = {row['operation']: row['count'] for row in cursor.fetchall()}
    
    # Get operation type counts
    cursor.execute('''
    SELECT operation_type, COUNT(*) as count
    FROM logs
    GROUP BY operation_type
    ORDER BY count DESC
    ''')
    
    operation_type_counts = {row['operation_type']: row['count'] for row in cursor.fetchall()}
    
    # Get average execution times
    cursor.execute('''
    SELECT operation, AVG(execution_time) as avg_time
    FROM logs
    WHERE execution_time IS NOT NULL
    GROUP BY operation
    ''')
    
    avg_execution_times = {row['operation']: row['avg_time'] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        "operation_counts": operation_counts,
        "operation_type_counts": operation_type_counts,
        "avg_execution_times": avg_execution_times,
        "total_logs": sum(operation_counts.values())
    }

# Initialize database when module is imported
init_db()