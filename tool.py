from typing import Optional
from langchain_core.tools import tool


# =========================
# TOOL 1: CREATE TICKET
# =========================
@tool
def create_ticket(
    issue_type: str,
    description: str,
    trip_id: Optional[str] = None,
    time: Optional[str] = None
) -> str:
    """
    Tạo ticket hỗ trợ cho khách hàng (khiếu nại, mất đồ, sự cố).
    """

    # 👉 mock xử lý
    ticket_id = "TICKET123"

    return (
        f"Đã tạo ticket thành công 🎫\n"
        f"- Mã ticket: {ticket_id}\n"
        f"- Loại vấn đề: {issue_type}\n"
        f"- Mô tả: {description}\n"
        f"Chúng tôi sẽ liên hệ với bạn sớm nhất có thể."
    )


# =========================
# TOOL 2: LOOKUP TRIP
# =========================
@tool
def lookup_trip(trip_id: str) -> str:
    """
    Tra cứu thông tin chuyến đi dựa trên mã chuyến.
    """

    # 👉 mock data (demo)
    fake_db = {
        "123": {
            "driver": "Nguyễn Văn A",
            "vehicle": "Xe máy",
            "time": "10:30 AM",
            "route": "A → B"
        }
    }

    trip = fake_db.get(trip_id)

    if not trip:
        return "Không tìm thấy thông tin chuyến đi. Bạn vui lòng kiểm tra lại mã chuyến giúp mình."

    return (
        f"Thông tin chuyến đi 🚗:\n"
        f"- Tài xế: {trip['driver']}\n"
        f"- Phương tiện: {trip['vehicle']}\n"
        f"- Thời gian: {trip['time']}\n"
        f"- Lộ trình: {trip['route']}"
    )