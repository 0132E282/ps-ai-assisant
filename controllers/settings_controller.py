from fastapi import APIRouter, Request
from core.database import SessionLocal
from models.database_models import SystemSetting
from config import AVAILABLE_MODELS, GEMINI_MODEL

router = APIRouter(prefix="/api", tags=["settings"])

@router.get("/current-prompt")
async def get_current_prompt():
    """
    Lấy system prompt hiện tại
    """
    db = SessionLocal()
    try:
        setting = db.query(SystemSetting).filter(SystemSetting.key == "system_prompt").first()
        return {"prompt": setting.value if setting else ""}
    finally:
        db.close()

@router.post("/update-prompt")
async def update_prompt(request: Request):
    """
    Cập nhật system prompt
    """
    data = await request.json()
    new_prompt = data.get("prompt")
    
    db = SessionLocal()
    try:
        # Lưu vào database
        setting = db.query(SystemSetting).filter(SystemSetting.key == "system_prompt").first()
        if not setting:
            setting = SystemSetting(key="system_prompt", value=new_prompt, description="AI System Prompt")
            db.add(setting)
        else:
            setting.value = new_prompt
        db.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@router.get("/settings")
async def get_settings():
    """
    Lấy tất cả các settings
    """
    db = SessionLocal()
    try:
        settings = db.query(SystemSetting).all()
        return {s.key: s.value for s in settings}
    finally:
        db.close()

@router.post("/settings")
async def update_settings(request: Request):
    """
    Cập nhật settings
    """
    data = await request.json()
    db = SessionLocal()
    try:
        for key, value in data.items():
            setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
            if setting:
                setting.value = str(value)
            else:
                db.add(SystemSetting(key=key, value=str(value), description="User defined setting"))
        db.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
