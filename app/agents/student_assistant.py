from typing import List
from app.agents.base_agent import BaseAgent
from app.models.message import AgentRequest, AgentResponse, UserRole
import json

class StudentAssistantAgent(BaseAgent):
    def __init__(self, discipline: str):
        super().__init__("student_assistant", discipline)
        self.prompts = self.load_prompts()
    
    def load_prompts(self):
        with open('app/static/prompts/student_prompts.json', 'r') as f:
            return json.load(f)
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        prompt = self.get_prompt_template(request)
        
        messages = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]}
        ]
        
        # Ajouter l'historique si disponible
        if request.conversation_history:
            for msg in request.conversation_history[-5:]:  # Derniers 5 messages
                messages.insert(-1, {"role": msg.role, "content": msg.content})
        
        response_text = await self.call_openai(messages, temperature=0.7)
        
        return AgentResponse(
            answer=response_text,
            agent_type=self.agent_type,
            confidence_score=0.9,
            follow_up_questions=self.generate_follow_up_questions(request.question)
        )
    
    def get_prompt_template(self, request: AgentRequest) -> dict:
        discipline = request.discipline.value
        difficulty = request.difficulty_level.value
        
        template_key = f"{discipline}_{difficulty}"
        if template_key in self.prompts:
            template = self.prompts[template_key]
        else:
            template = self.prompts["default"]
        
        return {
            "system": template["system"].format(discipline=discipline),
            "user": template["user"].format(
                question=request.question,
                course_context=request.course_context or "Pas de contexte spécifique"
            )
        }
    
    def generate_follow_up_questions(self, question: str) -> List[str]:
        # Logique pour générer des questions de suivi
        return [
            "Voulez-vous un exemple concret ?",
            "Souhaitez-vous des exercices pratiques ?",
            "Voulez-vous approfondir un aspect spécifique ?"
        ]