from datetime import datetime
from typing import List, Dict, Any
import json

class ResponseFormatter:
    @staticmethod
    def format_agent_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formater une réponse d'agent pour l'API"""
        return {
            "answer": response_data.get("answer", ""),
            "metadata": {
                "agent_type": response_data.get("agent_type", "unknown"),
                "confidence": response_data.get("confidence_score", 0.0),
                "timestamp": datetime.now().isoformat(),
                "sources": response_data.get("sources", []),
                "suggestions": response_data.get("suggested_resources", []),
                "follow_up": response_data.get("follow_up_questions", [])
            }
        }
    
    @staticmethod
    def format_error(message: str, error_code: str = None) -> Dict[str, Any]:
        """Formater une erreur"""
        return {
            "error": {
                "message": message,
                "code": error_code or "INTERNAL_ERROR",
                "timestamp": datetime.now().isoformat()
            }
        }
    
    @staticmethod
    def format_conversation_history(messages: List[Dict]) -> str:
        """Formater l'historique de conversation pour les prompts"""
        formatted = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 2000) -> str:
        """Tronquer un texte sans couper les mots"""
        if len(text) <= max_length:
            return text
        
        # Tronquer au dernier espace avant max_length
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + "..."

class JSONFormatter:
    @staticmethod
    def pretty_print(data: Any) -> str:
        """Formatter JSON pour l'affichage"""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    @staticmethod
    def minify(data: Any) -> str:
        """Minifier JSON"""
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)