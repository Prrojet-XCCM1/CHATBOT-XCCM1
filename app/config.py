import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())
    
    # OpenRouter
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.1-8b-instruct')
    
    # Alternatives models sur OpenRouter
    OPENROUTER_MODELS = {
        'llama': 'meta-llama/llama-3.1-8b-instruct',
        'mistral': 'mistralai/mistral-7b-instruct',
        'gemini': 'google/gemini-pro',
        'claude': 'anthropic/claude-3-haiku',
        'gpt': 'openai/gpt-4',
        'geminiflash': 'google/gemini-2.0-flash-001'
    }

    # Redis (utilisé pour la mise en cache cloud gratuit sur render)
    RENDER = os.getenv('RENDER', 'false').lower() == 'true'
    
    # Agents
    AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', 30))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # URL du site pour OpenRouter
    SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')
    
    # Domaines supportés
    SUPPORTED_DISCIPLINES = [
        'mathematics',
        'physics',
        'computer_science',
        'life_sciences',
        'databases',
        'artificial_intelligence',
        'general'
    ]