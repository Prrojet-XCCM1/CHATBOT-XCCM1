import json
import redis
from app.config import Config
from typing import Optional, Dict, List

class KnowledgeBase:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(Config.REDIS_URL)
        self.load_default_knowledge()
    
    def load_default_knowledge(self):
        """Charger les connaissances par défaut"""
        self.discipline_concepts = {
            "mathematics": [
                "Algèbre", "Géométrie", "Analyse", "Statistiques", 
                "Probabilités", "Logique", "Théorie des nombres"
            ],
            "physics": [
                "Mécanique", "Thermodynamique", "Électromagnétisme",
                "Optique", "Physique quantique", "Relativité"
            ],
            "computer_science": [
                "Algorithmique", "Structures de données", "Bases de données",
                "Réseaux", "Sécurité", "Programmation", "Architecture"
            ]
        }
    
    def get_concepts(self, discipline: str) -> List[str]:
        """Récupérer les concepts d'une discipline"""
        return self.discipline_concepts.get(discipline, [])
    
    def add_concept(self, discipline: str, concept: str):
        """Ajouter un concept à une discipline"""
        if discipline not in self.discipline_concepts:
            self.discipline_concepts[discipline] = []
        self.discipline_concepts[discipline].append(concept)
        self.save_to_cache(discipline)
    
    def save_to_cache(self, discipline: str):
        """Sauvegarder dans Redis"""
        key = f"knowledge:{discipline}"
        self.redis_client.set(key, json.dumps(self.discipline_concepts[discipline]))
    
    def get_from_cache(self, discipline: str) -> Optional[List[str]]:
        """Récupérer du cache Redis"""
        key = f"knowledge:{discipline}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def search_concept(self, query: str, discipline: str = None) -> List[str]:
        """Rechercher un concept"""
        results = []
        disciplines = [discipline] if discipline else self.discipline_concepts.keys()
        
        for disc in disciplines:
            for concept in self.discipline_concepts.get(disc, []):
                if query.lower() in concept.lower():
                    results.append(f"{concept} ({disc})")
        
        return results