from interfaces.ai_interface import AIServiceInterface
import os
import json

class ClaudeService(AIServiceInterface):
    """
    Implementation of Anthropic Claude Service.
    """
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        # Initialize Anthropic client here if library is installed
        # self.client = anthropic.Anthropic(api_key=self.api_key)
        self.client = None 

    def is_available(self) -> bool:
        return self.client is not None and self.api_key is not None

    def process_query(self, query: str, system_prompt: str):
        if not self.is_available():
            # Mocking response since key is missing
            return {
                "type": "chat",
                "params": {},
                "message": "Claude AI chưa được cấu hình. Vui lòng thêm CLAUDE_API_KEY vào .env"
            }
        
        # Actual implementation would go here
        return {"message": "Claude Processing..."}
