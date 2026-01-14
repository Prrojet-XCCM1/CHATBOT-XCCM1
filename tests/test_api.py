import pytest
from flask import Flask
from app import create_app
import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    """Test du endpoint health"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_disciplines_endpoint(client):
    """Test du endpoint disciplines"""
    response = client.get('/api/disciplines')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'disciplines' in data
    assert len(data['disciplines']) > 0

def test_agents_endpoint(client):
    """Test du endpoint agents"""
    response = client.get('/api/agents')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'agents' in data
    assert len(data['agents']) > 0

def test_chat_endpoint_valid_request(client):
    """Test du endpoint chat avec requête valide"""
    request_data = {
        'question': 'Quelle est la formule de l\'aire d\'un cercle ?',
        'user_id': 'test_user',
        'user_role': 'student',
        'discipline': 'mathematics',
        'difficulty_level': 'beginner'
    }
    
    response = client.post('/api/chat', 
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'answer' in data
    assert 'agent_type' in data

def test_chat_endpoint_invalid_discipline(client):
    """Test avec discipline invalide"""
    request_data = {
        'question': 'Test question',
        'user_id': 'test_user',
        'user_role': 'student',
        'discipline': 'invalid_discipline'
    }
    
    response = client.post('/api/chat',
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_chat_endpoint_missing_fields(client):
    """Test avec champs manquants"""
    request_data = {
        'question': 'Test question'
        # user_role et discipline manquants
    }
    
    response = client.post('/api/chat',
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_chat_endpoint_empty_question(client):
    """Test avec question vide"""
    request_data = {
        'question': '',
        'user_id': 'test_user',
        'user_role': 'student',
        'discipline': 'mathematics'
    }
    
    response = client.post('/api/chat',
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_chat_endpoint_with_course_context(client):
    """Test avec contexte de cours"""
    request_data = {
        'question': 'Pouvez-vous expliquer ce concept ?',
        'user_id': 'test_user',
        'user_role': 'student',
        'discipline': 'physics',
        'course_context': 'Cours de mécanique classique, chapitre sur les forces',
        'difficulty_level': 'intermediate'
    }
    
    response = client.post('/api/chat',
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['answer'] != ""

def test_chat_endpoint_teacher_role(client):
    """Test avec rôle enseignant"""
    request_data = {
        'question': 'Comment enseigner les fonctions trigonométriques ?',
        'user_id': 'test_teacher',
        'user_role': 'teacher',
        'discipline': 'mathematics',
        'difficulty_level': 'beginner'
    }
    
    response = client.post('/api/chat',
                          data=json.dumps(request_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'teacher' in data['agent_type']
    assert len(data['suggested_resources']) > 0

def test_swagger_documentation(client):
    """Test que la documentation Swagger est accessible"""
    response = client.get('/docs/')
    assert response.status_code == 200
    
    response = client.get('/apispec.json')
    assert response.status_code == 200