from typing import List
from app.agents.student_assistant import StudentAssistantAgent
from app.models.message import AgentRequest, AgentResponse

class DatabaseAIAgent(StudentAssistantAgent):
    def __init__(self):
        super().__init__("databases")
        self.disciplines = ["databases", "artificial_intelligence"]
    
    async def generate_response(self, request: AgentRequest) -> AgentResponse:
        # Déterminer si c'est BDD ou IA
        is_database = self.is_database_question(request.question)
        discipline = "bases de données" if is_database else "intelligence artificielle"
        
        system_prompt = f"""
        Vous êtes un expert en {discipline}.
        """
        
        if is_database:
            system_prompt += """
            Pour les questions de bases de données:
            1. Fournissez des exemples SQL si pertinent
            2. Expliquez les concepts de normalisation
            3. Comparez les différents types de bases de données
            4. Parlez des bonnes pratiques de modélisation
            """
        else:
            system_prompt += """
            Pour les questions d'IA:
            1. Distinguez clairement AI, ML, Deep Learning
            2. Expliquez les concepts avec des analogies
            3. Mentionnez les limitations et éthique
            4. Parlez des applications concrètes
            """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Question en {discipline}:\n{request.question}"}
        ]
        
        response_text = await self.call_openai(messages, temperature=0.7)
        
        return AgentResponse(
            answer=response_text,
            agent_type=f"{'database' if is_database else 'ai'}_specialist",
            confidence_score=0.91,
            suggested_resources=self.suggest_resources(is_database)
        )
    
    def is_database_question(self, question: str) -> bool:
        db_keywords = ["sql", "base de données", "table", "requête", "jointure", 
                      "normalisation", "postgresql", "mysql", "mongodb"]
        ai_keywords = ["machine learning", "deep learning", "neurone", "apprentissage",
                      "chatbot", "vision", "traitement langage"]
        
        question_lower = question.lower()
        db_count = sum(1 for word in db_keywords if word in question_lower)
        ai_count = sum(1 for word in ai_keywords if word in question_lower)
        
        return db_count >= ai_count
    
    def suggest_resources(self, is_database: bool) -> List[str]:
        if is_database:
            return [
                "Documentation SQL complète",
                "Tutoriels de modélisation",
                "Exercices de requêtes",
                "Comparaison SGBD"
            ]
        else:
            return [
                "Cours de Machine Learning",
                "Papers de recherche clés",
                "Librairies populaires (TensorFlow, PyTorch)",
                "Projets open source"
            ]