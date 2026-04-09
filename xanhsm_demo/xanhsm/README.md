# Xanh SM – Demo App

## Cấu trúc thư mục

```
xanhsm/
├── backend/
│   ├── agent.py          # LangGraph agent
│   ├── tool.py           # Tools: create_ticket, lookup_trip
│   ├── server.py         # FastAPI server
│   ├── system_promt.md   # System prompt
│   ├── requirements.txt
│   └── .env              # ← Điền OPENAI_API_KEY vào đây
└── frontend/
    ├── index.html        # App UI
    └── images/           # Ảnh màn hình
```

---

## Cài đặt & Chạy

### Bước 1 – Điền API Key

Mở file `backend/.env` và thay thế:
```
OPENAI_API_KEY=sk-...your-key-here...
```

### Bước 2 – Cài thư viện Python

```bash
cd backend
pip install -r requirements.txt
```

### Bước 3 – Chạy backend

```bash
cd backend
uvicorn server:app --reload --port 8000
```

Backend sẽ chạy tại: http://localhost:8000
Kiểm tra: http://localhost:8000/health

### Bước 4 – Mở frontend

Mở file `frontend/index.html` trực tiếp trên trình duyệt.

> ⚠️ Nếu dùng Chrome và gặp lỗi CORS khi load ảnh local, chạy bằng Live Server (VS Code extension) hoặc:
> ```bash
> cd frontend
> python -m http.server 3000
> ```
> Sau đó truy cập http://localhost:3000

---

## Cách dùng

1. **Màn hình Home** – Nhấn icon 💬 góc phải dưới để mở chatbot
2. **Quick chips** – Nhấn các chip để thử nhanh các tình huống
3. **Điều hướng tự động** – Agent sẽ tự mở màn hình tương ứng:
   - Đặt xe → màn hình chọn điểm đến
   - Đồ ăn → màn hình Xanh Ngon
   - Giao hàng → màn hình dịch vụ vận chuyển
   - Khuyến mãi → màn hình thẻ quà tặng
4. **Tra cứu chuyến** – Thử nhập "Tra cứu chuyến 124"
5. **Khiếu nại** – Agent thu thập thông tin rồi tạo ticket

---

## API Endpoints

| Method | URL | Mô tả |
|--------|-----|-------|
| POST | /chat | Gửi tin nhắn |
| DELETE | /chat/{session_id} | Xóa lịch sử hội thoại |
| GET | /health | Kiểm tra server |

### Ví dụ gọi API:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "message": "Tôi muốn đặt xe"}'
```
