from app.agents.base_agent import BaseAgent
from app.models.message import AgentRequest, AgentResponse
import json

class TeacherAssistantAgent(BaseAgent):
    def __init__(self, discipline: str):
        super().__init__("teacher_assistant", discipline)
        self.prompts = self.load_prompts()
    
    def load_prompts(self):
        with open('app/static/prompts/teacher_prompts.json', 'r') as f:
            return json.load(f)
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        prompt = self.get_prompt_template(request)
        
        messages = [
            {"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user"]}
        ]
        
        response_text = await self.call_openai(messages, temperature=0.8)
        
        return AgentResponse(
            answer=response_text,
            agent_type=self.agent_type,
            confidence_score=0.85,
            suggested_resources=self.generate_teaching_resources(request.question)
        )
    
    def get_prompt_template(self, request: AgentRequest) -> dict:
        template = self.prompts.get(request.discipline.value, self.prompts["default"])
        
        return {
            "system": template["system"],
            "user": template["user"].format(
                question=request.question,
                difficulty=request.difficulty_level.value
            )
        }
    
    def generate_teaching_resources(self, question: str) -> List[str]:
        # Logique pour suggérer des ressources pédagogiques
        return [
            "Exercices types",
            "Schémas explicatifs",
            "Références bibliographiques"
        ]