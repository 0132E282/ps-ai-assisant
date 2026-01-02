# AI Robot Assistant - Hướng dẫn xử lý lỗi Quota

## Vấn đề: Gemini API hết quota

Khi bạn thấy lỗi:
```
quotaMetric: 'generativelanguage.googleapis.com/generate_content_free_tier_requests'
```

Điều này có nghĩa là bạn đã vượt quá giới hạn miễn phí của Gemini API.

## Giải pháp

### 1. Đã áp dụng: Chuyển sang Gemini 2.5 Flash
✅ File `.env` đã được cập nhật để sử dụng `models/gemini-2.5-flash` thay vì `gemini-2.0-flash-exp`

Model này có quota cao hơn và ổn định hơn.

### 2. Đã áp dụng: Ưu tiên Google Web Speech cho STT
✅ File `services/stt_service.py` đã được cập nhật:
- **Ưu tiên 1**: Google Web Speech (miễn phí, không giới hạn, ổn định)
- **Ưu tiên 2**: Gemini STT (chỉ khi Google Web Speech thất bại)
- **Ưu tiên 3**: Nhập tay (nếu cả 2 đều thất bại)

### 3. Chuyển sang OpenAI (nếu cần)

Nếu Gemini vẫn gặp vấn đề, bạn có thể chuyển sang OpenAI:

```bash
# Trong file .env, thay đổi:
AI_PROVIDER=openai
```

OpenAI có quota cao hơn nhưng tốn phí.

### 4. Đợi quota reset

Gemini Free Tier reset theo:
- **Requests per minute**: Reset sau 1 phút
- **Requests per day**: Reset vào 00:00 UTC

## Kiểm tra quota hiện tại

Bạn có thể kiểm tra quota tại:
https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas

## Khởi động lại ứng dụng

Sau khi thay đổi `.env`, cần khởi động lại:

```bash
# Dừng ứng dụng hiện tại (Ctrl+C)
# Sau đó chạy lại:
source venv/bin/activate
python main.py
```

## Lưu ý về Google Web Speech

Google Web Speech API:
- ✅ Miễn phí
- ✅ Không giới hạn quota
- ✅ Hỗ trợ tiếng Việt tốt
- ⚠️ Cần kết nối internet
- ⚠️ Độ chính xác có thể thấp hơn Gemini một chút

Đây là lựa chọn tốt nhất cho STT trong dự án này!
