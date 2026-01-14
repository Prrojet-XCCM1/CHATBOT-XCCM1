from app.agents.student_assistant import StudentAssistantAgent
from app.models.message import AgentRequest, AgentResponse

class PhysicsAgent(StudentAssistantAgent):
    def __init__(self):
        super().__init__("physics")
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        # Surcharger pour ajouter des spécificités physiques
        system_prompt = """
        Vous êtes un assistant en physique. 
        Règles importantes:
        1. Toujours mentionner les unités de mesure
        2. Expliquer les lois physiques applicables
        3. Proposer des expériences mentales
        4. Relier aux phénomènes du quotidien
        5. Utiliser le formalisme mathématique approprié
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question de physique:\n{request.question}\n\nContexte du cours: {request.course_context or 'Général'}\nNiveau: {request.difficulty_level.value}"}
        ]
        
        response_text = await self.call_openai(messages, temperature=0.6)
        
        return AgentResponse(
            answer=response_text,
            agent_type="physics_specialist",
            confidence_score=0.92,
            suggested_resources=self.suggest_physics_resources(request.question)
        )
    
    def suggest_physics_resources(self, question: str) -> List[str]:
        resources = [
            "Simulations PhET (University of Colorado)",
            "Vidéos de démonstrations expérimentales",
            "Fiches de formules essentielles",
            "Problèmes types avec solutions"
        ]
        return resources