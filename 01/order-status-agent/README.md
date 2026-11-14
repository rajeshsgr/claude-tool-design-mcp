# Order Status Agent — Claude Tool Calling Demo

A small FastAPI app demonstrating Claude choosing a tool (`tool_choice={"type":"auto"}`) and a Python mock order-status API randomly returning an order status.

## Run

Requires Python 3.10+ and an Anthropic API key with access to the selected model.

```bash
cd order-status-agent
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # Windows: copy .env.example .env
# Edit .env with ANTHROPIC_API_KEY=your_actual_key
uvicorn app:app --reload
```

Open http://127.0.0.1:8000.

## Files

- `app.py`: Claude Messages API calls, `tool_choice={"type":"auto"}`, tool-call loop, validation and web endpoints.
- `tools.py`: Anthropic tool contract (name, description, `input_schema`) and function registry.
- `order_api.py`: simulated randomized order-status API.
- `static/index.html`: chat UI, tool trace, schema and prompt.

## Try

- `Where is ORD-1234?` → Claude calls `get_order_status`.
- `Where is my order?` → Claude requests order ID.
- `Cancel ORD-1234` → Claude explains this demo only checks status.

Claude emits `tool_use` with a name and input. Python validates and executes it, then appends a `tool_result` in a new user message. Claude responds with a summary. This demo has no fallback and does not use OpenAI.

Statuses are randomly generated per lookup, not fetched from a real store. Do not expose it as a public production service.
