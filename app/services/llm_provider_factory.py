from abc import ABC, abstractmethod
from enum import Enum
from app.config import Config

class LLMProvider(Enum):
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    LOCAL = "local"  # Pour les modèles locaux comme Ollama

class LLMProviderFactory:
    @staticmethod
    def get_provider(provider: LLMProvider = None):
        """Factory pour obtenir le bon service LLM"""
        if provider is None:
            # Déterminer automatiquement basé sur la configuration
            if hasattr(Config, 'OPENROUTER_API_KEY') and Config.OPENROUTER_API_KEY:
                provider = LLMProvider.OPENROUTER
            elif hasattr(Config, 'OPENAI_API_KEY') and Config.OPENAI_API_KEY:
                provider = LLMProvider.OPENAI
            else:
                raise ValueError("Aucun provider LLM configuré")
        
        if provider == LLMProvider.OPENROUTER:
            from app.services.openrouter_service import OpenRouterService
            return OpenRouterService()
        elif provider == LLMProvider.OPENAI:
            from app.services.openai_service import OpenAIService
            return OpenAIService()
        elif provider == LLMProvider.LOCAL:
            from app.services.local_llm_service import LocalLLMService
            return LocalLLMService()
        else:
            raise ValueError(f"Provider non supporté: {provider}")