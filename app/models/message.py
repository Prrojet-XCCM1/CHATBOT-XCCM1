from app.models.base import BaseModel, Discipline, DifficultyLevel, UserRole
from typing import Optional, List

class Message(BaseModel):
    content: str
    role: str  # user, assistant, system
    timestamp: str
    
class ConversationContext(BaseModel):
    user_id: str
    user_role: UserRole
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    discipline: Discipline
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    conversation_history: List[Message] = []
    
class AgentRequest(BaseModel):
    question: str
    user_id: str
    user_role: UserRole
    discipline: Discipline
    course_context: Optional[str] = None
    difficulty_level: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    conversation_history: List[Message] = []
    
class AgentResponse(BaseModel):
    answer: str
    sources: List[str] = []
    suggested_resources: List[str] = []
    agent_type: str
    confidence_score: float = 0.0
    follow_up_questions: List[str] = []