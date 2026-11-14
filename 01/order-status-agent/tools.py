"""Tool contracts and execution registry.

Teaching points:
- Tool descriptions tell the model WHEN a tool is relevant.
- JSON schemas tell the model HOW to call it.
- Python functions execute the tool; their returned data is not the tool definition.
"""
from order_api import get_order_status

ORDER_TOOL = {
    "name": "get_order_status",
    "description": (
        "Look up a customer's order status, shipment progress, expected delivery, or delay. "
        "Use only for an order-status question with an order ID supplied by the customer. "
        "If no order ID is present, ask for it first. "
        "Do not use for cancellations, refunds, returns, address changes, or store policies. "
        "Order IDs use ORD-1234 format. This returns randomized, simulated demo data."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "Customer-supplied order ID in ORD-1234 format; never invent one."
            }
        },
        "required": ["order_id"],
        "additionalProperties": False
    }
}

TOOL_REGISTRY = {"get_order_status": get_order_status}
