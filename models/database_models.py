from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now)
    message = Column(String(1000), nullable=False)  # Nội dung tin nhắn
    message_type = Column(String(20), nullable=False)  # 'user' hoặc 'assistant'
    ai_intent = Column(JSON)  # Lưu toàn bộ JSON response từ AI (chỉ cho assistant)
    command_type = Column(String(50))  # Loại lệnh (nếu có)
    execution_status = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Chat(id={self.id}, type='{self.message_type}', message='{self.message[:30]}...')>"

class SystemSetting(Base):
    __tablename__ = "system_settings"

    key = Column(String(50), primary_key=True)
    value = Column(String(1000))
    description = Column(String(255))

class RobotBehavior(Base):
    __tablename__ = "robot_behaviors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    command_type = Column(String(50), nullable=False)
    params = Column(JSON)
    icon = Column(String(50), default="Zap")
    is_active = Column(Boolean, default=True)
    trigger_keywords = Column(String(500))  # Từ khóa kích hoạt (cách nhau bởi dấu ,)
    description = Column(String(500))  # Mô tả hành vi
