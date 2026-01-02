# 🎯 Trigger Keywords - Hướng dẫn sử dụng

## Tổng quan

**Trigger Keywords** (từ khóa kích hoạt) cho phép bạn tự động thực thi behaviors khi nói đúng từ khóa, giống như "Hey Siri" hay "OK Google".

---

## 🚀 Cách sử dụng

### 1. Tạo Behavior với Trigger Keyword

#### Qua API:
```bash
curl -X POST http://localhost:8000/api/add-behavior \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mở Chrome",
    "command_type": "open_app",
    "params": {"app_name": "Google Chrome"},
    "icon": "Chrome",
    "trigger_keywords": "mở chrome, khởi động chrome, chrome đi",
    "description": "Mở trình duyệt Google Chrome"
  }'
```

#### Qua Web UI:
1. Vào **Dashboard** → **Behaviors**
2. Click **"+ Thêm hành vi"**
3. Điền thông tin:
   - **Tên:** Mở Chrome
   - **Loại tập lệnh:** Mở ứng dụng
   - **Từ khóa kích hoạt:** `mở chrome, khởi động chrome`
   - **Tham số:** `{"app_name": "Google Chrome"}`

---

## 📝 Các ví dụ Trigger Keywords

### Ví dụ 1: Giới thiệu bản thân
```json
{
  "name": "Giới thiệu bản thân",
  "command_type": "chat",
  "params": {
    "message": "Xin chào! Tôi là PS-Assistant, trợ lý AI thông minh..."
  },
  "trigger_keywords": "giới thiệu, bạn là ai, tên gì",
  "icon": "User"
}
```

**Khi nói:**
- ❌ "giới thiệu" → Kích hoạt! 🎯
- "bạn là ai" → Kích hoạt! 🎯
- "cho tôi giới thiệu về sản phẩm" → Kích hoạt! 🎯 (vì chứa "giới thiệu")

---

### Ví dụ 2: Mở Chrome
```json
{
  "name": "Mở Chrome",
  "command_type": "open_app",
  "params": {"app_name": "Google Chrome"},
  "trigger_keywords": "mở chrome, khởi động chrome, chrome đi",
  "icon": "Chrome"
}
```

**Khi nói:**
- "mở chrome" → Kích hoạt! 🎯
- "hey, mở chrome cho tôi" → Kích hoạt! 🎯
- "làm ơn khởi động chrome" → Kích hoạt! 🎯

---

### Ví dụ 3: Play Music
```json
{
  "name": "Phát nhạc",
  "command_type": "play_music",
  "params": {"query": "lofi music"},
  "trigger_keywords": "phát nhạc, mở nhạc, bật nhạc, play music",
  "icon": "Music"
}
```

**Khi nói:**
- "phát nhạc" → Kích hoạt! 🎯
- "bật nhạc thư giãn" → Kích hoạt! 🎯

---

### Ví dụ 4: Di chuyển Robot
```json
{
  "name": "Tiến lên",
  "command_type": "move",
  "params": {"direction": "forward", "distance": 1},
  "trigger_keywords": "tiến lên, đi thẳng, di chuyển về phía trước",
  "icon": "ArrowUp"
}
```

---

## ⚙️ Cách hoạt động

```
Người dùng nói: "mở chrome cho tôi"
       │
       ├─> Speech-to-Text
       │     └─> Text: "mở chrome cho tôi"
       │
       ├─> TriggerDetector.detect_keyword()
       │     └─> Tìm thấy "mở chrome" match với behavior "Mở Chrome"
       │
       ├─> execute_triggered_behavior()
       │     └─> PCController.execute("open_app", {"app_name": "Google Chrome"})
       │
       └─> Chrome được mở! ✅
```

---

## 🎨 Best Practices

### 1. **Nhiều từ khóa cho 1 behavior**
```json
"trigger_keywords": "mở chrome, khởi động chrome, chrome đi, bật chrome"
```

### 2. **Từ khóa cụ thể**
❌ **Tránh:** `"hành vi"` (quá chung chung)  
✅ **Nên:** `"mở chrome, khởi động trình duyệt"`

### 3. **Không trùng lặp**
Tránh tạo 2 behaviors với cùng trigger keyword:
```json
// Behavior 1
"trigger_keywords": "mở chrome"

// Behavior 2 - TRÁNH!
"trigger_keywords": "mở chrome"  // ❌ Trùng!
```

### 4. **Case insensitive**
Hệ thống tự động chuyển về lowercase:
- "MỞ CHROME" = "mở chrome" = "Mở Chrome"

---

## 🔧 Integration vào main.py

```python
from services.trigger_detector import TriggerDetector

# Khởi tạo
trigger_detector = TriggerDetector()

# Trong main loop
def process_speech(text):
    # Kiểm tra trigger keyword
    triggered = trigger_detector.detect_keyword(text)
    
    if triggered:
        # Thực thi behavior
        result = trigger_detector.execute_triggered_behavior(triggered)
        
        if result.get("message"):
            tts.speak(result["message"])
        
        return  # Không cần gọi AI
    
    # Nếu không match trigger, gọi AI bình thường
    ai_response = ai_service.process_query(text, system_prompt)
    # ...
```

---

## 📊 So sánh: AI vs Trigger

| Tính năng | AI Processing | Trigger Keyword |
|-----------|---------------|-----------------|
| **Tốc độ** | Chậm (gọi API) | Nhanh (~ms) |
| **Chính xác** | Cao (hiểu ngữ cảnh) | Trung bình (khớp từ) |
| **Quota** | Tiêu tốn quota | Không tốn quota |
| **Use case** | Chat, phức tạp | Lệnh đơn giản, lặp lại |

**Khuyến nghị:** Dùng Trigger cho các lệnh thường xuyên để tiết kiệm quota!

---

## 🔄 Reload Behaviors

Sau khi thêm/sửa behavior, reload:

```python
trigger_detector.reload_behaviors()
```

Hoặc restart `main.py`.

---

## 🎯 Use Cases

### 1. **Smart Home Control**
```json
{
  "trigger_keywords": "bật đèn, tắt đèn, mở điều hòa",
  "command_type": "robot",
  "params": {"device": "light", "action": "on"}
}
```

### 2. **Quick Shortcuts**
```json
{
  "trigger_keywords": "mở email, kiểm tra mail",
  "command_type": "open_app",
  "params": {"app_name": "Mail"}
}
```

### 3. **Information Responses**
```json
{
  "trigger_keywords": "mấy giờ rồi, thời gian",
  "command_type": "chat",
  "params": {"message": "Hiện tại là {current_time}"}
}
```

---

## 🐛 Troubleshooting

### Vấn đề: Trigger không hoạt động
**Giải pháp:**
1. Kiểm tra behavior có `is_active = True`
2. Kiểm tra `trigger_keywords` không rỗng
3. Reload behaviors: `trigger_detector.reload_behaviors()`
4. Kiểm tra log: `🎯 Trigger detected:...`

### Vấn đề: Trigger quá nhạy
**Giải pháp:**
- Dùng từ khóa cụ thể hơn
- Tránh từ quá phổ biến như "mở", "bật"

---

**Tạo bởi:** PS-AI Robot Assistant Team  
**Version:** 2.1.0  
**Ngày:** 2026-01-02
