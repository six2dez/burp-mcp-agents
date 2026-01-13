# Ollama Backend (Fully Local)

This backend runs the Burp MCP Agents entirely on your machine using Ollama.

No cloud.
No API keys.
No external data exposure.

This is a local-only analysis workflow wired directly into Burp.

---

## What you get

• Passive vulnerability discovery  
• IDOR / auth bypass / SSRF / logic flaw triage  
• Automated report writing  
• Full local data control  
• Zero cloud dependency  

---

## Requirements

| Component | Required |
|----------|----------|
| Burp Suite | Community or Pro |
| Burp MCP Server | Enabled |
| Caddy | Reverse proxy |
| Ollama | Installed |
| Python 3.10+ | Required |

## Ports

- Burp MCP Server: `127.0.0.1:9876`
- Caddy proxy: `127.0.0.1:19876`
- Ollama default: `127.0.0.1:11434`

If your Ollama server uses a custom host/port, set `OLLAMA_HOST`.

---

## Architecture

```

Burp MCP Server → Caddy → Python MCP Agent → Ollama model

````

---

## 1. Install Ollama

https://ollama.com

Verify:

```bash
ollama --version
````

---

## 2. Install dependencies

```bash
cd ollama
python3 -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```

---

## 3. Start Ollama

```bash
ollama serve
```

---

## 4. Start Caddy

Follow:

```
common/caddy_setup.md
```

---

## 5. Run the agent

```bash
python3 ollama_mcp_agent.py deepseek-r1:14b
```

## Optional launcher

To simplify startup and auto-shutdown of Caddy, use the provided launcher.

Source it into your shell:

```bash
source /path/to/burp-mcp-agents/ollama/burpollama.sh
```

Then run:

```bash
burpollama deepseek-r1:14b
```

This will:
• Start Caddy
• Launch the Ollama MCP agent
• Automatically stop Caddy when the agent exits

To make this available in every shell, add the `source` line to your `~/.zshrc`.

## Quick verification

1) Confirm the SSE proxy works:

```bash
curl -i http://127.0.0.1:19876/sse
```

2) Confirm the agent connects and lists tools:

```bash
python3 ollama_mcp_agent.py deepseek-r1:14b
```

You should see a tool list after connection.

## Test it

```
From Burp history, find endpoints that use numeric IDs and lack Authorization headers.
```

```
Using Burp MCP, identify possible SSRF parameters and rank them by risk.
```

```
From Burp evidence, write a full vulnerability report with reproduction, impact and remediation.
```

## Troubleshooting

- 403 or Origin errors: Caddy is not running or not used.
- `Model not found locally`: the agent will pull it; ensure Ollama is running.
- Empty tool list: Burp MCP Server extension is not enabled.

---

## Example models

| Model           | VRAM  | Quality   |
| --------------- | ----- | --------- |
| deepseek-r1:14b | 16GB  | Excellent |
| gpt-oss:20b     | 20GB  | Excellent |
| llama3.1:70b    | 48GB+ | Very large |

---

## Example usage

```
List all endpoints that use numeric IDs and lack Authorization headers.
```

```
Identify potential SSRF parameters and rank them by risk.
```

```
Write a vulnerability report from Burp evidence.
```

---

## Why Ollama

Ollama gives full privacy and offline operation.

This backend is ideal for restricted environments and internal red teams.

---

## Privacy

All traffic stays on your machine.
No telemetry.
No cloud.

---

## Next

Build hunters from `prompts/` to automate passive recon.
