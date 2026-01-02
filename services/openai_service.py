import openai
import json
from config import OPENAI_API_KEY, GPT_MODEL
from interfaces.ai_interface import AIServiceInterface

class OpenAIService(AIServiceInterface):
    """
    Implementation of OpenAI Service.
    """
    def __init__(self):
        try:
            if not OPENAI_API_KEY or "your-api-key" in OPENAI_API_KEY:
                self.client = None
            else:
                self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            print(f"OpenAI Init Error: {e}")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def process_query(self, query: str, system_prompt: str):
        if not self.is_available():
            raise Exception("OpenAI Service not available")

        response = self.client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
