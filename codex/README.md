# Codex Backend

This backend connects **OpenAI Codex CLI** to Burp MCP Server so Codex can use Burp MCP tools for traffic analysis.

This is a straightforward backend to set up.

---

## What you get

• Passive vulnerability discovery  
• IDOR / auth bypass / SSRF / logic flaw triage  
• Automated report writing from Burp evidence  
• Zero fuzzing, zero blind scanning  
• No API keys required (ChatGPT account login works)

---

## Requirements

| Component | Required |
|----------|----------|
| Burp Suite | Community or Pro |
| Burp MCP Server | Enabled |
| Codex CLI | Installed |
| Caddy | Reverse proxy |

## Ports

- Burp MCP Server: `127.0.0.1:9876`
- Caddy proxy: `127.0.0.1:19876`

---

## Architecture

```

Burp MCP Server → Caddy (header sanitizer) → Codex CLI

```

---

## 1. Install Burp MCP Server

Install the Burp MCP Server extension from the Burp BApp Store and enable it:
https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc
In the extension tab, click **Extract server proxy jar** to download:

```
mcp-proxy.jar
```

This jar is the stdio MCP bridge Codex uses.

---

## 2. Install Codex CLI

Follow the official installation guide:

https://developers.openai.com/codex/guides/install

Authenticate using your ChatGPT account.

---

## 3. Configure Codex MCP

Edit:

```

~/.codex/config.toml

````

Add:

```toml
[mcp_servers.burp]
command = "java"
args = ["-jar", "/absolute/path/to/mcp-proxy.jar", "--sse-url", "http://127.0.0.1:19876"]
````

You can download `mcp-proxy.jar` from the Burp MCP Server extension page in the
Burp BApp Store (the download button provides the jar).

---

## 4. Configure Caddy

Follow:

```
common/caddy_setup.md
```

---

## 5. Start everything

```bash
caddy run --config /path/to/burp-mcp-agents/common/Caddyfile
codex
```

Verify:

```
/mcp
```

You must see:

```
burp   connected ✓
```

## Quick verification

1) Confirm the SSE proxy works:

```bash
curl -i http://127.0.0.1:19876/sse
```

2) Confirm Codex sees the MCP server:

```text
/mcp
```

## 6. Test it

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
- `burp` missing from `/mcp`: check `~/.codex/config.toml` and the SSE URL.
- Empty tool list: Burp MCP Server extension is not enabled.

---

## Optional launcher

To simplify startup and auto-shutdown of Caddy, use the provided launcher.

Source it into your shell:

```bash
source /path/to/burp-mcp-agents/codex/burpcodex.sh
```

Then simply run:

```bash
burpcodex
```

This will:
• Start Caddy
• Launch Codex
• Automatically stop Caddy when Codex exits

To make this available in every shell, add the `source` line to your `~/.zshrc`.

---

## Example models

| Model         | Notes        |
| ------------- | ------------ |
| gpt-5.2-codex | General use  |
| gpt-5.1       | Faster       |
| gpt-5-mini    | Low resource |

Switch models inside Codex:

```
/model gpt-5.2-codex
```

---

## Why Codex

Codex has native MCP support and solid reasoning performance.

---

## Privacy notes

Only analyze traffic you are authorized to access.
Sensitive tokens can be redacted before analysis.

---

## Next

Add hunters from `prompts/` to start passive recon automation.
