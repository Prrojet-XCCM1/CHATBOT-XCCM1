from app.agents.student_assistant import StudentAssistantAgent
from app.models.message import AgentRequest, AgentResponse

class ComputerScienceAgent(StudentAssistantAgent):
    def __init__(self):
        super().__init__("computer_science")
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        # Identifier si c'est une question de code
        is_code_question = self.is_code_related(request.question)
        
        system_prompt = """
        Vous êtes un assistant en informatique.
        """
        
        if is_code_question:
            system_prompt += """
            Pour les questions de code:
            1. Fournissez des exemples de code commenté
            2. Expliquez la complexité algorithmique si applicable
            3. Proposez des bonnes pratiques
            4. Mentionnez les cas limites
            """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question en informatique:\n{request.question}"}
        ]
        
        response_text = await self.call_openai(messages, temperature=0.7)
        
        response = AgentResponse(
            answer=response_text,
            agent_type="cs_specialist",
            confidence_score=0.90
        )
        
        if is_code_question:
            response.suggested_resources = [
                "Documentation officielle",
                "Exemples de code sur GitHub",
                "Tutoriels interactifs",
                "Exercices de programmation"
            ]
        
        return response
    
    def is_code_related(self, question: str) -> bool:
        code_keywords = ["code", "programme", "algorithme", "fonction", "classe", 
                        "python", "java", "javascript", "c++", "boucle", "variable"]
        return any(keyword in question.lower() for keyword in code_keywords)