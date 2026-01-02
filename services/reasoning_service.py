from services.service_factory import AIServiceFactory
from config import GPT_MODEL

class ReasoningEngine:
    def __init__(self, provider=None):
        self.ai_service = AIServiceFactory.get_service(provider)

    def get_system_prompt(self):
        from core.database import SessionLocal
        from models.database_models import SystemSetting
        db = SessionLocal()
        try:
            setting = db.query(SystemSetting).filter(SystemSetting.key == "system_prompt").first()
            if setting:
                return setting.value
        except:
            pass
        finally:
            db.close()
        
        return """
        Bạn là bộ não của một Robot trợ lý thông minh. 
        Nhiệm vụ của bạn là nhận diện ý định từ giọng nói và chuyển thành lệnh JSON.
        Các lệnh hỗ trợ: move, stop, open_app, search_web.
        Trả về định dạng JSON: {"type": "command_type", "params": {...}, "message": "phản hồi bằng lời nói"}
        """

    def process_query(self, query):
        current_prompt = self.get_system_prompt()
        
        if not self.ai_service.is_available():
            print(f"AI Service not available. Using Mock Reasoning...")
            return self.mock_process(query)

        try:
            return self.ai_service.process_query(query, current_prompt)
        except Exception as e:
            print(f"AI Service Error: {e}. Using Mock Reasoning...")
            return self.mock_process(query)

    def mock_process(self, query):
        query = query.lower()
        if "đi thẳng" in query:
            return {"type": "move", "params": {"direction": "forward", "distance": 2}, "message": "Đang đi thẳng 2 mét."}
        elif "dừng" in query:
            return {"type": "stop", "params": {}, "message": "Đã dừng robot gấp."}
        elif "mở" in query and "chrome" in query:
            return {"type": "open_app", "params": {"app_name": "Google Chrome"}, "message": "Đang mở trình duyệt Chrome cho bạn."}
        else:
            return {"type": "chat", "params": {}, "message": "Xin lỗi, tôi đang offline."}
