# Burp MCP Agents

Practical setup guides and helpers to connect Burp Suite MCP Server to multiple AI backends (Codex, Gemini, Ollama).

This repo focuses on wiring, safety-first workflows, and reusable prompts to analyze real Burp traffic.

No fuzzing.
No blind scanning.
Only real traffic + reasoning.

---

## What this is

Burp MCP Agents is a collection of:

• Backend setup guides (Codex, Gemini, Ollama)
• Caddy proxy configuration for MCP SSE
• Prompt templates for passive analysis and reporting

---

## Architecture

```yaml
Burp Suite MCP Server
▲
│
MCP Bridge
│
┌─────────────────────────────┐
│              │              │
Codex CLI   Ollama Agent   Gemini CLI
```

---

## Supported Backends

| Backend | Mode | Privacy | Difficulty |
|--------|-----|--------|------------|
| Codex CLI | Cloud | Medium | Easy |
| Ollama | Local | Full | Advanced |
| Gemini CLI | Cloud | Medium | Easy |

---

## Quick start

All setups require:

1. Burp MCP Server plguin enabled
2. Caddy reverse proxy (see `common/caddy_setup.md`)
3. One backend of your choice

### Install the Burp MCP Server extension

1) Download the Burp MCP Server extension (MCP server jar) from:
   https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc
2) In Burp Suite: `Extender` → `Extensions` → `Add` → select the jar or from BApp Store.
3) Start the extension and confirm it listens on `127.0.0.1:9876`.

---

## Codex CLI

See: `codex/README.md`

**Example models**

| Model | Use |
|------|----|
| gpt-5.2-codex | General use |
| gpt-5.1 | Faster |
| gpt-5-mini | Low resource |

---

## Ollama (fully local)

See: `ollama/README.md`

**Example models**

| Model | VRAM | Quality |
|------|-----|--------|
| deepseek-r1:14b | 16GB | Excellent |
| gpt-oss:20b | 20GB | Excellent |
| llama3.1:70b | 48GB+ | Very large |

---

## Gemini CLI

See: `gemini-cli/README.md`

**Example models**

| Model | Notes |
|------|-----|
| gemini-2.0-flash | Fast |
| gemini-2.0-pro | Deeper reasoning |

---

## Prompts

The real power lives in `prompts/`:

| Prompt | Purpose |
|------|--------|
| passive_hunter.md | Broad passive vuln surfacing |
| idor_hunter.md | IDOR/BOLA discovery |
| auth_flow_mapper.md | Auth vs unauth access mapping |
| ssrf_redirect_hunter.md | SSRF/open redirect candidates |
| logic_flaw_hunter.md | Multi-step logic issues |
| session_scope_hunter.md | Token scope/audience misuse |
| rate_limit_abuse_hunter.md | Rate-limit and abuse gaps |
| report_writer.md | Evidence-based reporting |

See `prompts/README.md` for usage guidance.

---

## Optional launchers

You can use the backend launchers to auto-start Caddy and shut it down when the
backend exits.

Source them directly:

```bash
source /path/to/burp-mcp-agents/codex/burpcodex.sh
source /path/to/burp-mcp-agents/gemini-cli/burpgemini.sh
source /path/to/burp-mcp-agents/ollama/burpollama.sh
```

Then run:

```bash
burpcodex
burpgemini
burpollama deepseek-r1:14b
```

To make these available in every shell, add the `source` lines to your
`~/.zshrc`.

---

## What this enables

You are not running a scanner.
You are reviewing real traffic with assisted reasoning.
