import pytest
from app.services.knowledge_base import KnowledgeBase
from app.services.prompt_manager import PromptManager
from app.services.cache_service import CacheService
import json

@pytest.fixture
def knowledge_base():
    return KnowledgeBase()

@pytest.fixture
def prompt_manager():
    return PromptManager()

@pytest.fixture
def cache_service():
    return CacheService()

def test_knowledge_base_concepts(knowledge_base):
    """Test de la base de connaissances"""
    concepts = knowledge_base.get_concepts("mathematics")
    assert isinstance(concepts, list)
    assert len(concepts) > 0
    
    # Vérifier la présence de concepts connus
    expected_concepts = ["Algèbre", "Géométrie"]
    for concept in expected_concepts:
        assert concept in concepts

def test_knowledge_base_add_concept(knowledge_base):
    """Test d'ajout de concept"""
    initial_count = len(knowledge_base.get_concepts("mathematics"))
    
    knowledge_base.add_concept("mathematics", "Nouveau concept")
    
    concepts = knowledge_base.get_concepts("mathematics")
    assert len(concepts) == initial_count + 1
    assert "Nouveau concept" in concepts

def test_prompt_manager_loading(prompt_manager):
    """Test du chargement des prompts"""
    prompts = prompt_manager.prompts
    assert isinstance(prompts, dict)
    assert len(prompts) > 0
    
    # Vérifier les fichiers de prompts chargés
    assert "student_prompts" in prompts
    assert "teacher_prompts" in prompts

def test_prompt_manager_get_prompt(prompt_manager):
    """Test de récupération de prompt"""
    student_prompts = prompt_manager.get_prompt("student_prompts")
    assert isinstance(student_prompts, dict)
    assert "default" in student_prompts
    
    # Test avec clé spécifique
    specific_prompt = prompt_manager.get_prompt("student_prompts", "default")
    assert "system" in specific_prompt
    assert "user" in specific_prompt

def test_prompt_manager_system_prompt(prompt_manager):
    """Test de génération de prompt système"""
    system_prompt = prompt_manager.get_system_prompt(
        role="student",
        discipline="mathematics",
        difficulty="beginner"
    )
    
    assert isinstance(system_prompt, str)
    assert len(system_prompt) > 0

def test_cache_service_basic_operations(cache_service):
    """Test des opérations basiques du cache"""
    test_key = "test_key"
    test_value = {"data": "test", "number": 42}
    
    # Test set et get
    cache_service.set(test_key, test_value)
    retrieved = cache_service.get(test_key)
    
    assert retrieved == test_value
    
    # Test avec TTL
    cache_service.set(test_key, test_value, ttl=1)
    import time
    time.sleep(1.1)  # Attendre que le cache expire
    
    expired = cache_service.get(test_key)
    assert expired is None

def test_cache_service_generate_key(cache_service):
    """Test de génération de clé de cache"""
    key1 = cache_service.generate_key("user1", "question1")
    key2 = cache_service.generate_key("user1", "question1")
    key3 = cache_service.generate_key("user1", "question2")
    
    assert key1 == key2  # Mêmes paramètres = même clé
    assert key1 != key3  # Paramètres différents = clés différentes
    
    # Vérifier que la clé est un hash MD5
    assert len(key1) == 32  # Longueur MD5 hex

def test_cache_conversation(cache_service):
    """Test de mise en cache de conversation"""
    conversation_id = "conv_123"
    messages = [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Bonjour, comment puis-vous aider ?"}
    ]
    
    cache_service.cache_conversation(conversation_id, messages)
    
    retrieved = cache_service.get_conversation(conversation_id)
    assert retrieved == messages

def test_cache_response(cache_service):
    """Test de mise en cache de réponse"""
    question = "Quelle est la capitale de la France ?"
    user_id = "user123"
    response = {"answer": "Paris", "sources": ["géographie"]}
    
    cache_key = cache_service.cache_response(question, user_id, response)
    
    retrieved = cache_service.get_cached_response(question, user_id)
    assert retrieved == response
    
    # Vérifier que la clé générée fonctionne
    assert cache_service.get(cache_key) == response

def test_cache_increment_counter(cache_service):
    """Test d'incrémentation de compteur"""
    counter_key = "test_counter"
    
    # Initialiser à 0
    cache_service.redis_client.delete(counter_key)
    
    # Incrémenter
    result1 = cache_service.increment_counter(counter_key)
    result2 = cache_service.increment_counter(counter_key)
    
    assert result1 == 1
    assert result2 == 2

def test_cache_stats(cache_service):
    """Test des statistiques du cache"""
    stats = cache_service.get_stats()
    
    assert isinstance(stats, dict)
    assert "connected" in stats
    assert stats["connected"] is True
    
    # Vérifier que nous pouvons obtenir des infos
    assert "info" in stats
    assert isinstance(stats["info"], dict)