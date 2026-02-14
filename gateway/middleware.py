# gateway/middleware.py
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gateway_requests.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("gateway")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = f"{time.time()}"
        
        # Log request details
        logger.info(f"Request ID: {request_id}")
        logger.info(f"Request Method: {request.method}")
        logger.info(f"Request URL: {request.url}")
        logger.info(f"Client IP: {request.client.host if request.client else 'Unknown'}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Record start time
        start_time = time.time()
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response details
            logger.info(f"Request ID: {request_id}")
            logger.info(f"Response Status: {response.status_code}")
            logger.info(f"Process Time: {process_time:.4f}s")
            logger.info("-" * 80)
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log errors
            process_time = time.time() - start_time
            logger.error(f"Request ID: {request_id}")
            logger.error(f"Error: {str(e)}")
            logger.error(f"Process Time: {process_time:.4f}s")
            logger.error("-" * 80)
            raise
