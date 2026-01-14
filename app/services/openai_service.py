import openai
from app.config import Config
from tenacity import retry, stop_after_attempt, wait_exponential

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_completion(self, messages: list, **kwargs) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get('model', Config.OPENAI_MODEL),
                messages=messages,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', Config.MAX_TOKENS)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI error: {str(e)}")