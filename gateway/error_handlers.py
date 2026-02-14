# gateway/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger("gateway")

# Custom exception classes
class ServiceUnavailableError(Exception):
    """Raised when a microservice is unavailable"""
    def __init__(self, service_name: str, detail: str):
        self.service_name = service_name
        self.detail = detail
        super().__init__(f"Service {service_name} unavailable: {detail}")

class ServiceError(Exception):
    """Raised when a microservice returns an error"""
    def __init__(self, service_name: str, status_code: int, detail: str):
        self.service_name = service_name
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Service {service_name} error: {detail}")

# Exception handlers
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions with detailed error messages"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    logger.error(f"Request: {request.method} {request.url}")
    
    error_responses = {
        400: "Bad Request",
        401: "Unauthorized - Invalid or missing authentication",
        403: "Forbidden - You don't have permission to access this resource",
        404: "Not Found - The requested resource does not exist",
        405: "Method Not Allowed",
        422: "Unprocessable Entity - Invalid request data",
        500: "Internal Server Error",
        503: "Service Unavailable"
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_responses.get(exc.status_code, "Error"),
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url),
            "method": request.method
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed field information"""
    logger.error(f"Validation Error: {exc.errors()}")
    logger.error(f"Request: {request.method} {request.url}")
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": "Invalid request data",
            "status_code": 422,
            "path": str(request.url),
            "method": request.method,
            "validation_errors": errors
        }
    )

async def service_unavailable_handler(request: Request, exc: ServiceUnavailableError):
    """Handle service unavailable errors"""
    logger.error(f"Service Unavailable: {exc.service_name} - {exc.detail}")
    logger.error(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service Unavailable",
            "detail": f"The {exc.service_name} service is currently unavailable",
            "status_code": 503,
            "path": str(request.url),
            "method": request.method,
            "service": exc.service_name,
            "technical_detail": exc.detail
        }
    )

async def service_error_handler(request: Request, exc: ServiceError):
    """Handle service errors"""
    logger.error(f"Service Error: {exc.service_name} - {exc.status_code} - {exc.detail}")
    logger.error(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Service Error",
            "detail": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url),
            "method": request.method,
            "service": exc.service_name
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled Exception: {type(exc).__name__} - {str(exc)}")
    logger.error(f"Request: {request.method} {request.url}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "status_code": 500,
            "path": str(request.url),
            "method": request.method,
            "error_type": type(exc).__name__
        }
    )
