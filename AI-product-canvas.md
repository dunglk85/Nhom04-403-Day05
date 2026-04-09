# AI Product Canvas — Xanh SM Customer Support Agent

**Nhóm:** Nhóm 4  
**Track:** XanhSM  
**Problem statement:** Khách hàng của Xanh SM phải chờ đợi lâu để được hỗ trợ cho các vấn đề lặp lại (khiếu nại, mất đồ, FAQ), trong khi một AI agent có thể hiểu ngữ cảnh và xử lý phần lớn các yêu cầu này ngay lập tức.

---

## AI Product Canvas

|   | **Value** | **Trust** | **Feasibility** |
|---|-----------|-----------|-----------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | **User:** Khách hàng Xanh SM có vấn đề cần hỗ trợ (khiếu nại tài xế, mất đồ, hỏi FAQ).<br><br>**Pain:** Phải chờ 5–10 phút để kết nối với CSKH qua hotline/chat cho các vấn đề đơn giản, lặp lại. Tốn thời gian, trải nghiệm kém.<br><br>**AI giải quyết:** Trả lời ngay lập tức (<10s) trong chat, xử lý tự động các case đơn giản (FAQ, hướng dẫn huỷ chuyến), đề xuất tạo ticket cho case phức tạp. Cách hiện tại không thể scale 24/7 với chi phí thấp. | **Khi AI sai:** User nhận câu trả lời không chính xác hoặc không liên quan → mất thời gian, giảm niềm tin vào hệ thống.<br><br>**User biết AI sai:** Câu trả lời không khớp với câu hỏi, hoặc thông tin rõ ràng sai lệch với thực tế (vd: AI nói "không thể huỷ" nhưng user biết là được).<br><br>**User sửa:** Nhập lại câu hỏi chi tiết hơn, hoặc yêu cầu tạo ticket để chuyển cho nhân viên CSKH thực xử lý. | **Cost:** ~$0.005–0.02/request (LLM API + RAG retrieval).<br><br>**Latency:** <3s (target), ngưỡng đỏ >5s.<br><br>**Risk chính:**<br>• Hallucination (AI bịa thông tin không có trong KB)<br>• Hiểu sai intent (nhầm "mất đồ" thành "khiếu nại")<br>• Thiếu context (không nhớ lịch sử chat) |

---

## Automation hay augmentation?

☐ **Automation** — AI làm thay, user không can thiệp  
☑ **Augmentation** — AI gợi ý, user quyết định cuối cùng

**Justify:**  
User vẫn giữ quyền kiểm soát cuối cùng: có thể chấp nhận câu trả lời của AI, yêu cầu làm rõ thêm, hoặc tạo ticket chuyển cho CSKH thực. AI chỉ đề xuất giải pháp và hướng dẫn, không tự động thực hiện hành động có tác động lớn (vd: hoàn tiền, khoá tài khoản). **Cost of reject ≈ 0** — nếu user không hài lòng, họ chỉ cần bỏ qua hoặc hỏi lại.

*Lưu ý: Nếu AI sai mà user không biết → automation nguy hiểm. Ở đây user nhìn thấy output ngay, nên augmentation an toàn hơn.*

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| **1** | User correction đi vào đâu? | Mọi tương tác được log: câu hỏi gốc, intent đã detect, câu trả lời AI đưa ra, phản ứng của user (accept/reject/hỏi lại/tạo ticket). Data này đưa vào data warehouse để:<br>• Retrain intent classifier<br>• Cập nhật FAQ knowledge base<br>• Fine-tune prompt engineering |
| **2** | Product thu signal gì để biết tốt lên hay tệ đi? | **Leading indicators:**<br>• % user chấp nhận câu trả lời ngay (≥70% = tốt)<br>• % user không cần tạo ticket sau khi chat với AI<br>• Số lần user phải hỏi lại (càng ít càng tốt)<br>• Average conversation length (càng ngắn = AI hiểu nhanh)<br><br>**Lagging indicators:**<br>• CSAT score sau khi dùng AI agent<br>• Giảm volume ticket CSKH cho các vấn đề đơn giản<br>• Retention rate của user đã dùng AI vs chưa dùng |
| **3** | Data thuộc loại nào?<br>☐ User-specific<br>☑ Domain-specific<br>☑ Real-time<br>☑ Human-judgment<br>☐ Khác: ___ | ☑ **Domain-specific:** Ngôn ngữ CSKH của Xanh SM (cách khách phàn nàn, thuật ngữ như "đi vòng", "quên đồ")<br>☑ **Real-time:** Intent và context thay đổi liên tục theo tình huống thực tế<br>☑ **Human-judgment:** Đánh giá "câu trả lời này có hữu ích không" phụ thuộc vào cảm nhận của user<br><br>**Có marginal value không?**<br>**CÓ.** LLM công khai (GPT, Claude) được train trên data chung, chưa tối ưu cho:<br>• Ngôn ngữ thực tế của khách Việt Nam ("bác tài xế chạy lung tung")<br>• Chính sách cụ thể của Xanh SM (thời gian huỷ, quy trình đền bù mất đồ)<br>• Pattern khiếu nại đặc thù (hotspot vấn đề: khu vực nào hay bị đi vòng, loại đồ nào hay quên)<br><br>Data này khó mua được từ bên ngoài → **marginal value cao** cho việc cải thiện model. |

