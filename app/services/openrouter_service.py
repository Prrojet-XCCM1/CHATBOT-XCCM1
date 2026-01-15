import openai
from app.config import Config
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)

class OpenRouterService:
    def __init__(self):
        # Configuration OpenAI client pour OpenRouter
        self.client = openai.OpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=Config.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "http://localhost:5000",  # Votre URL
                "X-Title": "Education Multi-Agent System"
            }
        )
        self.default_model = Config.OPENROUTER_MODEL
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_completion(self, messages: list, **kwargs) -> str:
        try:
            model = kwargs.get('model', self.default_model)
            temperature = kwargs.get('temperature', 0.7)
            max_tokens = kwargs.get('max_tokens', Config.MAX_TOKENS)
            
            logger.debug(f"Calling OpenRouter with model: {model}")
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except openai.APIError as e:
            logger.error(f"OpenRouter API error: {str(e)}")
            raise Exception(f"OpenRouter API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise
    
    def get_available_models(self) -> list:
        """Récupérer les modèles disponibles sur OpenRouter"""
        # Note: OpenRouter n'a pas d'endpoint officiel pour lister les modèles
        # On retourne une liste prédéfinie
        return list(Config.OPENROUTER_MODELS.values())
    
    def select_model_by_discipline(self, discipline: str) -> str:
        """Sélectionner un modèle optimal selon la discipline"""
        model_mapping = {
            'mathematics': Config.OPENROUTER_MODELS['geminiflash'],  # Bon pour le raisonnement
            'physics': Config.OPENROUTER_MODELS['llama'],  # Bon pour les sciences
            'computer_science': Config.OPENROUTER_MODELS['gpt'],  # Bon pour le code
            'life_sciences': Config.OPENROUTER_MODELS['claude'],  # Bon pour les textes longs
            'databases': Config.OPENROUTER_MODELS['gpt'],  # Bon pour le SQL
            'artificial_intelligence': Config.OPENROUTER_MODELS['gpt'],  # Bon pour les concepts IA
            'general': self.default_model
        }
        
        return model_mapping.get(discipline, self.default_model)