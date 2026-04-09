# SPEC — AI Product Hackathon

**Nhóm:** Nhóm 4 

**Track:** ☐ VinFast · ☐ Vinmec · ☐ VinUni-VinSchool ·  ☑ XanhSM · ☐ Open

**Problem statement (1 câu):** Khách hàng của Xanh SM phải chờ đợi lâu để được hỗ trợ cho các vấn đề lặp lại (khiếu nại, mất đồ, FAQ), trong khi một AI agent có thể hiểu ngữ cảnh và xử lý phần lớn các yêu cầu này ngay lập tức.

---

## 1. AI Product Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi** | User nào? Pain gì? AI giải gì? | Khi AI sai thì sao? User sửa bằng cách nào? | Cost/latency bao nhiêu? Risk chính? |
| **Trả lời** | Người dùng Xanh SM mất 5–10 phút để liên hệ CSKH cho các vấn đề đơn giản → AI agent xử lý ngay trong chat (<10s)| AI trả lời sai → user thấy ngay trong chat → có thể nhập lại hoặc yêu cầu tạo ticket|~$0.005–0.02/request, latency <3s, risk: hallucination, hiểu sai intent |

**Automation hay augmentation?** ☐ Automation · ☑ Augmentation
Justify: User vẫn là người quyết định cuối cùng (chấp nhận câu trả lời hoặc tạo ticket), AI chỉ đề xuất và hỗ trợ → cost of reject ≈ 0
**Learning signal:**

1. User correction đi vào đâu? → Log hội thoại + intent đúng → dùng để cải thiện prompt / training sau
2. Product thu signal gì để biết tốt lên hay tệ đi? 
   → Tỷ lệ:
   user chấp nhận câu trả lời
   user không cần tạo ticket
   số lần user hỏi lại
3. Data thuộc loại nào? ☐ User-specific · ☑ Domain-specific · ☑ Real-time · ☑ Human-judgment · ☐ Khác: ___
   
   Có marginal value không? (Model đã biết cái này chưa?):  Có. Dữ liệu CSKH (complaint, lost-item) mang tính đặc thù, model chung chưa tối ưu tốt.

---

## 2. User Stories — 4 paths

Mỗi feature chính = 1 bảng. AI trả lời xong → chuyện gì xảy ra?

### Feature: Xử lý khiếu nại tài xế

User nhập: “Tôi bị tài xế đi vòng”

| Path | Câu hỏi thiết kế | Mô tả |
|------|-------------------|-------|
| Happy — AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | AI xin lỗi + hướng dẫn + đề xuất tạo ticket → user đồng ý |
| Low-confidence — AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | AI hỏi thêm chi tiết (xe, thời gian, mã chuyến xe) |
| Failure — AI sai | User biết AI sai bằng cách nào? Recover ra sao? | AI không detect đúng intent|
| Correction — user sửa | User sửa bằng cách nào? Data đó đi vào đâu? |User bổ sung thông tin → hệ thống cập nhật |

### Feature: Mất đồ
Trigger:
User: “Tôi để quên ví trên xe”

|Path|Câu hỏi thiết kế|Mô tả|  
|------|-------|
|Happy	|Flow end?	|AI hỏi thêm info → tạo ticket thành công|
|Low-confidence	|Không chắc?	|AI hỏi thêm chi tiết (xe, thời gian)|
|Failure	|Sai?	|AI không detect đúng intent|
|Correction	|Sửa?	|User bổ sung thông tin → hệ thống cập nhật|

### Feature: FAQ
Trigger:
User: “Huỷ chuyến thế nào?”

|Path		|Mô tả|
|-------|-------|
|Happy	|AI trả lời đúng từ FAQ|
|Low-confidence	|AI trả lời “không chắc”|
|Failure	|AI hallucinate
|Correction	|User phản hồi lại|
---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** ☑ Precision · ☐ Recall
**Tại sao? → CSKH cần trả lời đúng, sai → mất trust ngay
**Nếu sai ngược lại thì chuyện gì xảy ra? trả lời lan man, không chính xác → user bỏ dùng.

| Metric	|Threshold	|Red flag (dừng khi)|
|------|-------------------|-------|
|Intent classification accuracy	|≥85%	|<70%|
|FAQ answer accuracy	|≥80%	|<60%|
|User accept rate	|≥70%	|<50%|
|Latency	|<3s	|>5s|

---

## 4. Top 3 failure modes

*Liệt kê cách product có thể fail — không phải list features.*
*"Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."*

|#	|Trigger	|Hậu quả	|Mitigation|
|------|---------|----------|-------|
|1	|Prompt không rõ / thiếu data	|AI hallucinate	|Dùng RAG + fallback “không chắc”|
|2	|Hiểu sai intent	|Gọi sai action	|Thêm bước hỏi lại (clarification)|
|3	|Thiếu context	|Trả lời generic	|Lưu lịch sử chat|
---

## 5. ROI 3 kịch bản

||Conservative	|Realistic	|Optimistic|
|--|----|-------------------|-------|
|Assumption	|100 user/ngày, 60% hài lòng|500 user/ngày, 80%	|2000 user/ngày, 90%|
|Cost	|$20/ngày| $100/ngày	|$400/ngày|
|Benefit	|Giảm 2h CSKH/ngày|Giảm 8h/ngày	|Giảm 20h + tăng retention|
|Net	|+	|++	|+++|

**Kill criteria:** 
→ Dừng nếu cost > benefit trong 2 tháng liên tục

---

## 6. Mini AI spec (1 trang)
Sản phẩm là một AI Customer Support Agent cho Xanh SM, giúp xử lý các yêu cầu chăm sóc khách hàng lặp lại như khiếu nại, mất đồ và FAQ.

Hệ thống sử dụng LLM để hiểu ngôn ngữ tự nhiên tiếng Việt, phân loại intent và truy xuất thông tin từ FAQ (RAG). Điểm khác biệt chính là AI không chỉ trả lời mà còn có khả năng ra quyết định hành động, ví dụ như đề xuất tạo ticket khi cần thiết.

Sản phẩm theo hướng augmentation, nghĩa là AI hỗ trợ và đề xuất, còn người dùng vẫn kiểm soát quyết định cuối cùng. Điều này giúp giảm rủi ro khi AI sai.

Chất lượng hệ thống ưu tiên precision (≥85%) để đảm bảo độ tin cậy. Các rủi ro chính bao gồm hallucination và hiểu sai intent, được giảm thiểu bằng cách:

sử dụng knowledge base (RAG)
hỏi lại khi không chắc (clarification)
cho phép user chỉnh sửa (correction)

Dữ liệu từ hành vi người dùng (chỉnh sửa, phản hồi) sẽ tạo thành một data flywheel, giúp hệ thống ngày càng chính xác hơn theo thời gian.
