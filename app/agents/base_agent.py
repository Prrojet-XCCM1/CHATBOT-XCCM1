from abc import ABC, abstractmethod
from app.models.message import AgentRequest, AgentResponse
from app.config import Config
import openai
import asyncio
from openai import AsyncOpenAI  # Note: AsyncOpenAI

class BaseAgent(ABC):
    def __init__(self, agent_type: str, discipline: str):
        self.agent_type = agent_type
        self.discipline = discipline
        
        # Utiliser AsyncOpenAI
        self.client = AsyncOpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=Config.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": Config.SITE_URL,
                "X-Title": "Education Multi-Agent System"
            }
        )
    
    async def call_openai(self, messages: list, temperature: float = 0.7) -> str:
        """Appeler l'API OpenAI/OpenRouter (asynchrone)"""
        try:
            response = await self.client.chat.completions.create(
                model=Config.OPENROUTER_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=Config.MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")