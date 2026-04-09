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
        },
        "124": {
            "driver": "Trần Thị B",
            "vehicle": "Ô tô 4 chỗ",
            "time": "11:00 AM",
            "route": "Vincom Đồng Khởi → Sân bay Tân Sơn Nhất"
        },
        "125": {
            "driver": "Lê Minh C",
            "vehicle": "Ô tô 7 chỗ",
            "time": "01:15 PM",
            "route": "Bến Thành → Thảo Điền"
        },
        "126": {
            "driver": "Phạm Quốc D",
            "vehicle": "Xe máy",
            "time": "02:45 PM",
            "route": "Đại học Bách Khoa → Crescent Mall"
        },
        "127": {
            "driver": "Hoàng Gia E",
            "vehicle": "Ô tô 4 chỗ",
            "time": "04:20 PM",
            "route": "Landmark 81 → Chợ Bến Thành"
        },
        "128": {
            "driver": "Đỗ Thu F",
            "vehicle": "Xe máy",
            "time": "05:05 PM",
            "route": "Aeon Mall Tân Phú → Đầm Sen"
        },
        "129": {
            "driver": "Bùi Anh G",
            "vehicle": "Ô tô 7 chỗ",
            "time": "06:30 PM",
            "route": "Sân bay Tân Sơn Nhất → Quận 7"
        },
        "130": {
            "driver": "Võ Thanh H",
            "vehicle": "Ô tô 4 chỗ",
            "time": "07:10 PM",
            "route": "Bưu điện Thành phố → Bitexco"
        },
        "131": {
            "driver": "Ngô Đức I",
            "vehicle": "Xe máy",
            "time": "08:00 PM",
            "route": "Phú Mỹ Hưng → SC VivoCity"
        },
        "132": {
            "driver": "Phan Mỹ J",
            "vehicle": "Ô tô 4 chỗ",
            "time": "09:25 PM",
            "route": "Gò Vấp → Quận 1"
        },
        "133": {
            "driver": "Đặng Khánh K",
            "vehicle": "Xe máy",
            "time": "09:50 PM",
            "route": "Ngã tư Hàng Xanh → Thủ Đức"
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