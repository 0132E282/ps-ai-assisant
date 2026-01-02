import os
from dotenv import load_dotenv
from services.openai_service import OpenAIService
from services.claude_service import ClaudeService
from services.gemini_service import GeminiService
from services.llama_service import LLaMAService

load_dotenv()

class AIServiceFactory:
    """
    Factory to manage and switch between different AI providers.
    """
    @staticmethod
    def get_service(provider_name=None):
        if provider_name is None:
            provider_name = os.getenv("AI_PROVIDER", "gemini").lower()

        if provider_name == "openai":
            return OpenAIService()
        elif provider_name == "claude":
            return ClaudeService()
        elif provider_name == "gemini":
            return GeminiService()
        elif provider_name == "llama":
            return LLaMAService()
        else:
            print(f"Provider {provider_name} not supported. Falling back to Gemini.")
            return GeminiService()
