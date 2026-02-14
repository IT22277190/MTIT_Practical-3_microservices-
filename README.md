# Microservices FastAPI Project

A microservices-based REST API system built with FastAPI, featuring student and course management services with a unified API gateway.

## Architecture

- **API Gateway** (Port 8000): Central entry point with authentication, logging, and request forwarding
- **Student Service** (Port 8001): Manages student data
- **Course Service** (Port 8002): Manages course data

## Features

### ✅ Activity 1: Course Microservice
- Full CRUD operations for courses
- RESTful API endpoints
- Mock data storage

### ✅ Activity 2: JWT Authentication
- Token-based authentication
- Protected endpoints
- Username/password login

### ✅ Activity 3: Request Logging
- Middleware logging all requests and responses
- Request ID tracking
- Performance metrics
- Log file: `gateway_requests.log`

### ✅ Activity 4: Enhanced Error Handling
- Detailed error messages
- Proper HTTP status codes
- Service-specific error responses
- Validation error details

## Installation

1. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Running the Services

### Start Student Service:
```powershell
cd student-service
uvicorn main:app --reload --port 8001
```

### Start Course Service:
```powershell
cd course-service
uvicorn main:app --reload --port 8002
```

### Start API Gateway:
```powershell
cd gateway
uvicorn main:app --reload --port 8000
```

## Authentication

### Login Credentials
- **Username**: `admin` or `user`
- **Password**: `secret`

### Getting Access Token

**Request:**
```bash
POST http://localhost:8000/gateway/token
Content-Type: application/x-www-form-urlencoded

username=admin&password=secret
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Add the token to the Authorization header for all protected endpoints:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

### Gateway Endpoints

#### Authentication
- `POST /gateway/token` - Login to get access token
- `GET /gateway/users/me` - Get current user info (protected)

#### Student Endpoints (All Protected)
- `GET /gateway/students` - Get all students
- `GET /gateway/students/{id}` - Get student by ID
- `POST /gateway/students` - Create new student
- `PUT /gateway/students/{id}` - Update student
- `DELETE /gateway/students/{id}` - Delete student

#### Course Endpoints (All Protected)
- `GET /gateway/courses` - Get all courses
- `GET /gateway/courses/{id}` - Get course by ID
- `POST /gateway/courses` - Create new course
- `PUT /gateway/courses/{id}` - Update course
- `DELETE /gateway/courses/{id}` - Delete course

## Example Usage

### 1. Login
```bash
curl -X POST "http://localhost:8000/gateway/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=secret"
```

### 2. Get All Students (with token)
```bash
curl -X GET "http://localhost:8000/gateway/students" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Create a Student
```bash
curl -X POST "http://localhost:8000/gateway/students" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Brown",
    "age": 20,
    "email": "alice@example.com",
    "course": "Computer Science"
  }'
```

### 4. Get All Courses
```bash
curl -X GET "http://localhost:8000/gateway/courses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Create a Course
```bash
curl -X POST "http://localhost:8000/gateway/courses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "CS401",
    "name": "Advanced Algorithms",
    "credits": 4,
    "instructor": "Dr. Taylor",
    "department": "Computer Science"
  }'
```

## Data Models

### Student
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com",
  "course": "Computer Science"
}
```

### Course
```json
{
  "id": 1,
  "code": "CS101",
  "name": "Introduction to Programming",
  "credits": 3,
  "instructor": "Dr. Smith",
  "department": "Computer Science"
}
```

## Error Response Format

All errors follow a consistent format:
```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "status_code": 404,
  "path": "/gateway/students/999",
  "method": "GET",
  "service": "student-service"
}
```

## Logging

Request logs include:
- Request ID (for tracking)
- HTTP Method and URL
- Client IP Address
- Request/Response headers
- Processing time
- Error details (if any)

Logs are saved to `gateway_requests.log` in the gateway directory.

## Testing with Swagger UI

Access the interactive API documentation:
- Gateway: http://localhost:8000/docs
- Student Service: http://localhost:8001/docs
- Course Service: http://localhost:8002/docs

For protected endpoints in Swagger:
1. Click "Authorize" button
2. Enter: `admin` / `secret`
3. Click "Authorize"
4. Now you can test protected endpoints

## Project Structure

```
microservices-fastapi/
├── requirements.txt
├── README.md
├── gateway/
│   ├── main.py
│   ├── auth.py
│   ├── config.py
│   ├── middleware.py
│   ├── error_handlers.py
│   └── gateway_requests.log
├── student-service/
│   ├── main.py
│   ├── models.py
│   ├── service.py
│   ├── data_service.py
│   └── error_handlers.py
└── course-service/
    ├── main.py
    ├── models.py
    ├── service.py
    ├── data_service.py
    └── error_handlers.py
```

## Security Notes

⚠️ **Important for Production:**
- Change the SECRET_KEY in `gateway/config.py`
- Use a real database instead of mock data
- Use environment variables for configuration
- Implement proper user management
- Add rate limiting
- Use HTTPS in production
- Implement proper password validation

## Dependencies

- fastapi==0.115.0
- uvicorn[standard]==0.32.0
- pydantic==2.10.0
- httpx==0.27.0
- python-multipart==0.0.12
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- python-dotenv==1.0.0
