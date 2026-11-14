# Order Status Agent — Claude + MCP (second demo)

This is the **MCP version** of the same order-status application. It still uses Claude and the same random-status mock API, but the agent now connects to a **separate MCP server process** rather than importing the API function directly.

## Architecture

```text
Browser (static/index.html)
  → FastAPI (app.py)
  → MCP client opens stdio connection → MCP server (mcp_server.py)
      MCP tools/list → returns tool description + input schema
  → Claude API (tool_choice=auto, tools discovered from MCP)
      returns tool_use or text
  → If tool_use: MCP tools/call → mcp_server.py → order_api.py
      returns tool_result
  → Claude API again → final natural-language answer
```

**This is genuine MCP:** the application uses MCP `initialize`, `tools/list`, and `tools/call` over stdio. Claude is still responsible for tool selection. This is a client-hosted MCP bridge, *not* Anthropic's remote MCP connector feature. The MCP server launches automatically as a local child process for a request; no separate terminal is required.

## Run (macOS/Linux)

1. `cd order-status-agent-mcp`
2. `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `python -m pip install -r requirements.txt`
5. `cp .env.example .env` and set your real `ANTHROPIC_API_KEY` in `.env` (never commit it).
6. `python -m uvicorn app:app --reload`
7. Open http://127.0.0.1:8000

If your original demo is using port 8000, use `python -m uvicorn app:app --reload --port 8001` and open http://127.0.0.1:8001.

## Demo queries
- `Check status of ORD-1234` → Claude should select the MCP `get_order_status` tool.
- `Where is my order?` → Claude should ask for an ID, no MCP `tools/call`.
- `Cancel order ORD-4567` → Claude should decline, no MCP `tools/call`.
- `Is ORD-5678 delayed?` → Claude requests MCP tool; random response can be anything.

## What to look for in terminal logs

```text
MCP SESSION INITIALIZED
MCP TOOLS DISCOVERED: ['get_order_status']
CALLING CLAUDE | round=1 | tool_choice=auto
CLAUDE SELECTED TOOL | get_order_status | args={'order_id': 'ORD-1234'}
INVOKING MCP TOOL | tools/call | get_order_status
MCP SERVER | MCP TOOL INVOKED | get_order_status | order_id=ORD-1234
MCP TOOL RESULT | ...
RETURNING MCP RESULTS TO CLAUDE | next loop iteration
CALLING CLAUDE | round=2 | tool_choice=auto
CLAUDE FINAL RESPONSE | no further tool calls | ...
```

When Claude doesn't select a tool, you should see `CLAUDE FINAL RESPONSE` without `CLAUDE SELECTED TOOL` or `INVOKING MCP TOOL`. Note: tool **discovery** may still occur even when there is no invocation.

## Files
- `app.py` — FastAPI, MCP client, Claude loop, validation, logging.
- `mcp_server.py` — real MCP server and MCP tool description/schema generated from Python annotations and docstring.
- `order_api.py` — identical simulated order API from Demo 1.
- `static/index.html` — familiar UI with MCP trace and dynamically discovered tool schema.
- `.env.example` / `requirements.txt` — configuration.

## Notes
- The mock API produces a **new random status on each call**.
- The server writes logs to **stderr**, not stdout (stdout carries the stdio MCP protocol).
- No API key is required for the MCP server; the Anthropic key is for Claude.
- Each HTTP chat request starts a fresh chat and a fresh MCP session, to keep this demo simple.
- `tool_choice=auto` means Claude may choose no tool. A missing order ID is answered without calling the mocked API.
- If API authentication fails, check your Anthropic key and model access.
