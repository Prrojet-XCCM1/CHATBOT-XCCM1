from app.models.base import BaseModel, Discipline
from typing import Optional, Dict
from enum import Enum

class AgentType(str, Enum):
    STUDENT_ASSISTANT = "student_assistant"
    TEACHER_ASSISTANT = "teacher_assistant"
    SPECIALIST = "specialist"
    COORDINATOR = "coordinator"

class AgentState(str, Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    TRAINING = "training"

class Agent(BaseModel):
    id: str
    name: str
    agent_type: AgentType
    discipline: Discipline
    state: AgentState = AgentState.IDLE
    capabilities: List[str] = []
    performance_metrics: Dict = {}
    last_active: str
    model_config: Optional[Dict] = None