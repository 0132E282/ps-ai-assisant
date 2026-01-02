from google import genai
from google.genai import types
import json
import os
from config import GEMINI_API_KEY, GEMINI_MODEL
from interfaces.ai_interface import AIServiceInterface

class GeminiService(AIServiceInterface):
    """
    Implementation of Google Gemini AI Service using the new google-genai SDK.
    """
    def __init__(self):
        try:
            if not GEMINI_API_KEY:
                self.client = None
                print("Gemini API Key missing.")
            else:
                self.client = genai.Client(api_key=GEMINI_API_KEY)
                
                # Try to fetch model from DB
                from core.database import SessionLocal
                from models.database_models import SystemSetting
                db = SessionLocal()
                try:
                    setting = db.query(SystemSetting).filter(SystemSetting.key == "gemini_model").first()
                    self.model_id = setting.value if setting else GEMINI_MODEL
                except:
                    self.model_id = GEMINI_MODEL
                finally:
                    db.close()
                    
                print(f"Gemini Service initialized with model: {self.model_id}")
        except Exception as e:
            print(f"Gemini Init Error: {e}")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def process_query(self, query: str, system_prompt: str):
        if not self.is_available():
            raise Exception("Gemini Service not available")

        # Combining system prompt and user query
        full_prompt = f"{system_prompt}\n\nUser query: {query}"
        
        try:
            # Using the new SDK's generate_content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type='application/json',
                )
            )
            
            if not response.text:
                raise Exception("Empty response from Gemini")
                
            text = response.text.strip()
            # Basic JSON extraction in case of markdown formatting (though mime_type should handle it)
            if text.startswith("```json"):
                text = text.split("```json")[1].split("```")[0].strip()
            elif text.startswith("```"):
                text = text.split("```")[1].split("```")[0].strip()
                
            return json.loads(text)
        except Exception as e:
            print(f"Gemini (google-genai) Error: {e}")
            raise e

    def get_available_models(self):
        """
        Lấy danh sách các models có sẵn từ Google Gemini API
        """
        if not self.is_available():
            print("Gemini client not available, using config fallback")
            from config import AVAILABLE_MODELS
            return AVAILABLE_MODELS
            
        try:
            # Use the new SDK to list models
            models_response = self.client.models.list()
            
            available_models = {}
            
            # Convert to list if it's an iterator
            models_list = list(models_response) if models_response else []
            
            for model in models_list:
                # Get model attributes
                name = model.name if hasattr(model, 'name') else str(model)
                display_name = model.display_name if hasattr(model, 'display_name') else name
                supported_actions = model.supported_actions if hasattr(model, 'supported_actions') else []
                
                # Filter only models that support generateContent
                if 'generateContent' in supported_actions:
                    # Only include main Gemini models
                    if name.startswith("models/gemini-") and not name.endswith("-tuning"):
                        # Add tags for experimental/latest versions
                        if "exp" in name.lower():
                            display_name += " (Experimental)"
                        elif "latest" in name.lower():
                            display_name += " (Latest)"
                        
                        available_models[display_name] = name
            
            if available_models:
                print(f"Successfully fetched {len(available_models)} models from Gemini API")
                return available_models
            else:
                print("No models found from Gemini API, using config fallback")
                from config import AVAILABLE_MODELS
                return AVAILABLE_MODELS
                
        except Exception as e:
            print(f"Error fetching models from Gemini: {e}")
            # Return fallback from config
            from config import AVAILABLE_MODELS
            return AVAILABLE_MODELS
