import redis
import json
from app.config import Config
from typing import Optional, Any
import hashlib
from datetime import datetime, timedelta

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.default_ttl = 3600  # 1 heure
    
    def generate_key(self, *args) -> str:
        """Générer une clé de cache unique"""
        key_string = ":".join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Récupérer une valeur du cache"""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Stocker une valeur dans le cache"""
        ttl = ttl or self.default_ttl
        serialized = json.dumps(value)
        self.redis_client.setex(key, ttl, serialized)
    
    def cache_response(self, question: str, user_id: str, response: Any) -> str:
        """Mettre en cache une réponse d'assistant"""
        cache_key = self.generate_key("assistant_response", user_id, question)
        self.set(cache_key, response)
        return cache_key
    
    def get_cached_response(self, question: str, user_id: str) -> Optional[Any]:
        """Récupérer une réponse mise en cache"""
        cache_key = self.generate_key("assistant_response", user_id, question)
        return self.get(cache_key)
    
    def cache_conversation(self, conversation_id: str, messages: list):
        """Mettre en cache une conversation"""
        cache_key = f"conversation:{conversation_id}"
        self.set(cache_key, messages, ttl=86400)  # 24 heures
    
    def get_conversation(self, conversation_id: str) -> Optional[list]:
        """Récupérer une conversation du cache"""
        cache_key = f"conversation:{conversation_id}"
        return self.get(cache_key)
    
    def increment_counter(self, key: str) -> int:
        """Incrémenter un compteur"""
        return self.redis_client.incr(key)
    
    def get_stats(self) -> dict:
        """Obtenir des statistiques du cache"""
        return {
            "connected": self.redis_client.ping(),
            "keys": self.redis_client.dbsize(),
            "info": self.redis_client.info()
        }