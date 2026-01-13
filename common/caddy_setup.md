# Caddy Reverse Proxy Setup

Burp MCP Server enforces strict Origin/Host validation and currently rejects
many default HTTP headers sent by modern MCP clients (Codex, Gemini, Ollama),
causing 403 errors and MCP handshake failures.

This proxy normalizes MCP traffic and ensures reliable SSE connectivity.

This component is needed for most setups.

---

## Architecture

```

Burp MCP Server (127.0.0.1:9876)
▲
│
Caddy Proxy
│
Clients (Codex / Gemini / Ollama)

```

Caddy listens on:

```

127.0.0.1:19876

````

and forwards normalized traffic to Burp MCP.

Ports used:
- Burp MCP Server: 127.0.0.1:9876
- Caddy proxy: 127.0.0.1:19876

---

## Install Caddy

### macOS
```bash
brew install caddy
````

### Linux

```bash
sudo apt install -y caddy
```

---

## Use the repo Caddyfile

This repo includes a ready-to-use Caddyfile:

```
/path/to/burp-mcp-agents/common/Caddyfile
```

---

## Start Caddy

```bash
caddy run --config /path/to/burp-mcp-agents/common/Caddyfile
```

---

## Verify

```bash
curl -i http://127.0.0.1:19876/sse
```

You should see:

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
event: endpoint
```

If you see `403` or Origin-related errors, Caddy is not running or not being used.

---

## Why this is needed

Burp MCP SSE currently enforces:

• strict Origin validation
• limited header acceptance
• DNS rebinding protection

Most MCP clients violate these constraints by default.

This proxy ensures compatibility and stable operation.

---

## Do not expose this proxy externally

Caddy must remain bound to `127.0.0.1` only.
This stack is designed for local, trusted use only.

---

## Next

Proceed to configure your chosen backend (Codex / Ollama / Gemini).
