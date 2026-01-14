import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    
    # Agents
    AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', 30))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    
    # Redis (pour cache et queues)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
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