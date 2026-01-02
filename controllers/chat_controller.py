from fastapi import APIRouter, Request
from core.database import SessionLocal
from models.database_models import Chat

router = APIRouter(prefix="/api", tags=["chat"])

@router.get("/chat")
async def get_chat():
    """
    Lấy lịch sử chat (user + assistant messages)
    """
    db = SessionLocal()
    try:
        chats = db.query(Chat).order_by(Chat.timestamp.asc()).limit(50).all()
        return [{
            "id": chat.id,
            "message": chat.message,
            "type": chat.message_type,
            "timestamp": chat.timestamp.isoformat(),
            "command_type": chat.command_type,X
            "ai_intent": chat.ai_intent
        } for chat in chats]
    finally:
        db.close()

@router.post("/chat")
async def send_message(request: Request):
    """
    Gửi tin nhắn mới (từ web interface)
    """
    data = await request.json()
    message = data.get("message")
    
    if not message:
        return {"status": "error", "message": "Message is required"}
    
    db = SessionLocal()
    try:
        # Lưu tin nhắn user
        user_message = Chat(
            message=message,
            message_type='user',
            ai_intent=None,
            command_type=None,
            execution_status=True
        )
        db.add(user_message)
        db.commit()
        
        # Gọi AI service để xử lý
        from services.service_factory import AIServiceFactory
        from models.database_models import SystemSetting
        
        # Lấy system prompt từ database
        setting = db.query(SystemSetting).filter(SystemSetting.key == "system_prompt").first()
        system_prompt = setting.value if setting else "Bạn là trợ lý AI thông minh."
        
        # Xử lý với AI
        ai_service = AIServiceFactory.get_service()
        try:
            response = ai_service.process_query(message, system_prompt)
            
            # Lưu phản hồi AI
            ai_message = Chat(
                message=response.get("message", "Xin lỗi, tôi không hiểu."),
                message_type='assistant',
                ai_intent=response.get("type"),
                command_type=response.get("type"),
                execution_status=True
            )
            db.add(ai_message)
            db.commit()
            
            return {
                "status": "success", 
                "message": "Message sent",
                "response": response.get("message"),
                "ai_response": response
            }
        except Exception as ai_error:
            print(f"AI Error: {ai_error}")
            import traceback
            traceback.print_exc()
            # Lưu error message
            error_message = Chat(
                message=f"Xin lỗi, tôi đang offline. Lỗi: {str(ai_error)}",
                message_type='assistant',
                ai_intent=None,
                command_type=None,
                execution_status=False
            )
            db.add(error_message)
            db.commit()
            
            return {
                "status": "error", 
                "message": str(ai_error),
                "response": f"Xin lỗi, tôi đang offline. Lỗi: {str(ai_error)}"
            }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

@router.delete("/chat/{chat_id}")
async def delete_chat(chat_id: int):
    """
    Xóa một tin nhắn chat
    """
    db = SessionLocal()
    try:
        chat = db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            db.delete(chat)
            db.commit()
            return {"status": "success"}
        return {"status": "error", "message": "Chat not found"}
    finally:
        db.close()

@router.delete("/chat")
async def clear_chat():
    """
    Xóa toàn bộ lịch sử chat
    """
    db = SessionLocal()
    try:
        db.query(Chat).delete()
        db.commit()
        return {"status": "success", "message": "All chat history cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
