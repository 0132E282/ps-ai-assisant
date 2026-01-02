from fastapi import APIRouter
from config import GEMINI_MODEL, AVAILABLE_MODELS
from services.gemini_service import GeminiService

router = APIRouter(prefix="/api")

@router.get("/models")
async def get_available_models():
    """
    Lấy danh sách các AI models có thể sử dụng từ Google Gemini API
    """
    try:
        gemini_service = GeminiService()
        if gemini_service.is_available():
            models = gemini_service.get_available_models()
            return {
                "models": models,
                "default_model": GEMINI_MODEL,
                "source": "gemini_api"
            }
        else:
            return {
                "models": AVAILABLE_MODELS,
                "default_model": GEMINI_MODEL,
                "source": "config_fallback"
            }
    except Exception as e:
        print(f"Error in get_available_models: {e}")
        return {
            "models": AVAILABLE_MODELS,
            "default_model": GEMINI_MODEL,
            "source": "config_fallback"
        }

class RobotController:
    def __init__(self):
        print("Robot Controller Initialized (Simulation Mode)")

    def execute(self, command_type, params):
        if command_type == "move":
            direction = params.get("direction")
            distance = params.get("distance", 0)
            print(f"[ROBOT] Moving {direction} for {distance} meters.")
            return True
        elif command_type == "stop":
            print("[ROBOT] Emergency Stop!")
            return True
        return False
