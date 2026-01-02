"""
Trigger Keyword Detection Service
Phát hiện từ khóa kích hoạt từ giọng nói
"""
from core.database import SessionLocal
from models.database_models import RobotBehavior

class TriggerDetector:
    """
    Phát hiện trigger keywords trong text
    """
    def __init__(self):
        self.behaviors_cache = []
        self.reload_behaviors()
    
    def reload_behaviors(self):
        """
        Load lại behaviors từ database
        """
        db = SessionLocal()
        try:
            behaviors = db.query(RobotBehavior).filter(
                RobotBehavior.is_active == True,
                RobotBehavior.trigger_keywords != None,
                RobotBehavior.trigger_keywords != ""
            ).all()
            
            self.behaviors_cache = []
            for b in behaviors:
                keywords = [k.strip().lower() for k in (b.trigger_keywords or "").split(",")]
                self.behaviors_cache.append({
                    "id": b.id,
                    "name": b.name,
                    "keywords": keywords,
                    "command_type": b.command_type,
                    "params": b.params
                })
            
            print(f"✓ Loaded {len(self.behaviors_cache)} behaviors with triggers")
        finally:
            db.close()
    
    def detect_keyword(self, text):
        """
        Phát hiện keyword trong text
        Args:
            text (str): Text cần check
        Returns:
            dict: Behavior được trigger, hoặc None
        """
        if not text:
            return None
        
        text_lower = text.lower().strip()
        
        for behavior in self.behaviors_cache:
            for keyword in behavior["keywords"]:
                if keyword and keyword in text_lower:
                    print(f"🎯 Trigger detected: '{keyword}' -> {behavior['name']}")
                    return behavior
        
        return None
    
    def execute_triggered_behavior(self, behavior):
        """
        Thực thi behavior được trigger
        """
        from controllers.robot_controller import RobotController
        from controllers.pc_controller import PCController
        
        command_type = behavior["command_type"]
        params = behavior["params"] or {}
        
        print(f"⚡ Executing triggered behavior: {behavior['name']}")
        
        success = False
        
        if command_type in ["move", "stop"]:
            success = RobotController().execute(command_type, params)
        elif command_type in ["open_app", "play_music"]:
            success = PCController().execute(command_type, params)
        elif command_type == "chat":
            # Nếu là chat, trả về message để TTS đọc
            message = params.get("message", f"Đã kích hoạt: {behavior['name']}")
            print(f"💬 Chat response: {message}")
            return {"success": True, "message": message}
        
        return {"success": success, "message": f"{behavior['name']} executed"}
