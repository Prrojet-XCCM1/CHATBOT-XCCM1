from abc import ABC, abstractmethod
from app.models.message import AgentRequest, AgentResponse
from app.config import Config
import openai
import json

class BaseAgent(ABC):
    def __init__(self, agent_type: str, discipline: str):
        self.agent_type = agent_type
        self.discipline = discipline
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    @abstractmethod
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        pass
    
    async def call_openai(self, messages: list, temperature: float = 0.7) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def format_prompt(self, prompt_template: str, **kwargs) -> str:
        return prompt_template.format(**kwargs)