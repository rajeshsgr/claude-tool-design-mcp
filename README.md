# Claude Tool Design & MCP — Hands-on Examples

Four progressive Python demos illustrating Claude tool calling, Model Context Protocol (MCP), multiple tool selection, and structured error recovery. Each uses simulated order data; no real order system is connected.

## Examples

| Example | Concept | Application | Port |
|---|---|---|---|
| 01 | Direct Python tool calling | [Order Status Agent](01/order-status-agent/) | 8000 |
| 02 | MCP tool discovery and execution | [Order Status Agent with MCP](02/order-status-agent-mcp/) | 8001 |
| 03 | Multiple MCP tools and dynamic selection | [Two-tool agent](03/order-status-agent-mcp-two-tools/) | 8002 |
| 04 | Structured errors and recovery | [Structured error agent](04/order-status-agent-mcp-structured-errors/) | 8003 |

[**Architecture flowcharts for all four examples**](order-status-four-examples-flowchart.html) — download or clone and open locally in a browser.

## Prerequisites

- Python 3.10+ (or the version specified by the individual demo)
- Anthropic API key with API credits and access to the configured Claude model
- MCP Python SDK v1 for examples 02–04 (`mcp<2`), compatible with `FastMCP`

## Run locally

Clone this repository and enter the application directory for the example you want to run. For example:

```bash
cd 01/order-status-agent
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Set `ANTHROPIC_API_KEY` in `.env` and select a supported model using `ANTHROPIC_MODEL`. Never commit your key. For examples 02–04, ensure the installed MCP SDK is v1:

```bash
python -m pip install 'mcp<2'
```

Start the application (change the port according to the table above):

```bash
python -m uvicorn app:app --reload --port 8000
```

Open http://localhost:8000. MCP servers in examples 02–04 are launched by the application through stdio; no separate server startup is necessary.

## Demo prompts

- Example 01 and 02: `Check status of ORD-1234` or `Hello`.
- Example 03: `What is the status and delivery date of ORD-1234?`.
- Example 04: check `ORD-1001` (transient), `ORD-ABCD` (validation), `ORD-1003` (business), `ORD-1004` (permission), or `ORD-9999` (empty result).

Tool choices and retries are model decisions; simulated results may vary. The terminal logs and web UI traces help illustrate the execution flow.

## Core learning

The first LLM call determines whether a tool is needed. Application code executes the selected tool directly or via MCP. The tool result is returned to Claude for a subsequent LLM call to generate a final answer or request another tool. Structured errors give the agent actionable recovery information.

These examples are educational demos, not production-ready services.
