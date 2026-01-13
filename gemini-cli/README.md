# Gemini CLI Backend

This backend connects **Gemini CLI** to **Burp MCP Server** (via the local Caddy SSE proxy), so Gemini can call Burp tools directly for traffic triage and vulnerability reasoning.

---

## What you get

- Analysis on top of real Burp traffic (via MCP tools)
- Faster triage: endpoints, params, auth context, reflections, errors
- Vulnerability candidates: IDOR/BOLA, access control, SSRF, open redirect, logic flaws
- No need to copy/paste raw requests

---

## Requirements

| Component | Required |
|---|---|
| Burp Suite | Community or Pro |
| Burp MCP Server extension | Enabled (listening on `127.0.0.1:9876`) |
| Caddy | Reverse proxy for SSE header constraints |
| Gemini CLI | Installed + authenticated |

## Ports

- Burp MCP Server: `127.0.0.1:9876`
- Caddy proxy: `127.0.0.1:19876`

---

## Architecture

```

Burp MCP Server (127.0.0.1:9876) → Caddy (127.0.0.1:19876) → Gemini CLI MCP (SSE)

````

Gemini CLI supports MCP servers via **SSE, stdio, or streamable HTTP**, configured in `settings.json`.  
This setup uses **SSE**.  
Reference: MCP servers + `mcpServers` config. :contentReference[oaicite:0]{index=0}

---

## 1) Install Gemini CLI

Recommended install (NPM):

```bash
npm install -g @google/gemini-cli
gemini --version
````

Reference: official install docs. ([Gemini CLI][1])

(Alternative: Homebrew exists, but avoid double-installing via npm + brew.)

---

## 2) Make sure Burp MCP + Caddy are working

Follow the common Caddy setup in:

* `common/caddy_setup.md`

Then verify the SSE endpoint is reachable:

```bash
curl -i http://127.0.0.1:19876/sse
```

You should see `Content-Type: text/event-stream` and an `event: endpoint` line.

---

## 3) Configure Burp MCP server in Gemini CLI

Gemini CLI reads MCP server configs from `settings.json`, typically:

* User scope: `~/.gemini/settings.json`

Add this:

```json
{
  "mcpServers": {
    "burp": {
      "url": "http://127.0.0.1:19876/sse",
      "trust": false,
      "timeout": 600000
    }
  }
}
```

Notes:

* `url` is the SSE endpoint.
* `trust: false` keeps confirmations enabled (recommended).
* `timeout` defaults to 10 minutes; set explicitly if you want.
  Reference: MCP server configuration structure (`mcpServers`, `url`, `trust`, `timeout`). ([Gemini CLI][2])

### Optional: manage MCP servers via CLI

Gemini CLI also supports managing MCP servers without editing JSON manually:

```bash
gemini mcp add burp http://127.0.0.1:19876/sse
```

Reference: `gemini mcp add` exists and writes to user/project settings. ([Gemini CLI][2])

---

## 4) Start Gemini CLI and verify MCP connection

Start:

```bash
gemini
```

Inside Gemini CLI:

```text
/mcp
```

You should see `burp` listed with its available tools/resources (if any).
Reference: `/mcp` shows connected servers, tools, resources. ([Gemini CLI][2])

## Optional launcher

To simplify startup and auto-shutdown of Caddy, use the provided launcher.

Source it into your shell:

```bash
source /path/to/burp-mcp-agents/gemini-cli/burpgemini.sh
```

Then run:

```bash
burpgemini
```

This will:
• Start Caddy
• Launch Gemini CLI
• Automatically stop Caddy when Gemini exits

To make this available in every shell, add the `source` line to your `~/.zshrc`.

## Quick verification

```bash
curl -i http://127.0.0.1:19876/sse
```

Inside Gemini CLI:

```text
/mcp
```

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

---

## 5) Model selection (recommended)

Inside Gemini CLI:

```text
/model
```

Suggested: use **Auto (Gemini 2.5)** for mixed workloads, switch to **Pro** when you need deeper reasoning.
Reference: `/model` + Auto/Pro/Flash guidance and supported models. ([Gemini CLI][3])

You can also start with a specific model:

```bash
gemini -m "gemini-2.5-pro"
# or
gemini -m "gemini-2.5-flash"
```

Reference: CLI supports `-m/--model` and `/model`. ([Gemini CLI][3])

---

## 6) Example prompts (safe, non-destructive)

Paste any of these after you’ve browsed normally through the target so Burp has traffic.

### Passive endpoint & auth mapping

```text
Using the Burp MCP tools, list the top 30 unique endpoints and group them by host and auth state (authenticated vs unauthenticated). Only use real Burp data.
```

### IDOR / BOLA candidate finder

```text
From Burp traffic, identify endpoints that look like object access (numeric IDs, UUIDs, usernames). For each candidate, explain why it’s suspicious and propose a non-destructive confirmation plan.
```

### SSRF / redirect parameter surfacing

```text
Find parameters that look like URLs/hosts/redirects/callbacks. Rank them by SSRF/open-redirect likelihood and suggest safe probes (no exploitation).
```

### Report drafting from evidence

```text
Draft a vulnerability report template based only on Burp evidence: affected endpoint(s), steps to reproduce (safe), impact, remediation, and proof snippets.
```

---

## Troubleshooting

### Burp MCP blocks requests (Origin/Host constraints)

If you see 403/Origin-related blocks, keep using the Caddy proxy described in `common/caddy_setup.md`.
Gemini CLI supports custom headers for MCP `url`, but Burp MCP constraints can be strict; the proxy is the most reliable fix. ([Gemini CLI][2])

### “Server not visible in /mcp”

* Confirm `curl -i http://127.0.0.1:19876/sse` works
* Confirm `~/.gemini/settings.json` is valid JSON
* Restart `gemini`

### MCP tool list is empty

* Confirm the Burp MCP Server extension is enabled
* Confirm Burp is listening on `127.0.0.1:9876`

---

## Why Gemini CLI

* Native MCP support (SSE/stdio/streamable HTTP) ([Gemini CLI][2])
* Fast iteration with `/mcp` and `/model`
* Solid reasoning with Auto/Pro/Flash routing ([Gemini CLI][3])


[1]: https://geminicli.com/docs/get-started/installation/?utm_source=chatgpt.com "Gemini CLI installation, execution, and deployment"
[2]: https://geminicli.com/docs/tools/mcp-server/ "MCP servers with the Gemini CLI | Gemini CLI"
[3]: https://geminicli.com/docs/cli/model/ "Gemini CLI model selection (`/model` command) | Gemini CLI"
