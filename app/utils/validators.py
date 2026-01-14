from pydantic import BaseModel, validator, ValidationError
import re
from typing import Optional
from app.models.base import Discipline, UserRole, DifficultyLevel

class RequestValidator:
    @staticmethod
    def validate_question(question: str) -> tuple[bool, str]:
        """Valider une question"""
        if not question or len(question.strip()) == 0:
            return False, "La question ne peut pas être vide"
        
        if len(question) > 1000:
            return False, "La question est trop longue (max 1000 caractères)"
        
        # Vérifier les caractères dangereux
        if re.search(r'[<>{}[\]\\]', question):
            return False, "La question contient des caractères non autorisés"
        
        return True, ""
    
    @staticmethod
    def validate_discipline(discipline: str) -> tuple[bool, str]:
        """Valider une discipline"""
        try:
            Discipline(discipline)
            return True, ""
        except ValueError:
            valid_disciplines = [d.value for d in Discipline]
            return False, f"Discipline invalide. Valides: {', '.join(valid_disciplines)}"
    
    @staticmethod
    def validate_user_role(role: str) -> tuple[bool, str]:
        """Valider un rôle utilisateur"""
        try:
            UserRole(role)
            return True, ""
        except ValueError:
            valid_roles = [r.value for r in UserRole]
            return False, f"Rôle invalide. Valides: {', '.join(valid_roles)}"
    
    @staticmethod
    def validate_difficulty(difficulty: str) -> tuple[bool, str]:
        """Valider un niveau de difficulté"""
        try:
            DifficultyLevel(difficulty)
            return True, ""
        except ValueError:
            valid_levels = [d.value for d in DifficultyLevel]
            return False, f"Niveau invalide. Valides: {', '.join(valid_levels)}"

class InputSanitizer:
    @staticmethod
    def sanitize_text(text: str) -> str:
        """Nettoyer le texte d'entrée"""
        if not text:
            return ""
        
        # Supprimer les balises HTML/XML
        text = re.sub(r'<[^>]+>', '', text)
        
        # Échapper les caractères spéciaux
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Limiter la longueur
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        return text.strip()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Nettoyer un nom de fichier"""
        # Remplacer les caractères dangereux
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        return filename[:255]