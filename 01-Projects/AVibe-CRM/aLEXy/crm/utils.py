import logging
from datetime import datetime
from flask import request, g
import json

logger = logging.getLogger(__name__)

def setup_logging():
    # Configure logging handler
    handler = logging.FileHandler('crm_audit.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def log_request():
    """Middleware to log all requests"""
    g.start_time = datetime.utcnow()
    
    # Log request
    user_id = None
    if hasattr(g, 'jwt_identity'):
        user_id = g.jwt_identity
    
    logger.info(
        f"REQUEST | {request.method} {request.path} | IP: {request.remote_addr} | User: {user_id}"
    )

def log_response(response):
    """Log response details"""
    if hasattr(g, 'start_time'):
        duration = (datetime.utcnow() - g.start_time).total_seconds()
    else:
        duration = 0
    
    logger.info(
        f"RESPONSE | {response.status_code} | {request.method} {request.path} | Duration: {duration:.3f}s"
    )
    return response

def standardize_error_response(error_msg, error_code="UNKNOWN_ERROR", field=None, status_code=400):
    """Return standardized error response"""
    return {
        "error": error_msg,
        "code": error_code,
        "field": field,
        "timestamp": datetime.utcnow().isoformat()
    }, status_code
