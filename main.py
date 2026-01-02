from services.stt_service import STTManager
from services.tts_service import TTSManager
from services.reasoning_service import ReasoningEngine
from controllers.robot_controller import RobotController
from controllers.pc_controller import PCController
from core.database import init_db, SessionLocal
from models.database_models import Chat

def main():
    # Khởi tạo database
    init_db()
    
    # Khởi tạo các module
    stt = STTManager()
    tts = TTSManager()
    reasoning = ReasoningEngine()
    robot = RobotController()
    pc = PCController()

    tts.speak("Hệ thống trợ lý ảo đã sẵn sàng. Tôi có thể giúp gì cho bạn?")

    while True:
        try:
            # 1. Nghe từ Micro
            query = stt.listen_and_transcribe()
            
            if not query:
                continue
                
            print(f"Người dùng nói: {query}")
            
            if query.lower() in ["thoát", "exit", "quit", "tạm biệt"]:
                tts.speak("Tạm biệt bạn!")
                break

            # 2. Suy luận ý định từ văn bản
            intent = reasoning.process_query(query)
            print(f"DEBUG: Intent detected -> {intent}")

            # 3. Thực thi lệnh
            cmd_type = intent.get("type")
            params = intent.get("params", {})
            message = intent.get("message", "Đã rõ.")

            # Phản hồi bằng giọng nói trước/sau khi thực hiện
            tts.speak(message)

            if cmd_type in ["move", "stop"]:
                success = robot.execute(cmd_type, params)
            elif cmd_type in ["open_app"]:
                success = pc.execute(cmd_type, params)
            else:
                success = True

            # 4. Lưu vào Database
            db = SessionLocal()
            try:
                # Lưu tin nhắn của User
                user_message = Chat(
                    message=query,
                    message_type='user',
                    ai_intent=None,
                    command_type=None,
                    execution_status=True
                )
                db.add(user_message)
                
                # Lưu phản hồi của Assistant
                assistant_message = Chat(
                    message=message,
                    message_type='assistant',
                    ai_intent=intent,
                    command_type=cmd_type,
                    execution_status=success
                )
                db.add(assistant_message)
                db.commit()
            except Exception as db_e:
                print(f"Lỗi lưu DB: {db_e}")
            finally:
                db.close()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Lỗi hệ thống: {e}")

if __name__ == "__main__":
    main()
