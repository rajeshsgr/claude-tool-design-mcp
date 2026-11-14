"""Second hardcoded mock API: delivery estimate, independent of order status."""
from datetime import datetime, timedelta, timezone
import re


def get_delivery_eta(order_id: str) -> dict:
    """Deterministic simulated delivery estimate based on order digits."""
    if not re.fullmatch(r"ORD-\d{4}", order_id, re.IGNORECASE):
        raise ValueError("Order ID must match ORD-1234")
    # Stable per ID for the demo; no external services are contacted.
    days = 1 + int(order_id[-4:]) % 5
    eta = (datetime.now(timezone.utc) + timedelta(days=days)).date().isoformat()
    return {"order_id": order_id.upper(), "estimated_delivery": eta,
            "days_remaining": days, "source": "mock-delivery-api", "simulated": True,
            "message": "Estimated arrival based on simulated shipping schedule."}
