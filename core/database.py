from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.database_models import Base

# Create Engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Khởi tạo database và tạo các bảng nếu chưa tồn tại.
    """
    global engine, SessionLocal
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        if "mysql" in str(e).lower() or "connection refused" in str(e).lower():
            print(f"⚠️ Lỗi kết nối MySQL: {e}")
            print("🔄 Đang chuyển sang SQLite dự phòng để ứng dụng có thể chạy...")
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            fallback_url = "sqlite:///./robot_assistant.db"
            engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
        else:
            raise e
    
    # Thêm cấu hình mặc định nếu chưa có
    from models.database_models import SystemSetting, RobotBehavior
    db = SessionLocal()
    try:
        # Prompt mặc định
        existing_prompt = db.query(SystemSetting).filter(SystemSetting.key == "system_prompt").first()
        if not existing_prompt:
            db.add(SystemSetting(
                key="system_prompt",
                value="Bạn là một trợ lý Robot thông minh, lễ phép và có tính cách hài hước. Nhiệm vụ của bạn là hỗ trợ điều khiển robot và PC qua lệnh JSON.",
                description="Tính cách và hành động mặc định của Robot"
            ))
            print("✅ Default system prompt initialized.")

        # Agent name & Theme
        default_settings = [
            ("agent_name", "PS-Assistant", "Tên hiển thị của trợ lý"),
            ("theme_color", "#6366f1", "Màu chủ đạo của giao diện"),
            ("gemini_model", "models/gemini-2.5-flash", "Model Gemini sử dụng"),
            ("bot_eye_color", "#ffffff", "Màu mắt của Bot"),
            ("bot_body_color", "#4f46e5", "Màu thân của Bot")
        ]
        for key, val, desc in default_settings:
            if not db.query(SystemSetting).filter(SystemSetting.key == key).first():
                db.add(SystemSetting(key=key, value=val, description=desc))
                print(f"✅ Setting '{key}' initialized.")

        # Hành vi mặc định
        if db.query(RobotBehavior).count() == 0:
            default_behaviors = [
                RobotBehavior(name="Mở Chrome", command_type="open_app", params={"app_name": "Google Chrome"}, icon="Chrome"),
                RobotBehavior(name="Mở Facebook", command_type="open_app", params={"app_name": "Facebook"}, icon="Facebook"),
                RobotBehavior(name="Đi thẳng", command_type="move", params={"direction": "forward", "distance": 1}, icon="ArrowUp"),
                RobotBehavior(name="Dừng lại", command_type="stop", params={}, icon="Square")
            ]
            db.add_all(default_behaviors)
            print("✅ Default behaviors initialized.")
            
        db.commit()
    except Exception as e:
        print(f"❌ Error initializing default settings: {e}")
    finally:
        db.close()
        
    print("🚀 Database Initialized.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
