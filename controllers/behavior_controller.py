from fastapi import APIRouter, Request
from core.database import SessionLocal
from models.database_models import RobotBehavior

router = APIRouter(prefix="/api", tags=["behavior"])

@router.get("/behaviors")
async def get_behaviors():
    """
    Lấy danh sách các behavior đang active
    """
    db = SessionLocal()
    try:
        behaviors = db.query(RobotBehavior).filter(RobotBehavior.is_active == True).all()
        return behaviors
    finally:
        db.close()

@router.post("/execute-behavior/{behavior_id}")
async def execute_behavior(behavior_id: int):
    """
    Thực thi một behavior cụ thể
    """
    db = SessionLocal()
    try:
        behavior = db.query(RobotBehavior).filter(RobotBehavior.id == behavior_id).first()
        if not behavior:
            return {"status": "error", "message": "Behavior not found"}
        
        # Integration with controllers
        from controllers.robot_controller import RobotController
        from controllers.pc_controller import PCController
        
        success = False
        if behavior.command_type in ["move", "stop"]:
            success = RobotController().execute(behavior.command_type, behavior.params)
        elif behavior.command_type == "open_app":
            success = PCController().execute(behavior.command_type, behavior.params)
            
        return {"status": "success" if success else "failed"}
    finally:
        db.close()

@router.post("/add-behavior")
async def add_behavior(request: Request):
    """
    Thêm behavior mới với trigger keywords
    """
    data = await request.json()
    db = SessionLocal()
    try:
        new_b = RobotBehavior(
            name=data.get("name"),
            command_type=data.get("command_type"),
            params=data.get("params"),
            icon=data.get("icon", "Zap"),
            trigger_keywords=data.get("trigger_keywords", ""),  # Từ khóa trigger
            description=data.get("description", "")  # Mô tả
        )
        db.add(new_b)
        db.commit()
        return {"status": "success", "id": new_b.id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@router.delete("/behavior/{behavior_id}")
async def delete_behavior(behavior_id: int):
    """
    Xóa một behavior
    """
    db = SessionLocal()
    try:
        behavior = db.query(RobotBehavior).filter(RobotBehavior.id == behavior_id).first()
        if behavior:
            db.delete(behavior)
            db.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
