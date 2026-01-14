from app.models.base import BaseModel, UserRole
from typing import Optional, List

class User(BaseModel):
    id: str
    email: str
    username: str
    role: UserRole
    full_name: str
    created_at: str
    disciplines: List[str] = []  # disciplines d'intérêt/enseignement
    preferences: Dict = {}
    
class TeacherProfile(BaseModel):
    teacher_id: str
    bio: Optional[str] = None
    expertise: List[str] = []
    years_experience: int = 0
    courses_created: int = 0
    rating: Optional[float] = None
    
class StudentProfile(BaseModel):
    student_id: str
    level: str = "beginner"
    completed_courses: int = 0
    current_courses: List[str] = []
    learning_goals: List[str] = []