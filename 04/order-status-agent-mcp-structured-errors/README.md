# Example 4 — Structured MCP Error Responses (Claude + MCP)

This extends Example 3 (two MCP tools) with **real MCP `CallToolResult`** responses. A tool execution failure returns `isError: true` with structured application metadata in `structuredContent` (`errorCategory`, `isRetryable`, `description`, `recoveryAction`). Both `get_order_status` and `get_delivery_eta` are exposed via one stdio MCP server. The FastAPI application discovers them using MCP `tools/list` and executes through MCP `tools/call`.

## Run on Mac

```bash
cd order-status-agent-mcp-structured-errors
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY and an available ANTHROPIC_MODEL
python -m uvicorn app:app --reload --port 8003
```

Open http://localhost:8003. MCP runs as a subprocess; no second terminal is required. This example uses **MCP 1.x** (`mcp>=1.28,<2`) because the source imports `mcp.server.fastmcp.FastMCP`.

## Demonstrations (click the sample buttons in the UI)

| Input | MCP response | Recovery |
|---|---|---|
| Check ORD-1234 | `isError=false` | Claude summarizes random mock status |
| Check ORD-1001 | `isError=true`, `transient`, retryable on first call, then successful | Claude may retry the same call once |
| Check ORD-ABCD | `isError=true`, `validation`, not retryable | Ask for a correctly formatted ID |
| Check ORD-1003 | `isError=true`, `business`, not retryable | Explain hold, refer to support |
| Check ORD-1004 | `isError=true`, `permission`, not retryable | Escalate to authorized staff |
| Check ORD-9999 | `isError=false`, `found=false` | Explain no order found; no retry |

The model is asked to follow these behaviors, but `tool_choice=auto` means routing and retries are not perfectly deterministic. The host allows at most two attempts for a transient tool+order combination and at most five Claude rounds. ORD-1001 resets on each new chat API request because each request launches a fresh MCP subprocess.

## Example tool execution error (MCP result)

```json
{
  "isError": true,
  "content": [{"type": "text", "text": "{...structured error as JSON...}"}],
  "structuredContent": {
    "errorCategory": "transient",
    "isRetryable": true,
    "description": "Mock order service is temporarily unavailable on this first request.",
    "recoveryAction": "Retry the same tool call once."
  }
}
```

`isError`, `content`, and `structuredContent` are MCP fields. The fields nested inside `structuredContent` are **your own tool-contract conventions**, not fixed MCP protocol keys.

## Distinguish protocol errors

An unknown tool requested using MCP `tools/call` is a **JSON-RPC protocol error** (top-level `error` with code and message), not the above tool execution result. This demo focuses on execution errors, avoiding malformed protocol calls from the main UI. To teach both, compare the protocol illustration in the flowchart or use MCP Inspector to manually call an unknown tool. Claude is passed the execution-result metadata for recovery; the host typically handles protocol failures.

**Do not use this simulated API in production.** For real services, bound retries, implement backoff for transient failures, secure access checks, and do not expose private authentication details in client-visible errors.
