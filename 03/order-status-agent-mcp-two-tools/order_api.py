"""Standalone simulated Order API; independent from LLM tool definitions."""
import random
from datetime import datetime, timedelta, timezone

STATUSES = ["Processing", "Packed", "Shipped", "Out for delivery", "Delivered", "Delayed"]

def get_order_status(order_id: str) -> dict:
    """Hardcoded mock API behavior: returns a randomly selected status on every call."""
    status = random.choice(STATUSES)
    eta_days = {"Processing": 5, "Packed": 4, "Shipped": 2, "Out for delivery": 0, "Delayed": 7}
    result = {"order_id": order_id, "status": status, "source": "mock-order-api", "simulated": True}
    if status in eta_days:
        result["estimated_delivery"] = (datetime.now(timezone.utc) + timedelta(days=eta_days[status])).date().isoformat()
    if status == "Delivered":
        result["message"] = "The package has been delivered."
    elif status == "Delayed":
        result["message"] = "A shipping delay was reported; delivery estimate may change."
    else:
        result["message"] = f"The order is currently {status.lower()}."
    return result

