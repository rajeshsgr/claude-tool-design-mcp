"""Standalone MCP server for the mocked order API (stdio transport)."""
import logging
import re
import sys
from mcp.server.fastmcp import FastMCP
from order_api import get_order_status as mock_order_lookup

# An MCP stdio server must NOT print logs to stdout: stdout is for MCP protocol messages.
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(asctime)s | MCP SERVER | %(levelname)s | %(message)s")
logger = logging.getLogger("order_mcp_server")

mcp = FastMCP("mock-order-service")
ORDER_ID = re.compile(r"ORD-\d{4}", re.IGNORECASE)

@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """Look up a customer's simulated order status using its order ID.

    Use this tool only when the user asks about tracking/shipping/delivery status
    and explicitly provides an order ID in the format ORD-1234.
    Do not use it to cancel, refund, return, or modify orders.
    The returned order status is RANDOM mock data, not a real customer record.

    Args:
        order_id: The user-provided identifier, e.g. ORD-1234.
    """
    logger.info("MCP TOOL INVOKED | get_order_status | order_id=%s", order_id)
    if not isinstance(order_id, str) or not ORDER_ID.fullmatch(order_id):
        logger.warning("MCP TOOL REJECTED | invalid order ID")
        raise ValueError("Order ID must match ORD-1234")
    result = mock_order_lookup(order_id.upper())
    logger.info("MCP TOOL RESULT | %s", result)
    return result

if __name__ == "__main__":
    logger.info("Starting mock-order-service MCP server using stdio")
    mcp.run(transport="stdio")
