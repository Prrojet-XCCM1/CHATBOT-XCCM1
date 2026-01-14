from abc import ABC, abstractmethod
from app.models.message import AgentRequest, AgentResponse
from app.services.llm_service import LLMService

class BaseAgent(ABC):
    def __init__(self, agent_type: str, discipline: str):
        self.agent_type = agent_type
        self.discipline = discipline
        self.llm_service = LLMService()
    
    @abstractmethod
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        pass
    
    async def call_llm(self, messages: list, temperature: float = 0.7, model: str = None) -> str:
        try:
            if model is None:
                model = self.llm_service.get_model_for_discipline(self.discipline)
            
            response_text = await self.llm_service.generate_completion(
                messages=messages,
                model=model,
                temperature=temperature
            )
            return response_text
        except Exception as e:
            raise Exception(f"LLM API error: {str(e)}")