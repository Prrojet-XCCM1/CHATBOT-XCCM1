from flasgger import Swagger
from flasgger.utils import swag_from

def setup_swagger(app):
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "urls": [
            {
                "name": "Local server",
                "url": "http://localhost:5000/apispec.json"
            },
            {
                "name": "Render (chatbotxccm1)",
                "url": "https://chatbotxccm1.onrender.com/apispec.json"
            }
        ],
       
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/",
        "title": "Education Multi-Agent API",
        "uiversion": 3,
        "swagger_ui_parameters": {
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": 1,
            "docExpansion": "none",
            "tryItOutEnabled": True,
            "requestSnippetsEnabled": True,
            "displayRequestDuration": True,
            "persistAuthorization": True,
            "syntaxHighlight": {
                "activate": True,
                "theme": "monokai"
            },
            "tryItOutEnabled": True
        }
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Education Multi-Agent API",
            "description": "API pour le système multi-agent éducatif",
            "version": "1.0.0"
        },
         "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Serveur de développement local"
        },
        {
            "url": "https://chatbotxccm1.onrender.com",
            "description": "Serveur de production (Render)"
        },
       
    ],
        "host": "localhost:5000",
        "basePath": "/api",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Health",
                "description": "Endpoints de santé"
            },
            {
                "name": "Chat",
                "description": "Chat avec les assistants"
            },
            {
                "name": "Information",
                "description": "Informations système"
            },
            {
                "name": "Testing",
                "description": "Tests et débogage"
            }
        ],
        "definitions": {
            "AgentRequest": {
                "type": "object",
                "required": ["question", "user_role", "discipline"],
                "properties": {
                    "question": {
                        "type": "string",
                        "example": "Quelle est la formule de l'aire d'un cercle ?"
                    },
                    "user_id": {
                        "type": "string",
                        "example": "student_123"
                    },
                    "user_role": {
                        "type": "string",
                        "enum": ["student", "teacher", "admin"],
                        "example": "student"
                    },
                    "discipline": {
                        "type": "string",
                        "enum": ["mathematics", "physics", "computer_science", 
                                "life_sciences", "databases", "artificial_intelligence", "general"],
                        "example": "mathematics"
                    },
                    "course_context": {
                        "type": "string",
                        "example": "Cours de géométrie de base"
                    },
                    "difficulty_level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "example": "beginner"
                    }
                }
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)