import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
GPT_MODEL = "gpt-4o-mini"

# Gemini Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AVAILABLE_MODELS = {
    "gemini-2.5 pro": "models/gemini-2.5-pro",
    "Gemini 2.5 Flash": "models/gemini-2.5-flash",
    "Gemini 3 Pro Preview": "gemini-3-pro-preview",
    "Gemini 2.0 Flash": "gemini-2.0-flash-exp",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro",
}
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

# Speech Config
LANGUAGE = "vi" # default language

# Robot Config (Simulation for now)
ROBOT_ENABLED = True
PC_CONTROL_ENABLED = True

# Database Config
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "robot_assistant")

if os.getenv("DB_NAME"):
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    DATABASE_URL = "sqlite:///./robot_assistant.db"
