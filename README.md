# 🤖 PS-AI Robot Assistant

Trợ lý AI thông minh hỗ trợ điều khiển robot và PC qua giọng nói, với khả năng chuyển đổi linh hoạt giữa các AI providers.

## ✨ Tính năng

- 🎯 **Trigger Keywords** - Kích hoạt behaviors bằng từ khóa
- 🗣️ **Voice Control** - Điều khiển bằng giọng nói (tiếng Việt)
- 🤖 **Multi-AI Support** - Gemini, ChatGPT, Claude, LLaMA
- 💻 **Web Dashboard** - Giao diện quản lý hiện đại
- 📊 **Dynamic Model Selection** - Chọn AI model theo thời gian thực
- 🔊 **Enhanced TTS** - Giọng nói tự nhiên, rõ ràng

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd ps-ai-robot-assistant
```

### 2. Setup Backend (Python)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
nano .env
```

### 3. Setup Frontend (React)
```bash
cd frontend
pnpm install  # or npm install
pnpm dev      # Start dev server
```

### 4. Run Application
```bash
# Terminal 1: Backend
source venv/bin/activate
python web_dashboard.py

# Terminal 2: Frontend
cd frontend
pnpm dev

# Terminal 3: Voice Interface (optional)
source venv/bin/activate
python main.py
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Required: Choose AI provider
AI_PROVIDER=gemini  # or openai, claude, llama

# Google Gemini (Recommended for free tier)
GEMINI_API_KEY=your_api_key_here

# Optional: Other providers
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_claude_key
GROQ_API_KEY=your_groq_key
```

### Get API Keys:
- **Gemini**: https://ai.google.dev/
- **OpenAI**: https://platform.openai.com/
- **Claude**: https://console.anthropic.com/
- **Groq (LLaMA)**: https://console.groq.com/

---

## 📖 Documentation

- [📊 System Overview](docs/SYSTEM_OVERVIEW.md)
- [🎯 Trigger Keywords Guide](docs/TRIGGER_KEYWORDS.md)
- [🆕 Update Log](docs/UPDATE_LOG.md)
- [🔧 API Endpoints](docs/API_MODELS_ENDPOINT.md)
- [⚠️ Quota Troubleshooting](docs/QUOTA_TROUBLESHOOTING.md)

---

## 🎯 Usage Examples

### Voice Commands
```
"Mở Chrome"           → Opens Google Chrome
"Giới thiệu"          → AI introduces itself
"Phát nhạc"           → Plays music
"Di chuyển về phía trước" → Robot moves forward
```

### Web Dashboard
```
http://localhost:5173  → Frontend
http://localhost:8000  → Backend API
```

### Add Behavior with Trigger
```bash
curl -X POST http://localhost:8000/api/add-behavior \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mở Chrome",
    "trigger_keywords": "mở chrome, chrome đi",
    "command_type": "open_app",
    "params": {"app_name": "Google Chrome"}
  }'
```

---

## 🏗️ Project Structure

```
ps-ai-robot-assistant/
├── controllers/          # API endpoints
│   ├── chat_controller.py
│   ├── behavior_controller.py
│   ├── settings_controller.py
│   └── robot_controller.py
├── services/            # Business logic
│   ├── gemini_service.py
│   ├── llama_service.py
│   ├── tts_service.py
│   └── trigger_detector.py
├── frontend/            # React app
│   └── src/
│       └── pages/
│           ├── Admin.jsx
│           └── Settings.jsx
├── docs/               # Documentation
├── .env.example        # Environment template
└── .gitignore         # Git ignore rules
```

---

## 🛠️ Tech Stack

**Backend:**
- Python 3.9+
- FastAPI
- SQLAlchemy
- Google Gemini API

**Frontend:**
- React + Vite
- TailwindCSS
- Framer Motion

**AI Providers:**
- Google Gemini
- OpenAI GPT
- Anthropic Claude
- LLaMA (Ollama/Groq)

---

## 🔒 Security

⚠️ **IMPORTANT**: Never commit `.env` file to Git!

- ✅ `.env` is in `.gitignore`
- ✅ Use `.env.example` as template
- ✅ Keep API keys secret
- ✅ Rotate keys if exposed

---

## 🐛 Troubleshooting

### Gemini Quota Exceeded
```bash
# Switch to LLaMA (local, no quota)
AI_PROVIDER=llama
LLAMA_PROVIDER=ollama

# Or use different Gemini model
GEMINI_MODEL=models/gemini-2.5-flash
```

### Frontend Not Loading
```bash
# Clear Vite cache
rm -rf frontend/node_modules/.vite
cd frontend && pnpm dev
```

### Voice Commands Not Working
```bash
# Check microphone permissions
# Try manual input mode instead
```

---

## 📝 License

MIT License - See LICENSE file

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📧 Support

- Documentation: `docs/`
- Issues: GitHub Issues
- Email: support@example.com

---

**Made with ❤️ by PS-AI Team**  
Version: 2.1.0 | Last Updated: 2026-01-02