---

## Tóm tắt chiến lược

Sản phẩm này theo hướng **augmentation with strong learning loop**: 

AI hỗ trợ → user phản hồi → data feed back → AI tốt hơn → user hài lòng hơn → nhiều user dùng → nhiều data hơn. 

Điểm mấu chốt là **không để AI tự động làm việc nguy hiểm**, mà luôn có human-in-the-loop ở các điểm quan trọng.

---

## User Stories — 4 paths

### Feature 1: Xử lý khiếu nại tài xế

**Trigger:** User nhập: "Tôi bị tài xế đi vòng"

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy — AI đúng, tự tin** | User thấy gì? Flow kết thúc ra sao? | AI xin lỗi + hướng dẫn + đề xuất tạo ticket → user đồng ý |
| **Low-confidence — AI không chắc** | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI hỏi thêm chi tiết (xe, thời gian, mã chuyến xe) |
| **Failure — AI sai** | User biết AI sai bằng cách nào? Recover ra sao? | AI không detect đúng intent → user nhập lại hoặc yêu cầu chuyển nhân viên |
| **Correction — user sửa** | User sửa bằng cách nào? Data đó đi vào đâu? | User bổ sung thông tin → hệ thống cập nhật log + retrain |

---

### Feature 2: Mất đồ

**Trigger:** User: "Tôi để quên ví trên xe"

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy** | Flow end? | AI hỏi thêm info → tạo ticket thành công |
| **Low-confidence** | Không chắc? | AI hỏi thêm chi tiết (xe, thời gian, mô tả đồ vật) |
| **Failure** | Sai? | AI không detect đúng intent → user làm rõ |
| **Correction** | Sửa? | User bổ sung thông tin → hệ thống cập nhật |

---

### Feature 3: FAQ

**Trigger:** User: "Huỷ chuyến thế nào?"

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| **Happy** | Flow end? | AI trả lời đúng từ FAQ knowledge base |
| **Low-confidence** | Không chắc? | AI trả lời "Tôi không chắc chắn, bạn có thể..." |
| **Failure** | Sai? | AI hallucinate thông tin sai → user phát hiện |
| **Correction** | Sửa? | User phản hồi lại → log để cải thiện KB |

---

## Eval metrics + threshold

**Optimize precision hay recall?** ☑ **Precision** · ☐ Recall

**Tại sao?** → CSKH cần trả lời đúng, sai → mất trust ngay  
**Nếu sai ngược lại thì chuyện gì xảy ra?** Trả lời lan man, không chính xác → user bỏ dùng.

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| Intent classification accuracy | ≥85% | <70% |
| FAQ answer accuracy | ≥80% | <60% |
| User accept rate | ≥70% | <50% |
| Latency | <3s | >5s |

---

## Top 3 failure modes

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| **1** | Prompt không rõ / thiếu data | AI hallucinate | Dùng RAG + fallback "không chắc" |
| **2** | Hiểu sai intent | Gọi sai action | Thêm bước hỏi lại (clarification) |
| **3** | Thiếu context | Trả lời generic | Lưu lịch sử chat |

---

## ROI 3 kịch bản

|  | **Conservative** | **Realistic** | **Optimistic** |
|---|------------------|---------------|----------------|
| **Assumption** | 100 user/ngày, 60% hài lòng | 500 user/ngày, 80% | 2000 user/ngày, 90% |
| **Cost** | $20/ngày | $100/ngày | $400/ngày |
| **Benefit** | Giảm 2h CSKH/ngày (~$30) | Giảm 8h/ngày (~$120) | Giảm 20h/ngày + tăng retention (~$500) |
| **Net** | +$10/ngày | +$20/ngày | +$100/ngày |

**Kill criteria:**  
→ Dừng nếu cost > benefit trong 2 tháng liên tục

---

## Mini AI spec (1 trang)

### Sản phẩm là gì?
AI Customer Support Agent cho Xanh SM, giúp xử lý các yêu cầu chăm sóc khách hàng lặp lại như khiếu nại, mất đồ và FAQ.

### Công nghệ
Hệ thống sử dụng LLM để hiểu ngôn ngữ tự nhiên tiếng Việt, phân loại intent và truy xuất thông tin từ FAQ (RAG). 

### Điểm khác biệt
AI không chỉ trả lời mà còn có khả năng ra quyết định hành động, ví dụ như đề xuất tạo ticket khi cần thiết.

### Triết lý thiết kế
Sản phẩm theo hướng **augmentation**, nghĩa là AI hỗ trợ và đề xuất, còn người dùng vẫn kiểm soát quyết định cuối cùng. Điều này giúp giảm rủi ro khi AI sai.

### Chất lượng
Hệ thống ưu tiên **precision (≥85%)** để đảm bảo độ tin cậy. 

### Rủi ro & giảm thiểu
Các rủi ro chính bao gồm hallucination và hiểu sai intent, được giảm thiểu bằng cách:
- Sử dụng knowledge base (RAG)
- Hỏi lại khi không chắc (clarification)
- Cho phép user chỉnh sửa (correction)

### Data flywheel
Dữ liệu từ hành vi người dùng (chỉnh sửa, phản hồi) sẽ tạo thành một data flywheel, giúp hệ thống ngày càng chính xác hơn theo thời gian.
