from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Student Service", version="1.0.0")

# In-memory database
students_db = {}
student_id_counter = 1


class Student(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    age: int
    major: str


@app.get("/")
def read_root():
    return {"message": "Student Service is running", "service": "student-service"}


@app.get("/students", response_model=List[Student])
def get_all_students():
    """Get all students"""
    return list(students_db.values())


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    """Get a specific student by ID"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]


@app.post("/students", response_model=Student, status_code=201)
def create_student(student: Student):
    """Create a new student"""
    global student_id_counter
    student.id = student_id_counter
    students_db[student_id_counter] = student
    student_id_counter += 1
    return student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    """Update an existing student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    student.id = student_id
    students_db[student_id] = student
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """Delete a student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return {"message": "Student deleted successfully"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "student-service"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
