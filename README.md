# MTIT Practical-3: Microservices Architecture

A microservices-based REST API system built with FastAPI, featuring student and course management services with a unified API gateway.

## Architecture Overview

This project implements a microservices architecture with the following components:

- **API Gateway** (Port 8000): Unified entry point that routes requests to appropriate services
- **Student Service** (Port 8001): Manages student data and operations
- **Course Service** (Port 8002): Manages course data and operations

All services are containerized using Docker and can be orchestrated using Docker Compose.

## Features

### Student Service
- Create, Read, Update, and Delete (CRUD) operations for students
- Student attributes: ID, Name, Email, Age, Major
- RESTful API endpoints
- Health check endpoint

### Course Service
- Create, Read, Update, and Delete (CRUD) operations for courses
- Course attributes: ID, Name, Code, Credits, Instructor
- RESTful API endpoints
- Health check endpoint

### API Gateway
- Unified routing to all microservices
- Health monitoring for all services
- Service discovery and load balancing
- Centralized error handling

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized deployment)

## Installation and Setup

### Option 1: Running with Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/IT22277190/MTIT_Practical-3_microservices-.git
cd MTIT_Practical-3_microservices-
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the services:
   - API Gateway: http://localhost:8000
   - Student Service: http://localhost:8001
   - Course Service: http://localhost:8002

### Option 2: Running Locally

1. Install dependencies for each service:

```bash
# Student Service
cd student-service
pip install -r requirements.txt

# Course Service
cd ../course-service
pip install -r requirements.txt

# API Gateway
cd ../api-gateway
pip install -r requirements.txt
```

2. Start each service in separate terminal windows:

```bash
# Terminal 1 - Student Service
cd student-service
python main.py

# Terminal 2 - Course Service
cd course-service
python main.py

# Terminal 3 - API Gateway
cd api-gateway
python main.py
```

## API Documentation

### API Gateway Endpoints

All requests should be made through the API Gateway at `http://localhost:8000`

#### Gateway Status
- `GET /` - Gateway information and service URLs
- `GET /health` - Health check for gateway and all services

#### Student Management

- `GET /api/students` - Get all students
- `GET /api/students/{id}` - Get a specific student
- `POST /api/students` - Create a new student
- `PUT /api/students/{id}` - Update a student
- `DELETE /api/students/{id}` - Delete a student

**Example Student JSON:**
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "age": 20,
  "major": "Computer Science"
}
```

#### Course Management

- `GET /api/courses` - Get all courses
- `GET /api/courses/{id}` - Get a specific course
- `POST /api/courses` - Create a new course
- `PUT /api/courses/{id}` - Update a course
- `DELETE /api/courses/{id}` - Delete a course

**Example Course JSON:**
```json
{
  "name": "Introduction to Programming",
  "code": "CS101",
  "credits": 3,
  "instructor": "Dr. Smith"
}
```

## Testing the API

### Using cURL

#### Create a Student:
```bash
curl -X POST "http://localhost:8000/api/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 21,
    "major": "Data Science"
  }'
```

#### Get All Students:
```bash
curl "http://localhost:8000/api/students"
```

#### Create a Course:
```bash
curl -X POST "http://localhost:8000/api/courses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Machine Learning",
    "code": "CS401",
    "credits": 4,
    "instructor": "Prof. Davis"
  }'
```

#### Get All Courses:
```bash
curl "http://localhost:8000/api/courses"
```

### Using Swagger UI

Each service provides an interactive API documentation:
- API Gateway: http://localhost:8000/docs
- Student Service: http://localhost:8001/docs
- Course Service: http://localhost:8002/docs

## Architecture Design Decisions

1. **Microservices Pattern**: Each service is independent and can be scaled separately
2. **API Gateway Pattern**: Provides a single entry point and handles routing
3. **In-Memory Storage**: Simplified for demonstration; can be replaced with a database
4. **Docker Containerization**: Ensures consistency across environments
5. **Health Checks**: Monitoring endpoint for service availability

## Project Structure

```
.
├── api-gateway/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── student-service/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── course-service/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Future Enhancements

- Add persistent database (PostgreSQL/MongoDB)
- Implement authentication and authorization
- Add service-to-service communication
- Implement caching layer (Redis)
- Add logging and monitoring (ELK stack)
- Implement circuit breaker pattern
- Add API rate limiting
- Implement student-course enrollment relationship

## Technology Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **HTTP Client**: httpx (for API Gateway)

## License

This project is created for educational purposes as part of MTIT Practical-3.

## Author

IT22277190
