from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class Discipline(str, Enum):
    MATHEMATICS = "mathematics"
    PHYSICS = "physics"
    COMPUTER_SCIENCE = "computer_science"
    LIFE_SCIENCES = "life_sciences"
    DATABASES = "databases"
    AI = "artificial_intelligence"
    GENERAL = "general"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"