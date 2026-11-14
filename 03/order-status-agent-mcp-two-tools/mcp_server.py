"""MCP server that exposes TWO mock order tools over stdio (MCP SDK v1)."""
import logging
import re
import sys
from mcp.server.fastmcp import FastMCP
from order_api import get_order_status as lookup_status
from delivery_api import get_delivery_eta as lookup_eta

logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(asctime)s | MCP SERVER | %(levelname)s | %(message)s")
logger = logging.getLogger("order_mcp_server")
mcp = FastMCP("mock-order-service-two-tools")
ORDER_ID = re.compile(r"ORD-\d{4}", re.IGNORECASE)


def validate_id(order_id: str) -> str:
    if not isinstance(order_id, str) or not ORDER_ID.fullmatch(order_id):
        raise ValueError("Order ID must be in format ORD-1234")
    return order_id.upper()


@mcp.tool()
def get_order_status(order_id: str) -> dict:
    """Look up the CURRENT simulated processing/shipping status of an order.

    Use for requests like 'What is the status?', 'Is my order shipped?', or
    'Is ORD-1234 delayed?'. Do NOT use solely to answer 'When will it arrive?';
    that is get_delivery_eta. Never use for refunds, cancellation, or modifications.
    This is random mock status data; never claim that it is real.

    Args:
        order_id: Exact order ID supplied by the user, e.g. ORD-1234.
    """
    order_id = validate_id(order_id)
    logger.info("INVOKING MCP TOOL | get_order_status | %s", order_id)
    return lookup_status(order_id)


@mcp.tool()
def get_delivery_eta(order_id: str) -> dict:
    """Look up the simulated expected delivery DATE or arrival timeframe of an order.

    Use for 'When will ORD-1234 arrive?', 'What's the ETA?', or 'How many days
    until delivery?'. Do NOT use solely to determine current shipping/status;
    that is get_order_status. For status AND ETA, both tools may be useful.
    No real carrier tracking occurs; estimates are fabricated for this demo.

    Args:
        order_id: Exact order ID supplied by the user, e.g. ORD-1234.
    """
    order_id = validate_id(order_id)
    logger.info("INVOKING MCP TOOL | get_delivery_eta | %s", order_id)
    return lookup_eta(order_id)


if __name__ == "__main__":
    logger.info("Starting two-tool MCP server over stdio")
    mcp.run(transport="stdio")
