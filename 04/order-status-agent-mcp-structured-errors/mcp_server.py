"""Example 4: MCP tools returning exact structured success/failure envelopes.

Error metadata fields are application conventions; isError is part of MCP.
"""
import json
import logging
import re
import sys
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
from order_api import get_order_status as lookup_status
from delivery_api import get_delivery_eta as lookup_eta

logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                    format="%(asctime)s | MCP SERVER | %(levelname)s | %(message)s")
logger = logging.getLogger("structured_order_server")
mcp = FastMCP("mock-order-service-structured-errors")
ID_RE = re.compile(r"ORD-\d{4}", re.IGNORECASE)
# State exists only for the lifespan of this demo MCP subprocess.
transient_attempts = {}


def result(data: dict, *, error: bool = False) -> CallToolResult:
    """Set the *real MCP* isError flag and structuredContent explicitly."""
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(data))],
        structuredContent=data,
        isError=error,
    )


def failure(category: str, retryable: bool, description: str, recovery: str) -> CallToolResult:
    payload = {"errorCategory": category, "isRetryable": retryable,
               "description": description, "recoveryAction": recovery}
    logger.warning("TOOL EXECUTION ERROR | category=%s | retryable=%s", category, retryable)
    return result(payload, error=True)


def checked_order(order_id: str):
    if not ID_RE.fullmatch(order_id):
        return failure("validation", False,
                       f"Invalid order ID '{order_id}'. Expected ORD followed by a hyphen and four digits, e.g. ORD-1234.",
                       "Ask user for a valid order ID; do not repeat the unchanged call.")
    order_id = order_id.upper()
    if order_id == "ORD-1003":
        return failure("business", False,
                       "Order ORD-1003 is locked pending manual review; status cannot be released.",
                       "Explain the hold and recommend contacting order support; do not retry.")
    if order_id == "ORD-1004":
        return failure("permission", False,
                       "Service account is not authorized to access restricted order ORD-1004.",
                       "Escalate to an authorized operator; do not retry with the same credentials.")
    if order_id == "ORD-1001":
        attempt = transient_attempts.get(order_id, 0)
        transient_attempts[order_id] = attempt + 1
        if attempt == 0:
            return failure("transient", True,
                           "Mock order service is temporarily unavailable on this first request.",
                           "Retry the same tool call once; this demo succeeds on the next attempt.")
    if order_id == "ORD-9999":
        # A valid empty result is NOT an MCP error.
        return result({"found": False, "order_id": order_id, "message": "No matching order found.",
                       "simulated": True}, error=False)
    return None


@mcp.tool()
def get_order_status(order_id: str) -> CallToolResult:
    """Retrieve simulated CURRENT status of an order.

    Use when asked 'What is the status?', 'Has it shipped?', or 'Is it delayed?'.
    Returns a normal result, or a structured MCP execution error with
    errorCategory, isRetryable, description, recoveryAction.
    Example demonstration IDs: ORD-1001 transient once, ORD-1003 business,
    ORD-1004 permission, ORD-9999 valid empty. ORD-ABCD validation.
    Do not use for ETA-only, refunds, cancellation, or address changes.

    Args:
        order_id: User-supplied order identifier, normally ORD-1234.
    """
    logger.info("MCP TOOL INVOKED | get_order_status | %s", order_id)
    check = checked_order(order_id)
    if check is not None:
        return check
    return result(lookup_status(order_id.upper()))


@mcp.tool()
def get_delivery_eta(order_id: str) -> CallToolResult:
    """Retrieve a separate simulated estimated arrival date.

    Use when asked 'When will my order arrive?' or 'What is its ETA?'.
    For combined status and ETA questions, Claude may call both tools.
    Uses the same demonstration error rules as get_order_status.

    Args:
        order_id: User-supplied order identifier, normally ORD-1234.
    """
    logger.info("MCP TOOL INVOKED | get_delivery_eta | %s", order_id)
    check = checked_order(order_id)
    if check is not None:
        return check
    return result(lookup_eta(order_id.upper()))


if __name__ == "__main__":
    mcp.run(transport="stdio")
