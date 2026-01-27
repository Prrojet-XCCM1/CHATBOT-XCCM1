from app.agents.base_agent import BaseAgent
from app.models.message import AgentRequest, AgentResponse
from app.agents.student_assistant import StudentAssistantAgent
from app.agents.teacher_assistant import TeacherAssistantAgent
from app.config import Config

class AgentCoordinator:
    def __init__(self):
        self.agents = {}
        self.init_agents()
    
    def init_agents(self):
        # Initialiser les agents par discipline
        for discipline in Config.SUPPORTED_DISCIPLINES:
            self.agents[f"student_{discipline}"] = StudentAssistantAgent(discipline)
            self.agents[f"teacher_{discipline}"] = TeacherAssistantAgent(discipline)
    
    def get_agent(self, user_role: str, discipline: str) -> BaseAgent:
        # Tenter de récupérer l'agent spécifique
        agent_key = f"{user_role}_{discipline}"
        if agent_key in self.agents:
            return self.agents[agent_key]
        
        # Repli sur le général pour le rôle demandé
        role_general = f"{user_role}_general"
        if role_general in self.agents:
            return self.agents[role_general]
            
        # Repli ultime sur student_general si rien d'autre ne match
        return self.agents.get("student_general")
    
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        # Récupérer l'agent approprié
        agent = self.get_agent(request.user_role.value, request.discipline.value)
        
        # Traiter la requête
        response = await agent.generate_response(request)
        
        return response
    
    def route_to_specialist(self, request: AgentRequest) -> str:
        # Logique de routage vers un agent spécialisé si nécessaire
        question_lower = request.question.lower()
        
        if "exercice" in question_lower or "problème" in question_lower:
            return "problem_solving_agent"
        elif "définition" in question_lower or "qu'est-ce que" in question_lower:
            return "definition_agent"
        elif "exemple" in question_lower:
            return "example_agent"
        
        return "general_agent"