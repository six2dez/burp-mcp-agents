# Prompts

These prompts are designed for bug hunters and pentesters. They only use real
Burp traffic via MCP tools and avoid destructive actions.

## How to use

1) Browse the target normally so Burp has traffic.
2) Open your backend (Codex, Gemini, or Ollama).
3) Paste a prompt from this folder and run it.
4) If the model asks for more evidence, capture it in Burp and retry.

## Tips

- Start with `passive_hunter.md` to map the surface.
- Use focused hunters for deeper analysis (IDOR, SSRF, logic flaws).
- For reporting, use `report_writer.md` after you have evidence.

## Safety

- Keep all confirmation steps non-destructive.
- Only analyze systems you are authorized to test.
