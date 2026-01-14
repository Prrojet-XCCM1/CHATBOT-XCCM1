from app.services.llm_provider_factory import LLMProviderFactory, LLMProvider
from app.config import Config
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Service LLM universel qui route vers le bon provider"""
    
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider
        self.service = LLMProviderFactory.get_provider(provider)
        
    async def generate_completion(self, messages: list, **kwargs) -> str:
        """Générer une complétion via le provider configuré"""
        try:
            # Ajouter des headers spécifiques pour OpenRouter si nécessaire
            if self.provider == LLMProvider.OPENROUTER or hasattr(Config, 'OPENROUTER_API_KEY'):
                if 'extra_headers' not in kwargs:
                    kwargs['extra_headers'] = {
                        "HTTP-Referer": "http://localhost:5000",
                        "X-Title": "Education Multi-Agent"
                    }
            
            return await self.service.generate_completion(messages, **kwargs)
            
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            
            # Fallback vers un autre provider si disponible
            if self.provider != LLMProvider.OPENAI and hasattr(Config, 'OPENAI_API_KEY'):
                logger.info("Trying OpenAI fallback...")
                fallback_service = LLMProviderFactory.get_provider(LLMProvider.OPENAI)
                return await fallback_service.generate_completion(messages, **kwargs)
            
            raise
    
    def get_model_for_discipline(self, discipline: str) -> str:
        """Obtenir le meilleur modèle pour une discipline donnée"""
        if hasattr(self.service, 'select_model_by_discipline'):
            return self.service.select_model_by_discipline(discipline)
        return Config.OPENROUTER_MODEL if hasattr(Config, 'OPENROUTER_MODEL') else 'gpt-4'