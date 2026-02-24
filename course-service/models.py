# course-service/models.py
from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: int
    code: str
    name: str
    credits: int
    instructor: str
    department: str

class CourseCreate(BaseModel):
    code: str
    name: str
    credits: int
    instructor: str
    department: str

class CourseUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    credits: Optional[int] = None
    instructor: Optional[str] = None
    department: Optional[str] = None
