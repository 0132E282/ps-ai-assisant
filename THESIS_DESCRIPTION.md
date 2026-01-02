# ĐỀ CƯƠNG ĐỒ ÁN TỐT NGHIỆP

**Tên đề tài:** Nghiên cứu và xây dựng hệ thống Trợ lý ảo AI đa mục tiêu điều khiển Robot vật lý và Máy tính cá nhân bằng giọng nói.

---

## 1. Lý do chọn đề tài
Trong kỷ nguyên Công nghiệp 4.0, sự phát triển của Trí tuệ nhân tạo (AI) đã mở ra những khả năng mới trong việc tương tác giữa người và máy. Các mô hình ngôn ngữ lớn (LLM) như GPT-4 đã chứng minh khả năng hiểu ngữ cảnh và ý định vượt trội. Tuy nhiên, việc kết nối sức mạnh trí tuệ của AI với các thực thể vật lý (Robot) và môi trường làm việc số (PC) một cách an toàn và trực quan vẫn là một thách thức. Đồ án này tập trung vào việc hiện thực hóa một hệ thống trợ lý AI "hybrid" có khả năng tác động đồng thời lên cả thế giới thực và thế giới số qua giao diện giọng nói.

## 2. Mục tiêu nghiên cứu
- **Tương tác đa phương thức:** Xây dựng module nhận dạng giọng nói (STT) và tổng hợp tiếng nói (TTS) hỗ trợ song ngữ (Việt/Anh).
- **Hệ thống tư duy AI:** Ứng dụng mô hình GPT-4o-mini làm bộ não điều phối, phân tích ý định từ ngôn ngữ tự nhiên thành các lệnh thực thi cấu trúc.
- **Điều khiển Robotics:** Thiết kế cơ chế điều khiển robot qua Raspberry Pi, đảm bảo độ trễ thấp và độ chính xác cao.
- **Tự động hóa PC:** Xây dựng Framework điều khiển máy tính an toàn, cho phép thao tác với ứng dụng và đa phương tiện.
- **Giao thức MCP:** Áp dụng Model Context Protocol để tiêu chuẩn hóa việc giao tiếp giữa AI và các công cụ hệ thống.

## 3. Kiến trúc hệ thống (MVC + MCP)
Hệ thống được thiết kế theo mô hình 3 lớp nhằm đảm bảo tính module hóa:
- **Lớp Dữ liệu (Model):** Quản lý trạng thái Robot, logic xử lý ngôn ngữ và các schema lệnh JSON.
- **Lớp Hiển thị/Giao diện (View):** Giao diện tương tác bằng giọng nói (Voice UI) và hệ thống log giám sát.
- **Lớp Điều khiển (Controller):** Đóng vai trò cầu nối, nhận Command JSON từ AI, xác thực bảo mật và điều phối xuống phần cứng hoặc hệ điều hành qua Python.

## 4. Công nghệ sử dụng
- **Phần mềm:** Python, OpenAI Whisper (STT), GPT-4o-mini API, FPT AI/gTTS (TTS).
- **Phẩn cứng:** Raspberry Pi 4/5, Mạch cầu H (L298N/L293D), Động cơ DC, Microphone Array.
- **Giao tiếp:** Model Context Protocol (MCP) giúp AI hiểu và gọi các "tool" hệ thống một cách chuẩn hóa.

## 5. Các tính năng chính
1. **Robot di chuyển:** Ra lệnh bằng giọng nói: "Đi thẳng 2 mét", "Rẽ trái và dừng lại".
2. **Trợ lý máy tính:** "Mở Chrome", "Phát nhạc trên Youtube", "Kiểm tra thời tiết hôm nay".
3. **Phản hồi thông minh:** AI không chỉ thực hiện lệnh mà còn phản hồi, giải thích hành động hoặc yêu cầu làm rõ ý định.
4. **An toàn hệ thống:** Giới hạn tốc độ robot, danh sách ứng dụng trắng (whitelist) cho PC, nút dừng khẩn cấp qua phần mềm.

## 6. Tính mới và Ứng dụng
- **Tính mới:** Thay vì dùng các bộ lệnh cứng (hard-coded), hệ thống sử dụng LLM để hiểu các câu lệnh phức tạp, mơ hồ. Việc áp dụng MCP giúp hệ thống dễ dàng mở rộng thêm các "kỹ năng" mới mà không cần sửa đổi kiến trúc lõi.
- **Ứng dụng:** Có thể phát triển thành robot phục vụ trong nhà, trợ lý cho người khuyết tật, hoặc hệ thống Smarthome thế hệ mới.

## 7. Kết luận
Đồ án không chỉ dừng lại ở việc tạo ra một thiết bị điều khiển từ xa, mà hướng tới việc xây dựng một **thực thể AI có khả năng tương tác** thực thụ. Sự kết hợp giữa xử lý ngôn ngữ tự nhiên đỉnh cao và khả năng can thiệp vật lý sẽ là nền tảng cho nhiều ứng dụng thực tiễn trong tương lai.
