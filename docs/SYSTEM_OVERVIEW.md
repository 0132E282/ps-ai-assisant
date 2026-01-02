# 🤖 PS-AI Robot Assistant - System Overview

## 📋 Tổng quan hệ thống

**PS-AI Robot Assistant** là một hệ thống trợ lý ảo thông minh, hỗ trợ điều khiển robot và PC thông qua giọng nói và text. Hệ thống có khả năng chuyển đổi giữa nhiều AI providers (Gemini, ChatGPT, Claude, LLaMA) và cung cấp giao diện web dashboard để quản lý.

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                          │
├─────────────────────────────────────────────────────────────┤
│  • Web Dashboard (React + Vite)                             │
│  • Voice Interface (Speech-to-Text)                          │
│  • Terminal CLI                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB DASHBOARD API                         │
│                   (FastAPI Backend)                          │
├─────────────────────────────────────────────────────────────┤
│  Controllers:                                                │
│  ├─ chat_controller.py      (Chat & AI Processing)          │
│  ├─ settings_controller.py  (System Settings)               │
│  ├─ behavior_controller.py  (Behavior Management)           │
│  ├─ robot_controller.py     (Robot Control + Models API)    │
│  ├─ frontend_controller.py  (Static Files Serving)          │
│  └─ pc_controller.py        (PC Control)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  AI Services:                                                │
│  ├─ gemini_service.py       (Google Gemini)                 │
│  ├─ openai_service.py       (ChatGPT)                       │
│  ├─ claude_service.py       (Anthropic Claude)              │
│  └─ llama_service.py        (LLaMA - Ollama/Groq) ⭐ NEW    │
│                                                              │
│  Other Services:                                             │
│  ├─ stt_service.py          (Speech-to-Text)                │
│  ├─ tts_service.py          (Text-to-Speech)                │
│  └─ service_factory.py      (AI Provider Selector)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
├─────────────────────────────────────────────────────────────┤
│  • SQLite/MySQL Database                                    │
│  • Models: Chat, SystemSetting, Behavior                    │
│  • ORM: SQLAlchemy                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTION LAYER                             │
├─────────────────────────────────────────────────────────────┤
│  • Robot Controller (Physical Robot Commands)               │
│  • PC Controller (System Commands - macOS/Windows/Linux)    │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Công việc đã hoàn thành

### 1. **Web Dashboard Refactoring** 🔄
- **Trước:** Tất cả API endpoints trong 1 file `web_dashboard.py` (159 dòng)
- **Sau:** Tách thành 5 controllers riêng biệt (37 dòng main file)
  - `chat_controller.py` - Xử lý chat và AI
  - `settings_controller.py` - Quản lý cấu hình
  - `behavior_controller.py` - Quản lý behaviors
  - `robot_controller.py` - Điều khiển robot + API models
  - `frontend_controller.py` - Serve static files

**Lợi ích:**
- ✅ Code dễ maintain và scale
- ✅ Separation of concerns
- ✅ Dễ dàng thêm features mới

---

### 2. **Dynamic AI Model Selection** 🤖
- **API mới:** `GET /api/models`
- **Source:** Lấy trực tiếp từ Google Gemini API
- **Kết quả:** 25+ models thay vì 6 models hardcoded

**Quy trình:**
```
Frontend Settings.jsx
       │
       ├─> GET /api/models
       │
       ▼
Robot Controller
       │
       ├─> GeminiService.get_available_models()
       │
       ▼
Google Gemini API
       │
       └─> Trả về danh sách models động
```

**Models hiện có:**
- Gemini 2.5 Flash/Pro
- Gemini 3 Pro/Flash Preview
- Gemini 2.0 Flash variants
- Gemini Robotics-ER
- Gemini Computer Use Preview
- Và 20+ models khác...

---

### 3. **Multi-AI Provider Support** 🌐 ⭐ NEW

**Frontend UI - AI Provider Selector:**
```
┌─────────────────────────────────────────┐
│  AI Provider:    [Dropdown]             │
│   🤖 Google Gemini                      │
│   💬 ChatGPT (OpenAI)                   │
│   🧠 Claude (Anthropic)                 │
│   🦙 LLaMA (Local/Groq)                 │
└─────────────────────────────────────────┘
```

**Backend Services:**

