# gateway/main.py 
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import httpx 
from typing import Any
from datetime import timedelta
from auth import (
    authenticate_user, create_access_token, get_current_active_user,
    Token, User
)
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from middleware import RequestLoggingMiddleware
from error_handlers import (
    http_exception_handler, validation_exception_handler,
    service_unavailable_handler, service_error_handler,
    general_exception_handler, ServiceUnavailableError, ServiceError
) 
 
app = FastAPI(title="API Gateway", version="1.0.0")

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Register exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ServiceUnavailableError, service_unavailable_handler)
app.add_exception_handler(ServiceError, service_error_handler)
app.add_exception_handler(Exception, general_exception_handler) 
 
# Service URLs 
SERVICES = { 
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
} 
 
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any: 
    """Forward request to the appropriate microservice""" 
    if service not in SERVICES: 
        raise HTTPException(
            status_code=404, 
            detail=f"Service '{service}' not found. Available services: {', '.join(SERVICES.keys())}"
        ) 
     
    url = f"{SERVICES[service]}{path}" 
     
    async with httpx.AsyncClient(timeout=30.0) as client: 
        try: 
            if method == "GET": 
                response = await client.get(url, **kwargs) 
            elif method == "POST": 
                response = await client.post(url, **kwargs) 
            elif method == "PUT": 
                response = await client.put(url, **kwargs) 
            elif method == "DELETE": 
                response = await client.delete(url, **kwargs) 
            else: 
                raise HTTPException(
                    status_code=405, 
                    detail=f"Method '{method}' not allowed. Supported methods: GET, POST, PUT, DELETE"
                )
            
            # Check if the service returned an error
            if response.status_code >= 400:
                try:
                    error_detail = response.json().get("detail", response.text)
                except:
                    error_detail = response.text or "Unknown error"
                
                raise ServiceError(
                    service_name=service,
                    status_code=response.status_code,
                    detail=error_detail
                )
            
            return JSONResponse( 
                content=response.json() if response.text else None, 
                status_code=response.status_code 
            )
        except httpx.TimeoutException:
            raise ServiceUnavailableError(
                service_name=service,
                detail=f"Request to {service} service timed out after 30 seconds"
            )
        except httpx.ConnectError:
            raise ServiceUnavailableError(
                service_name=service,
                detail=f"Could not connect to {service} service at {SERVICES[service]}"
            )
        except httpx.RequestError as e: 
            raise ServiceUnavailableError(
                service_name=service,
                detail=f"Request error: {str(e)}"
            )
        except ServiceError:
            # Re-raise ServiceError to be handled by the exception handler
            raise 
 
@app.get("/") 
def read_root(): 
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

# Authentication endpoint
@app.post("/gateway/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/gateway/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user 
 
# Student Service Routes 
@app.get("/gateway/students") 
async def get_all_students(current_user: User = Depends(get_current_active_user)): 
    """Get all students through gateway""" 
    return await forward_request("student", "/api/students", "GET") 
 
@app.get("/gateway/students/{student_id}") 
async def get_student(student_id: int, current_user: User = Depends(get_current_active_user)): 
    """Get a student by ID through gateway""" 
    return await forward_request("student", f"/api/students/{student_id}", "GET") 
 
@app.post("/gateway/students") 
async def create_student(request: Request, current_user: User = Depends(get_current_active_user)): 
    """Create a new student through gateway""" 
    body = await request.json() 
    return await forward_request("student", "/api/students", "POST", json=body) 
 
@app.put("/gateway/students/{student_id}") 
async def update_student(student_id: int, request: Request, current_user: User = Depends(get_current_active_user)): 
    """Update a student through gateway""" 
    body = await request.json() 
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body) 
 
@app.delete("/gateway/students/{student_id}") 
async def delete_student(student_id: int, current_user: User = Depends(get_current_active_user)): 
    """Delete a student through gateway""" 
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")

# Course Service Routes
@app.get("/gateway/courses")
async def get_all_courses(current_user: User = Depends(get_current_active_user)):
    """Get all courses through gateway"""
    return await forward_request("course", "/api/courses", "GET")

@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int, current_user: User = Depends(get_current_active_user)):
    """Get a course by ID through gateway"""
    return await forward_request("course", f"/api/courses/{course_id}", "GET")

@app.post("/gateway/courses")
async def create_course(request: Request, current_user: User = Depends(get_current_active_user)):
    """Create a new course through gateway"""
    body = await request.json()
    return await forward_request("course", "/api/courses", "POST", json=body)

@app.put("/gateway/courses/{course_id}")
async def update_course(course_id: int, request: Request, current_user: User = Depends(get_current_active_user)):
    """Update a course through gateway"""
    body = await request.json()
    return await forward_request("course", f"/api/courses/{course_id}", "PUT", json=body)

@app.delete("/gateway/courses/{course_id}")
async def delete_course(course_id: int, current_user: User = Depends(get_current_active_user)):
    """Delete a course through gateway"""
    return await forward_request("course", f"/api/courses/{course_id}", "DELETE")