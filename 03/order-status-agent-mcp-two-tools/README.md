# Example 3 — Claude MCP Agent with TWO tools

Two MCP tools are discovered dynamically from a local MCP server:
- `get_order_status(order_id)` — simulated random status from `order_api.py`
- `get_delivery_eta(order_id)` — simulated delivery date from `delivery_api.py`

Claude chooses one or both, with `tool_choice={"type":"auto"}`. The app logs discovery, selection, execution, and returns the tool results to Claude for the final response.

## Run (Mac)

```bash
cd order-status-agent-mcp-two-tools
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Edit .env to set ANTHROPIC_API_KEY
python -m uvicorn app:app --reload --port 8002
```

Open http://localhost:8002.

### Demo prompts

- `Check status of ORD-1234` → status tool
- `When will ORD-1234 arrive?` → ETA tool
- `What is the status and ETA of ORD-1234?` → potentially both tools
- `Hello` → no tool
- `Cancel ORD-1234` → unsupported

Tool choice is controlled by Claude, so exact selections are not guaranteed. The application enforces name, argument shape, and user-supplied order-ID validation. There is no persistence or real tracking. The two mocks are intentionally independent and their results may disagree.

## Claude Code project configuration

For Claude Code, copy `.mcp.json.example` to `.mcp.json` and replace `/ABSOLUTE/PATH/TO` with your machine's real project path. Then run `claude` in this directory and inspect `/mcp`. These Claude Code configuration files are not read by the FastAPI MCP client.

## SDK version

The code uses `FastMCP` from the v1 MCP SDK. `requirements.txt` pins `mcp>=1.28,<2` to avoid the v2 breaking change.
