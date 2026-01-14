from flask import Blueprint, request, jsonify
from app.agents.coordinator import AgentCoordinator
from app.models.message import AgentRequest, AgentResponse, UserRole, Discipline, DifficultyLevel
from pydantic import ValidationError
import logging

api_bp = Blueprint('api', __name__)
coordinator = AgentCoordinator()
logger = logging.getLogger(__name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "education-multiagent"})

@api_bp.route('/chat', methods=['POST'])
async def chat():
    try:
        data = request.get_json()
        
        # Validation des données
        agent_request = AgentRequest(
            question=data['question'],
            user_id=data.get('user_id', 'anonymous'),
            user_role=UserRole(data.get('user_role', 'student')),
            discipline=Discipline(data.get('discipline', 'general')),
            course_context=data.get('course_context'),
            difficulty_level=DifficultyLevel(data.get('difficulty_level', 'intermediate')),
            conversation_history=data.get('conversation_history', [])
        )
        
        # Traitement par le coordinateur
        response = await coordinator.process_request(agent_request)
        
        return jsonify(response.dict())
        
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/disciplines', methods=['GET'])
def get_disciplines():
    from app.config import Config
    return jsonify({"disciplines": Config.SUPPORTED_DISCIPLINES})

@api_bp.route('/agents', methods=['GET'])
def get_agents():
    agents_list = list(coordinator.agents.keys())
    return jsonify({"agents": agents_list})