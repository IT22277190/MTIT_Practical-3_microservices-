from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Course Service", version="1.0.0")

# In-memory database
courses_db = {}
course_id_counter = 1


class Course(BaseModel):
    id: Optional[int] = None
    name: str
    code: str
    credits: int
    instructor: str


@app.get("/")
def read_root():
    return {"message": "Course Service is running", "service": "course-service"}


@app.get("/courses", response_model=List[Course])
def get_all_courses():
    """Get all courses"""
    return list(courses_db.values())


@app.get("/courses/{course_id}", response_model=Course)
def get_course(course_id: int):
    """Get a specific course by ID"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses_db[course_id]


@app.post("/courses", response_model=Course, status_code=201)
def create_course(course: Course):
    """Create a new course"""
    global course_id_counter
    course.id = course_id_counter
    courses_db[course_id_counter] = course
    course_id_counter += 1
    return course


@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course: Course):
    """Update an existing course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    course.id = course_id
    courses_db[course_id] = course
    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    """Delete a course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses_db[course_id]
    return {"message": "Course deleted successfully"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "course-service"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
