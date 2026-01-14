from app.agents.student_assistant import StudentAssistantAgent
from app.models.message import AgentRequest, AgentResponse
import json

class MathAgent(StudentAssistantAgent):
    def __init__(self):
        super().__init__("mathematics")
        self.specialized_prompts = self.load_math_prompts()
    
    def load_math_prompts(self):
        return {
            "algebra": {
                "system": "Vous êtes un expert en algèbre. Expliquez les concepts algébriques avec des exemples numériques.",
                "user": "Question algébrique: {question}\n\nContexte: {course_context}\n\nExpliquez étape par étape:"
            },
            "geometry": {
                "system": "Vous êtes un expert en géométrie. Utilisez des descriptions visuelles et des schémas mentaux.",
                "user": "Question géométrique: {question}\n\nContexte: {course_context}\n\nFournissez une explication visuelle:"
            },
            "calculus": {
                "system": "Vous êtes un expert en calcul différentiel et intégral. Montrez les dérivations complètes.",
                "user": "Question de calcul: {question}\n\nContexte: {course_context}\n\nDémontrez avec rigueur mathématique:"
            }
        }
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        # Identifier le sous-domaine mathématique
        subdomain = self.identify_math_subdomain(request.question)
        
        # Utiliser le prompt spécialisé si disponible
        if subdomain in self.specialized_prompts:
            prompt = self.specialized_prompts[subdomain]
            messages = [
                {"role": "system", "content": prompt["system"]},
                {"role": "user", "content": prompt["user"].format(
                    question=request.question,
                    course_context=request.course_context or ""
                )}
            ]
        else:
            # Utiliser la méthode parent
            return await super().generate_response(request)
        
        response_text = await self.call_openai(messages, temperature=0.5)
        
        return AgentResponse(
            answer=response_text,
            agent_type="math_specialist",
            confidence_score=0.95,
            follow_up_questions=self.generate_math_follow_ups(subdomain)
        )
    
    def identify_math_subdomain(self, question: str) -> str:
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["équation", "variable", "polynôme", "algèbre"]):
            return "algebra"
        elif any(word in question_lower for word in ["géométrie", "angle", "triangle", "cercle", "aire"]):
            return "geometry"
        elif any(word in question_lower for word in ["dérivée", "intégrale", "limite", "calcul"]):
            return "calculus"
        elif any(word in question_lower for word in ["probabilité", "statistique", "moyenne"]):
            return "statistics"
        
        return "general"
    
    def generate_math_follow_ups(self, subdomain: str) -> List[str]:
        follow_ups = {
            "algebra": [
                "Voulez-vous voir un autre exemple similaire ?",
                "Souhaitez-vous des exercices d'application ?",
                "Voulez-vous comprendre la démonstration formelle ?"
            ],
            "geometry": [
                "Voulez-vous une représentation graphique ?",
                "Souhaitez-vous des exercices de construction ?",
                "Voulez-vous voir des applications concrètes ?"
            ],
            "calculus": [
                "Voulez-vous voir le calcul étape par étape ?",
                "Souhaitez-vous comprendre l'interprétation graphique ?",
                "Voulez-vous des exercices pratiques ?"
            ]
        }
        return follow_ups.get(subdomain, [])