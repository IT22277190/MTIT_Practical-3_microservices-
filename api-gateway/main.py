from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
import uvicorn
import os

app = FastAPI(title="API Gateway", version="1.0.0")

# Service URLs - can be configured via environment variables
STUDENT_SERVICE_URL = os.getenv("STUDENT_SERVICE_URL", "http://localhost:8001")
COURSE_SERVICE_URL = os.getenv("COURSE_SERVICE_URL", "http://localhost:8002")

# Timeout for requests to microservices
REQUEST_TIMEOUT = 30.0


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "services": {
            "students": f"{STUDENT_SERVICE_URL}",
            "courses": f"{COURSE_SERVICE_URL}"
        }
    }


@app.get("/health")
def health_check():
    """Check health of the gateway and all services"""
    health_status = {
        "gateway": "healthy",
        "services": {}
    }
    
    # Check student service
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{STUDENT_SERVICE_URL}/health")
            health_status["services"]["student-service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        health_status["services"]["student-service"] = f"unhealthy: {str(e)}"
    
    # Check course service
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{COURSE_SERVICE_URL}/health")
            health_status["services"]["course-service"] = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception as e:
        health_status["services"]["course-service"] = f"unhealthy: {str(e)}"
    
    return health_status


# Student Service Routes
@app.api_route("/api/students", methods=["GET", "POST"])
async def students_route(request: Request):
    """Route requests to student service"""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if request.method == "GET":
                response = await client.get(f"{STUDENT_SERVICE_URL}/students")
            elif request.method == "POST":
                body = await request.json()
                response = await client.post(f"{STUDENT_SERVICE_URL}/students", json=body)
            
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Student service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.api_route("/api/students/{student_id}", methods=["GET", "PUT", "DELETE"])
async def student_detail_route(student_id: int, request: Request):
    """Route requests for specific student to student service"""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if request.method == "GET":
                response = await client.get(f"{STUDENT_SERVICE_URL}/students/{student_id}")
            elif request.method == "PUT":
                body = await request.json()
                response = await client.put(f"{STUDENT_SERVICE_URL}/students/{student_id}", json=body)
            elif request.method == "DELETE":
                response = await client.delete(f"{STUDENT_SERVICE_URL}/students/{student_id}")
            
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Student service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Course Service Routes
@app.api_route("/api/courses", methods=["GET", "POST"])
async def courses_route(request: Request):
    """Route requests to course service"""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if request.method == "GET":
                response = await client.get(f"{COURSE_SERVICE_URL}/courses")
            elif request.method == "POST":
                body = await request.json()
                response = await client.post(f"{COURSE_SERVICE_URL}/courses", json=body)
            
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Course service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.api_route("/api/courses/{course_id}", methods=["GET", "PUT", "DELETE"])
async def course_detail_route(course_id: int, request: Request):
    """Route requests for specific course to course service"""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if request.method == "GET":
                response = await client.get(f"{COURSE_SERVICE_URL}/courses/{course_id}")
            elif request.method == "PUT":
                body = await request.json()
                response = await client.put(f"{COURSE_SERVICE_URL}/courses/{course_id}", json=body)
            elif request.method == "DELETE":
                response = await client.delete(f"{COURSE_SERVICE_URL}/courses/{course_id}")
            
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Course service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
