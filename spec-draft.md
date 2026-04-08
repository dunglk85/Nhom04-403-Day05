PEC DRAFT – AI Customer Support cho Xanh SM

🎯 Problem Statement

Bối cảnh
Trong quá trình mở rộng nhanh chóng, Xanh SM đang phải xử lý một lượng lớn yêu cầu từ khách hàng mỗi ngày, bao gồm: hỏi thông tin chuyến đi, khiếu nại tài xế, báo mất đồ, và các vấn đề liên quan đến thanh toán.

Vấn đề cốt lõi
Hiện tại, hệ thống chăm sóc khách hàng gặp 3 hạn chế chính:

Quá tải và phản hồi chậm
Các câu hỏi lặp lại chiếm phần lớn (ví dụ: giá cước, trạng thái chuyến, chính sách huỷ chuyến)
Nhân viên CSKH không thể xử lý kịp trong giờ cao điểm
→ Khách hàng phải chờ lâu, trải nghiệm kém
Thiếu cá nhân hoá và ngữ cảnh
Hệ thống hiện tại không hiểu sâu lịch sử người dùng
Không tự động tra cứu dữ liệu liên quan (chuyến đi gần nhất, tài xế, vị trí,...)
→ Trả lời chung chung, không giải quyết đúng vấn đề
Xử lý khiếu nại chưa thông minh
Khó phân loại mức độ nghiêm trọng của khiếu nại
Không có cơ chế tự động đề xuất hướng xử lý
→ Tăng chi phí vận hành và rủi ro mất khách

Hệ quả (Impact)

Tăng tỷ lệ khách hàng không hài lòng
Gia tăng chi phí nhân sự CSKH
Giảm khả năng giữ chân khách hàng trong thị trường cạnh tranh với các nền tảng ride-hailing khác

Câu hỏi cần giải quyết

Làm thế nào để xây dựng một hệ thống AI có thể hiểu đúng ý định khách hàng, truy xuất ngữ cảnh liên quan, và tự động xử lý hoặc hỗ trợ xử lý yêu cầu CSKH một cách nhanh chóng và chính xác, đồng thời giảm tải cho đội ngũ vận hành?

1. 🧭 Overview

Tên dự án: Xanh SM AI Support Agent
Mục tiêu:
Xây dựng một ứng dụng sử dụng LLM để tự động hóa chăm sóc khách hàng cho dịch vụ gọi xe điện của Xanh SM.

Vấn đề:

Quá tải CSKH
Khách hỏi lặp lại
Phản hồi chậm → trải nghiệm kém

Giải pháp:

AI chatbot hiểu tiếng Việt
Trả lời theo policy
Có thể thực hiện action (tạo ticket)
2. 👤 User Personas
2.1 Khách hàng
Muốn:
hỏi nhanh
giải quyết vấn đề ngay
Pain:
chờ tổng đài lâu
2.2 Nhân viên CSKH
Muốn:
giảm workload
Pain:
xử lý câu hỏi lặp lại
3. 🎯 Use Cases chính
ID	Use Case	Mô tả
UC1	Hỏi thông tin	Giá cước, chính sách
UC2	Khiếu nại	Tài xế, chuyến đi
UC3	Mất đồ	Tạo ticket
UC4	Huỷ chuyến	Hướng dẫn
UC5	FAQ	Trả lời tự động
4. 🧠 Functional Requirements
4.1 Chat AI
Nhận input tiếng Việt tự nhiên
Hiểu intent:
hỏi thông tin
khiếu nại
yêu cầu hỗ trợ
4.2 RAG (Knowledge Base)
Truy xuất từ:
FAQ
policy nội bộ
Trả lời đúng context
4.3 Ticket Simulation
Khi detect:
“khiếu nại”
“mất đồ”
→ tạo ticket giả lập
4.4 Context Memory
Giữ lịch sử chat trong session
5. ⚙️ Non-functional Requirements
Response < 3s
UI đơn giản, dễ dùng
Demo chạy local (không phụ thuộc backend thật)
Scale: không cần (hackathon)
6. 🏗️ System Architecture
[Frontend - Streamlit]
        ↓
[Backend Logic]
        ↓
[LLM API (GPT/Gemini)]
        ↓
[Vector DB (FAQ)]
7. 🧩 Components
7.1 Frontend
Chat UI
Input box
Hiển thị response
7.2 Backend
Prompt builder
Intent detection (LLM-based)
7.3 LLM Layer
Model: GPT / Gemini
Role:
hiểu câu hỏi
generate response
7.4 Knowledge Base
File:
faq.txt
Embedding + search
7.5 Tool Layer
create_ticket()
log_issue()
8. 🔄 Flow xử lý
User Input
   ↓
Intent Detection (LLM)
   ↓
RAG (FAQ retrieval)
   ↓
LLM Response
   ↓
Check action → tạo ticket (nếu cần)
   ↓
Return to UI
9. 🗂️ Data Design
FAQ sample:
{
  "question": "Huỷ chuyến thế nào?",
  "answer": "Bạn có thể huỷ miễn phí trong 2 phút đầu"
}
Ticket sample:
{
  "id": "T001",
  "type": "lost_item",
  "status": "created"
}
10. 🖥️ UI Mock
---------------------------
🚗 Xanh SM AI Support
---------------------------
[ Bạn cần hỗ trợ gì? ]

User: Tôi bị tài xế đi vòng
AI: Xin lỗi bạn...

👉 [Tạo ticket]
11. 🎬 Demo Scenario
Scenario 1:
User: “Tôi muốn huỷ chuyến”
AI: trả lời policy
Scenario 2:
User: “Tôi bị mất đồ”
AI:
hỏi thêm info
tạo ticket
12. 📊 Success Metrics
Accuracy trả lời: ~80%
Thời gian phản hồi: <3s
Demo flow mượt
13. 🚀 Future Work
Kết nối backend thật
Tích hợp app mobile
Voice assistant
Multi-agent system
💡 Bonus (ăn điểm judge)