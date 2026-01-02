from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.database import init_db
from controllers.chat_controller import router as chat_router
from controllers.behavior_controller import router as behavior_router
from controllers.settings_controller import router as settings_router
from controllers.frontend_controller import router as frontend_router
from controllers.robot_controller import router as robot_router
import uvicorn

# Initialize database
init_db()

app = FastAPI()

# Enable CORS for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(behavior_router)
app.include_router(settings_router)
app.include_router(robot_router)
app.include_router(frontend_router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    print("Dashboard is running at http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
