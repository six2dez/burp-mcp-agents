#!/usr/bin/env python3
import argparse
import asyncio
import json
import subprocess
import shutil
import sys
from typing import Any, Dict, List

from mcp import ClientSession
from mcp.client.sse import sse_client  # official SDK SSE transport
from rich import print

import ollama


DEFAULT_BURP_SSE_URL = "http://127.0.0.1:19876/sse"

SYSTEM = """You are a vulnerability analyst sitting directly on Burp Suite.
Rules:
- Only use real data you obtain via MCP tools. Never assume.
- Keep confirmation steps non-destructive.
- If you need data, call tools instead of guessing.
"""


def ensure_model(model: str) -> None:
    """Pull model if not present locally."""
    if not shutil.which("ollama"):
        print("[red]Ollama binary not found in PATH.[/red] Install it from https://ollama.com")
        sys.exit(1)
    try:
        subprocess.run(["ollama", "show", model], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print(f"[yellow]Model not found locally: {model}. Pulling…[/yellow]")
        subprocess.run(["ollama", "pull", model], check=True)


def mcp_tools_to_ollama_tools(mcp_tools: List[Any]) -> List[Dict[str, Any]]:
    """
    Convert MCP tool definitions (name/description/inputSchema) into
    the 'tools' format that Ollama's chat() expects.
    """
    tools: List[Dict[str, Any]] = []
    for t in mcp_tools:
        # MCP tool typically has: t.name, t.description, t.inputSchema
        schema = getattr(t, "inputSchema", None) or {"type": "object", "properties": {}}
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": getattr(t, "description", "") or "",
                    "parameters": schema,
                },
            }
        )
    return tools


async def run_agent(model: str, burp_sse_url: str) -> None:
    ensure_model(model)

    print(f"[cyan]Connecting to Burp MCP (SSE):[/cyan] {burp_sse_url}")
    try:
        async with sse_client(url=burp_sse_url) as streams, ClientSession(*streams) as session:
            try:
                await session.initialize()
            except Exception as exc:
                print(f"[red]MCP initialization failed:[/red] {exc}")
                print("[yellow]Check Caddy on 127.0.0.1:19876 and Burp MCP on 127.0.0.1:9876.[/yellow]")
                return

            # Smoke test: list tools
            try:
                tools_resp = await session.list_tools()
            except Exception as exc:
                print(f"[red]MCP tool listing failed:[/red] {exc}")
                print("[yellow]If you see 403/Origin errors, ensure Caddy is running.[/yellow]")
                return
            tool_names = [t.name for t in tools_resp.tools]
            print(f"[green]Connected.[/green] Tools available: {tool_names}")

            ollama_tools = mcp_tools_to_ollama_tools(tools_resp.tools)

            messages = [{"role": "system", "content": SYSTEM}]
            print("[green]Ready.[/green] Type a question (Ctrl+C to exit).")

            while True:
                user = input("> ").strip()
                if not user:
                    continue

                messages.append({"role": "user", "content": user})

                # Ask the model (with tool definitions)
                resp = ollama.chat(
                    model=model,
                    messages=messages,
                    tools=ollama_tools,
                )

                msg = resp.get("message", {})
                content = msg.get("content", "") or ""
                tool_calls = msg.get("tool_calls") or []

                # If no tool calls, just print content
                if not tool_calls:
                    print(content)
                    messages.append({"role": "assistant", "content": content})
                    continue

                # Execute tool calls via MCP and feed results back
                for call in tool_calls:
                    fn = call.get("function", {})
                    name = fn.get("name")
                    args = fn.get("arguments") or {}

                    # Ollama sometimes returns arguments as JSON string
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except Exception:
                            args = {"raw": args}

                    print(f"[dim]→ calling MCP tool: {name}({args})[/dim]")
                    result = await session.call_tool(name, arguments=args)

                    # MCP returns content blocks; keep it simple as text/json
                    tool_result_payload = {
                        "tool": name,
                        "result": [getattr(c, "text", str(c)) for c in result.content],
                        "structured": getattr(result, "structuredContent", None),
                    }

                    messages.append(
                        {
                            "role": "tool",
                            "name": name,
                            "content": json.dumps(tool_result_payload, ensure_ascii=False),
                        }
                    )

                # Ask the model again with tool outputs
                resp2 = ollama.chat(model=model, messages=messages)
                msg2 = resp2.get("message", {})
                content2 = msg2.get("content", "") or ""
                print(content2)
                messages.append({"role": "assistant", "content": content2})
    except Exception as exc:
        print(f"[red]Connection failed:[/red] {exc}")
        print("[yellow]Ensure Caddy is running and the Burp MCP extension is enabled.[/yellow]")
        return


def main() -> None:
    p = argparse.ArgumentParser(description="Ollama + Burp MCP (SSE) agent")
    p.add_argument("model", help="Ollama model name (e.g. gpt-oss:20b, deepseek-r1:14b)")
    p.add_argument("--burp", default=DEFAULT_BURP_SSE_URL, help=f"Burp MCP SSE URL (default: {DEFAULT_BURP_SSE_URL})")
    args = p.parse_args()

    asyncio.run(run_agent(args.model, args.burp))


if __name__ == "__main__":
    main()
