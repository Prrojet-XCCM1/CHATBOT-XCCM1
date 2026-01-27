from flask import Blueprint, request, jsonify
from app.agents.coordinator import AgentCoordinator
from app.models.message import AgentRequest, AgentResponse, UserRole, Discipline, DifficultyLevel
from pydantic import ValidationError
import logging
from flasgger import swag_from
import asyncio
import functools
import traceback

from asgiref.sync import async_to_sync

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)
logger.info("Initializing AgentCoordinator...")
coordinator = AgentCoordinator()
logger.info(f"AgentCoordinator initialized with {len(coordinator.agents)} agents")

def async_handler(f):
    """Gérer les fonctions asynchrones de manière compatible avec Flask sync"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return async_to_sync(f)(*args, **kwargs)
    return wrapper

@api_bp.route('/health', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'Vérification de santé du service',
    'description': 'Vérifie que le service est opérationnel',
    'responses': {
        200: {
            'description': 'Service en bonne santé',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'healthy'},
                    'service': {'type': 'string', 'example': 'education-multiagent'},
                    'timestamp': {'type': 'string', 'example': '2024-01-01T10:00:00Z'},
                    'agents_count': {'type': 'integer', 'example': 14}
                }
            }
        }
    }
})
def health_check():
    logger.info("Health check endpoint called")
    return jsonify({
        "status": "healthy", 
        "service": "education-multiagent",
        "timestamp": "2024-01-01T10:00:00Z",
        "agents_count": len(coordinator.agents)
    })

@api_bp.route('/chat', methods=['POST'])
@async_handler
@swag_from({
    'tags': ['Chat'],
    'summary': 'Chat avec l\'assistant IA',
    'description': 'Posez une question à l\'assistant IA éducatif',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['question', 'user_role', 'discipline'],
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': 'Quelle est la formule de l\'aire d\'un cercle ?'
                    },
                    'user_id': {
                        'type': 'string',
                        'example': 'student_123'
                    },
                    'user_role': {
                        'type': 'string',
                        'enum': ['student', 'teacher', 'admin'],
                        'example': 'student'
                    },
                    'discipline': {
                        'type': 'string',
                        'enum': ['mathematics', 'physics', 'computer_science', 
                                'life_sciences', 'databases', 'artificial_intelligence', 'general'],
                        'example': 'mathematics'
                    },
                    'course_context': {
                        'type': 'string',
                        'example': 'Cours de géométrie de base'
                    },
                    'difficulty_level': {
                        'type': 'string',
                        'enum': ['beginner', 'intermediate', 'advanced'],
                        'example': 'beginner'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Réponse de l\'assistant',
            'schema': {
                'type': 'object',
                'properties': {
                    'answer': {'type': 'string'},
                    'agent_type': {'type': 'string'},
                    'confidence_score': {'type': 'number'},
                    'sources': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'suggested_resources': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'follow_up_questions': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        400: {
            'description': 'Requête invalide'
        },
        500: {
            'description': 'Erreur interne du serveur'
        }
    }
})
async def chat():
    """
    Endpoint principal pour interagir avec les assistants IA éducatifs.
    """
    try:
        logger.info("=== CHAT ENDPOINT CALLED ===")
        
        # Obtenir les données de manière plus robuste
        if request.content_type != 'application/json':
            logger.warning(f"Invalid content type: {request.content_type}")
            return jsonify({"error": {"message": "Content-Type must be application/json", "code": "VALIDATION_ERROR"}}), 400
        
        data = request.get_json()
        logger.info(f"Raw data: {data}")
        
        # Si Swagger envoie des données vides, utiliser les valeurs par défaut
        if data is None:
            logger.warning("Data is None, using example data")
            data = {
                "question": "Quelle est la capitale de la France ?",
                "user_role": "student",
                "discipline": "general"
            }
        
        logger.info(f"Request data: {data}")
        
        if 'question' not in data or not data.get('question', '').strip():
            logger.warning("Missing or empty 'question' field in request")
            return jsonify({"error": {"message": "Missing or empty 'question' field", "code": "VALIDATION_ERROR"}}), 400
        
        # Validation des données
        try:
            agent_request = AgentRequest(
                question=data['question'],
                user_id=data.get('user_id', 'anonymous'),
                user_role=UserRole(data['user_role']) if 'user_role' in data else UserRole.STUDENT,
                discipline=Discipline(data['discipline']) if 'discipline' in data else Discipline.GENERAL,
                course_context=data.get('course_context', ''),
                difficulty_level=DifficultyLevel(data.get('difficulty_level', 'intermediate')),
                conversation_history=data.get('conversation_history', [])
            )
            
            # Vérifier que les champs requis étaient présents pour le test
            if 'user_role' not in data or 'discipline' not in data:
                logger.warning("Missing required fields: user_role or discipline")
                return jsonify({"error": {"message": "Missing user_role or discipline", "code": "VALIDATION_ERROR"}}), 400
                
            logger.info(f"AgentRequest created successfully")
        except ValueError as e:
            logger.error(f"Validation error creating AgentRequest: {str(e)}")
            return jsonify({"error": {"message": f"Validation error: {str(e)}", "code": "VALIDATION_ERROR"}}), 400
        
        # Traitement par le coordinateur
        logger.info("Processing request through coordinator...")
        try:
            response = await coordinator.process_request(agent_request)
            logger.info(f"Response generated successfully by agent: {response.agent_type}")
            
            return jsonify(response.model_dump())
            
        except Exception as e:
            logger.error(f"Error in coordinator.process_request: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": {"message": f"Agent processing error: {str(e)}", "code": "AGENT_ERROR"}}), 500
        
    except ValidationError as e:
        logger.error(f"Pydantic Validation error: {str(e)}")
        return jsonify({"error": {"message": str(e), "code": "VALIDATION_ERROR"}}), 400
    
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": {"message": f"Internal server error: {str(e)}", "code": "INTERNAL_ERROR"}}), 500
@api_bp.route('/test-simple', methods=['POST'])
@swag_from({
    'tags': ['Testing'],
    'summary': 'Test simple',
    'description': 'Endpoint de test simple sans async',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['question'],
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': 'Bonjour, ça va ?'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Réponse de test',
            'schema': {
                'type': 'object',
                'properties': {
                    'answer': {'type': 'string'},
                    'agent_type': {'type': 'string'},
                    'confidence_score': {'type': 'number'}
                }
            }
        }
    }
})
def test_simple():
    """Endpoint de test simple sans async"""
    logger.info("Test simple endpoint called")
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Missing question"}), 400
        
        # Retourner une réponse simple pour tester
        return jsonify({
            "answer": f"Test response for: {data['question']}",
            "agent_type": "test_agent",
            "confidence_score": 0.9,
            "sources": [],
            "suggested_resources": [],
            "follow_up_questions": ["Did this work?"]
        })
    except Exception as e:
        logger.error(f"Test simple error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/test-coordinator', methods=['GET'])
@swag_from({
    'tags': ['Testing'],
    'summary': 'Test du coordinateur',
    'description': 'Teste le coordinateur d\'agents',
    'responses': {
        200: {
            'description': 'Statut du coordinateur',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'agents_count': {'type': 'integer'},
                    'agents': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def test_coordinator():
    """Test du coordinateur d'agents"""
    logger.info("Testing coordinator...")
    try:
        return jsonify({
            "status": "coordinator_ok",
            "agents_count": len(coordinator.agents),
            "agents": list(coordinator.agents.keys())
        })
    except Exception as e:
        logger.error(f"Coordinator test error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@api_bp.route('/disciplines', methods=['GET'])
@swag_from({
    'tags': ['Information'],
    'summary': 'Liste des disciplines',
    'description': 'Récupère la liste des disciplines supportées',
    'responses': {
        200: {
            'description': 'Liste des disciplines',
            'schema': {
                'type': 'object',
                'properties': {
                    'disciplines': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_disciplines():
    try:
        from app.config import Config
        disciplines = Config.SUPPORTED_DISCIPLINES
        logger.info(f"Returning disciplines: {disciplines}")
        return jsonify({"disciplines": disciplines})
    except Exception as e:
        logger.error(f"Error getting disciplines: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/agents', methods=['GET'])
@swag_from({
    'tags': ['Information'],
    'summary': 'Liste des agents',
    'description': 'Récupère la liste des agents disponibles',
    'responses': {
        200: {
            'description': 'Liste des agents',
            'schema': {
                'type': 'object',
                'properties': {
                    'agents': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'count': {'type': 'integer'}
                }
            }
        }
    }
})
def get_agents():
    try:
        agents_list = list(coordinator.agents.keys())
        logger.info(f"Returning {len(agents_list)} agents")
        return jsonify({
            "agents": agents_list,
            "count": len(agents_list)
        })
    except Exception as e:
        logger.error(f"Error getting agents: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api_bp.route('/models', methods=['GET'])
@swag_from({
    'tags': ['Information'],
    'summary': 'Liste des modèles',
    'description': 'Récupère la liste des modèles LLM disponibles',
    'responses': {
        200: {
            'description': 'Liste des modèles',
            'schema': {
                'type': 'object',
                'properties': {
                    'models': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'current_model': {'type': 'string'},
                    'provider': {'type': 'string'}
                }
            }
        }
    }
})
def get_available_models():
    try:
        models = [
            'meta-llama/llama-3.1-70b-instruct',
            'mistralai/mistral-7b-instruct',
            'google/gemini-pro',
            'openai/gpt-4',
            'anthropic/claude-3-haiku'
        ]
        
        return jsonify({
            "models": models,
            "current_model": 'meta-llama/llama-3.1-70b-instruct',
            "provider": "openrouter"
        })
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return jsonify({"error": "Could not retrieve models"}), 500

@api_bp.route('/status', methods=['GET'])
@swag_from({
    'tags': ['Health'],
    'summary': 'Statut système',
    'description': 'Récupère des informations détaillées sur l\'état du système',
    'responses': {
        200: {
            'description': 'Statut du système',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'agents_ready': {'type': 'integer'},
                    'redis_connected': {'type': 'boolean'},
                    'llm_provider': {'type': 'string'},
                    'version': {'type': 'string'},
                    'timestamp': {'type': 'string'}
                }
            }
        }
    }
})
def system_status():
    try:
        return jsonify({
            "status": "operational",
            "agents_ready": len(coordinator.agents),
            "redis_connected": False,
            "llm_provider": "openrouter",
            "version": "1.0.0",
            "timestamp": "2024-01-01T10:00:00Z"
        })
    except Exception as e:
        logger.error(f"Error in status endpoint: {str(e)}")
        return jsonify({
            "status": "degraded",
            "error": str(e),
            "timestamp": "2024-01-01T10:00:00Z"
        }), 500