| Provider | Service File | API Type | Status |
|----------|-------------|----------|--------|
| **Gemini** | `gemini_service.py` | Cloud (Google) | ✅ Active |
| **ChatGPT** | `openai_service.py` | Cloud (OpenAI) | ✅ Ready |
| **Claude** | `claude_service.py` | Cloud (Anthropic) | ✅ Ready |
| **LLaMA** | `llama_service.py` | Local/Cloud (Ollama/Groq) | ⭐ **NEW** |

---

### 4. **Chat API với AI Integration** 💬

**Endpoint:** `POST /api/chat`

**Flow:**
```
User Message (Web/Voice)
       │
       ├─> Save to Database (user message)
       │
       ├─> Get System Prompt from DB
       │
       ├─> AIServiceFactory.get_service()
       │      └─> Chọn provider (gemini/openai/claude/llama)
       │
       ├─> AI Processing
       │      └─> Trả về JSON: {type, message, params}
       │
       ├─> Save AI Response to Database
       │
       └─> Return Response to User
```

**Response Format:**
```json
{
  "status": "success",
  "message": "Message sent",
  "response": "Xin chào! Tôi là PS-Assistant...",
  "ai_response": {
    "type": "chat",
    "message": "Xin chào! Tôi là PS-Assistant...",
    "params": {}
  }
}
```

---

### 5. **LLaMA Service Integration** 🦙 ⭐ NEW

**Hỗ trợ 2 modes:**

#### Mode 1: Local (Ollama)
```bash
# Cài đặt Ollama
brew install ollama

# Download model
ollama pull llama3.2

# Start Ollama server
ollama serve  # Mặc định: http://localhost:11434
```

**Config (.env):**
```env
AI_PROVIDER=llama
LLAMA_PROVIDER=ollama
LLAMA_MODEL=llama3.2
OLLAMA_URL=http://localhost:11434
```

#### Mode 2: Cloud (Groq)
**Config (.env):**
```env
AI_PROVIDER=llama
LLAMA_PROVIDER=groq
LLAMA_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your_groq_api_key_here
```

**Lợi ích:**
- ✅ **Không giới hạn quota** (local)
- ✅ **Privacy** (data không ra khỏi máy)
- ✅ **Tốc độ cao** với Groq Cloud
- ✅ **Fallback option** khi Gemini bị quota

---

## 🗃️ Database Schema

### Table: `chat`
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `message` | Text | Nội dung tin nhắn |
| `message_type` | String | 'user' hoặc 'assistant' |
| `ai_intent` | String | Loại command (chat/robot/pc) |
| `command_type` | String | Chi tiết command |
| `execution_status` | Boolean | Trạng thái thực thi |
| `timestamp` | DateTime | Thời gian |

### Table: `system_settings`
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `key` | String | Tên setting (vd: "system_prompt") |
| `value` | Text | Giá trị |
| `description` | String | Mô tả |

### Table: `behaviors`
| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary Key |
| `name` | String | Tên behavior |
| `description` | Text | Mô tả |
| `is_active` | Boolean | Kích hoạt hay không |

---

## 🔧 API Endpoints

### Chat Endpoints
- `GET /api/chat` - Lấy lịch sử chat
- `POST /api/chat` - Gửi tin nhắn mới (có AI processing)
- `DELETE /api/chat/{id}` - Xóa 1 tin nhắn
- `DELETE /api/chat` - Xóa toàn bộ lịch sử

### Settings Endpoints
- `GET /api/settings` - Lấy tất cả settings
- `POST /api/settings` - Cập nhật settings
- `POST /api/update-prompt` - Cập nhật system prompt
- `GET /api/models` ⭐ **NEW** - Lấy danh sách AI models (Gemini)

### Behavior Endpoints
- `GET /api/behaviors` - Lấy danh sách behaviors
- `POST /api/behaviors` - Tạo behavior mới
- `PUT /api/behaviors/{id}` - Cập nhật behavior
- `DELETE /api/behaviors/{id}` - Xóa behavior

### Frontend
- `GET /` - Serve React app
- `GET /static/*` - Serve static files

---

## 🚀 Cách chạy hệ thống

### Backend
```bash
cd ps-ai-robot-assistant
source venv/bin/activate
python web_dashboard.py
# Server: http://localhost:8000
```

