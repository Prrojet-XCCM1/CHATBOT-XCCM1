import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_object = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_object, ensure_ascii=False)

def setup_logger(name: str, log_file: str = "logs/education_assistant.log") -> logging.Logger:
    """Configurer un logger"""
    
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Éviter les logs multiples
    if logger.handlers:
        return logger
    
    # Créer le dossier logs si nécessaire
    import os
    os.makedirs("logs", exist_ok=True)
    
    # Handler fichier avec rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter())
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger principal
logger = setup_logger("education_assistant")

# Loggers spécialisés
agent_logger = setup_logger("education_assistant.agents")
api_logger = setup_logger("education_assistant.api")
service_logger = setup_logger("education_assistant.services")

def log_request(request_data: dict, user_id: str = None):
    """Logger une requête"""
    api_logger.info("Request received", extra={
        "user_id": user_id,
        "endpoint": request_data.get("endpoint"),
        "method": request_data.get("method"),
        "data": request_data.get("data")
    })

def log_agent_response(agent_type: str, question: str, response_time: float):
    """Logger une réponse d'agent"""
    agent_logger.info("Agent response", extra={
        "agent_type": agent_type,
        "question_length": len(question),
        "response_time_ms": response_time * 1000
    })