from app.models.base import BaseModel, Discipline, DifficultyLevel
from typing import Optional, List, Dict
from datetime import datetime

class Course(BaseModel):
    id: str
    title: str
    description: str
    discipline: Discipline
    difficulty: DifficultyLevel
    teacher_id: str
    created_at: str
    updated_at: Optional[str] = None
    content: Optional[str] = None
    tags: List[str] = []
    learning_objectives: List[str] = []
    prerequisites: List[str] = []
    
class CourseModule(BaseModel):
    id: str
    course_id: str
    title: str
    order: int
    content: str
    estimated_duration: int  # en minutes
    resources: List[str] = []
    
class StudentProgress(BaseModel):
    student_id: str
    course_id: str
    module_id: str
    completed: bool = False
    completion_date: Optional[str] = None
    quiz_score: Optional[float] = None
    time_spent: int = 0  # en minutes