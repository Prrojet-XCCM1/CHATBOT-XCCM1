from typing import List
from app.agents.student_assistant import StudentAssistantAgent
from app.models.message import AgentRequest, AgentResponse

class ScienceAgent(StudentAssistantAgent):
    def __init__(self):
        super().__init__("life_sciences")
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        # Identifier la spécialité scientifique
        specialty = self.identify_science_specialty(request.question)
        
        system_prompt = f"""
        Vous êtes un assistant en {specialty}.
        Règles:
        1. Basez-vous sur des faits scientifiques établis
        2. Mentionnez les sources quand c'est pertinent
        3. Expliquez les processus biologiques/géologiques
        4. Utilisez des schémas descriptifs
        5. Reliez aux enjeux environnementaux actuels
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question en sciences:\n{request.question}\n\nContexte: {request.course_context or 'Général'}"}
        ]
        
        response_text = await self.call_openai(messages, temperature=0.6)
        
        return AgentResponse(
            answer=response_text,
            agent_type="science_specialist",
            confidence_score=0.88,
            follow_up_questions=self.generate_science_follow_ups(specialty)
        )
    
    def identify_science_specialty(self, question: str) -> str:
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["cellule", "adn", "gène", "biologie"]):
            return "biologie"
        elif any(word in question_lower for word in ["roche", "tectonique", "géologie", "volcan"]):
            return "géologie"
        elif any(word in question_lower for word in ["écosystème", "environnement", "écologie"]):
            return "écologie"
        elif any(word in question_lower for word in ["évolution", "darwin", "espèce"]):
            return "évolution"
        
        return "sciences de la vie"
    
    def generate_science_follow_ups(self, specialty: str) -> List[str]:
        return [
            "Voulez-vous voir un schéma explicatif ?",
            "Souhaitez-vous des exemples concrets ?",
            "Voulez-vous connaître les applications pratiques ?",
            "Souhaitez-vous des références bibliographiques ?"
        ]