import pytest
import asyncio
from app.agents.student_assistant import StudentAssistantAgent
from app.agents.coordinator import AgentCoordinator
from app.models.message import AgentRequest, UserRole, Discipline, DifficultyLevel

@pytest.fixture
def coordinator():
    return AgentCoordinator()

@pytest.fixture
def student_request():
    return AgentRequest(
        question="Qu'est-ce que la photosynthèse ?",
        user_id="test_student",
        user_role=UserRole.STUDENT,
        discipline=Discipline.LIFE_SCIENCES,
        difficulty_level=DifficultyLevel.BEGINNER
    )

@pytest.fixture
def teacher_request():
    return AgentRequest(
        question="Comment expliquer les dérivées à des débutants ?",
        user_id="test_teacher",
        user_role=UserRole.TEACHER,
        discipline=Discipline.MATHEMATICS,
        difficulty_level=DifficultyLevel.BEGINNER
    )

@pytest.mark.asyncio
async def test_student_agent_response(coordinator, student_request):
    """Test de la réponse d'un agent étudiant"""
    response = await coordinator.process_request(student_request)
    
    assert response is not None
    assert response.answer != ""
    assert response.agent_type == "student_assistant"
    assert 0 <= response.confidence_score <= 1

@pytest.mark.asyncio
async def test_teacher_agent_response(coordinator, teacher_request):
    """Test de la réponse d'un agent enseignant"""
    response = await coordinator.process_request(teacher_request)
    
    assert response is not None
    assert response.answer != ""
    assert "teacher" in response.agent_type
    assert len(response.suggested_resources) > 0

@pytest.mark.asyncio
async def test_agent_coordinator_routing(coordinator):
    """Test du routage du coordinateur"""
    # Test avec différentes disciplines
    disciplines = [Discipline.MATHEMATICS, Discipline.PHYSICS, Discipline.COMPUTER_SCIENCE]
    
    for discipline in disciplines:
        request = AgentRequest(
            question="Test question",
            user_id="test_user",
            user_role=UserRole.STUDENT,
            discipline=discipline
        )
        
        response = await coordinator.process_request(request)
        assert response is not None
        assert response.agent_type != ""

def test_agent_initialization():
    """Test de l'initialisation des agents"""
    coordinator = AgentCoordinator()
    
    # Vérifier que les agents sont bien initialisés
    assert len(coordinator.agents) > 0
    
    # Vérifier les agents par discipline
    expected_agents = ["student_mathematics", "teacher_mathematics"]
    for agent_key in expected_agents:
        assert agent_key in coordinator.agents

@pytest.mark.asyncio
async def test_conversation_history(coordinator):
    """Test avec historique de conversation"""
    request = AgentRequest(
        question="Pouvez-vous répéter ?",
        user_id="test_user",
        user_role=UserRole.STUDENT,
        discipline=Discipline.MATHEMATICS,
        conversation_history=[
            {"role": "user", "content": "Qu'est-ce que 2+2 ?", "timestamp": "2024-01-01"},
            {"role": "assistant", "content": "2+2=4", "timestamp": "2024-01-01"}
        ]
    )
    
    response = await coordinator.process_request(request)
    assert response is not None
    assert response.answer != ""