### Frontend
```bash
cd frontend
pnpm install
pnpm dev
# Dev server: http://localhost:5173
```

### Voice Interface
```bash
cd ps-ai-robot-assistant
source venv/bin/activate
python main.py
# Chờ "Đang nghe..." rồi nói
```

---

## 🎯 Tính năng chính

### ✅ Đã hoàn thành
1. ✅ **Web Dashboard** - Giao diện quản lý đẹp mắt
2. ✅ **Multi-AI Support** - Gemini, ChatGPT, Claude, LLaMA
3. ✅ **Dynamic Model Selection** - Lấy models từ API
4. ✅ **Chat with AI** - Xử lý tin nhắn qua AI service
5. ✅ **Voice Control** - Speech-to-Text (Google + Gemini)
6. ✅ **Database Integration** - Lưu chat history và settings
7. ✅ **Robot Control** - Simulation mode (sẵn sàng kết nối hardware)
8. ✅ **PC Control** - Mở apps, play music, điều khiển hệ thống

### 🚧 Đang phát triển
- ⏳ Settings UI cho OpenAI/Claude API keys
- ⏳ LLaMA model selector
- ⏳ Behavior execution trong chat
- ⏳ Robot hardware integration

---

## ⚠️ Vấn đề hiện tại & Giải pháp

### Vấn đề: Gemini Quota Exceeded
```
Error: 429 RESOURCE_EXHAUSTED
Model: gemini-3-pro-image
Quota: 20 requests/day (Free tier)
```

### Giải pháp:

#### ✅ Giải pháp 1: Đổi sang model khác
Vào Settings UI → chọn model khác:
- `Gemini 2.5 Flash` (quota cao hơn)
- `Gemini 2.0 Flash 001` (ổn định)

#### ✅ Giải pháp 2: Dùng LLaMA (Local)
```bash
# Install Ollama
brew install ollama

# Download model
ollama pull llama3.2

# Start Ollama
ollama serve

# Update .env
AI_PROVIDER=llama
LLAMA_PROVIDER=ollama
LLAMA_MODEL=llama3.2
```

#### ✅ Giải pháp 3: Dùng ChatGPT
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

---

## 📊 Thống kê Code

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| `web_dashboard.py` | 159 lines | 37 lines | **-77%** |
| Controllers | 1 file | 5 files | **+400%** organization |
| AI Providers | 3 | 4 | **+33%** |
| Available Models | 6 (hardcoded) | 25+ (dynamic) | **+300%** |
| API Endpoints | 12 | 13 | +1 (`/api/models`) |

---

## 🔮 Next Steps

### Ngắn hạn (1-2 tuần)
1. ✅ Thêm UI cho API keys (OpenAI, Claude, Groq)
2. ✅ Model selector cho từng AI provider
3. ✅ Behavior execution trong chat
4. ✅ Error handling improvements

### Trung hạn (1 tháng)
1. Robot hardware integration
2. Camera vision integration
3. Advanced voice commands
4. Multi-user support

### Dài hạn (3-6 tháng)
1. Mobile app (React Native)
2. Cloud deployment
3. AI model training
4. Plugin system

---

## 📝 Ghi chú quan trọng

### Environment Variables (.env)
```env
# AI Provider Selection
AI_PROVIDER=gemini  # gemini | openai | claude | llama

# Gemini
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=models/gemini-2.5-flash

# OpenAI
OPENAI_API_KEY=your_openai_key

# Claude
CLAUDE_API_KEY=your_claude_key

# LLaMA
LLAMA_PROVIDER=ollama  # ollama | groq
LLAMA_MODEL=llama3.2
OLLAMA_URL=http://localhost:11434
GROQ_API_KEY=your_groq_key

# Database
DB_TYPE=sqlite  # sqlite | mysql
DATABASE_URL=sqlite:///./bot_system.db

# TTS
TTS_ENGINE=pygame  # pygame | macos
```

---

## 📚 Tài liệu liên quan

- [Web Dashboard Refactoring](./WEB_DASHBOARD_REFACTORING.md)
- [API Models Endpoint](./API_MODELS_ENDPOINT.md)
- [Quota Troubleshooting](./QUOTA_TROUBLESHOOTING.md)

---

**Tạo bởi:** PS-AI Robot Assistant Team  
**Ngày cập nhật:** 2026-01-02  
**Version:** 2.0.0
