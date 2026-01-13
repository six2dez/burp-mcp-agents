# Session Scope / Token Misuse Hunter (Focused)

Goal: detect weak session scoping and token misuse from Burp evidence.

Rules:
- Use MCP tools only; do not infer endpoints, params, or responses.
- Only report issues supported by evidence.
- Keep confirmation steps non-destructive.
- Ask for more data when evidence is insufficient.

Task:
1) Identify auth tokens/cookies and their usage across hosts/paths.
2) Look for tokens used across different tenants, roles, or subdomains.
3) Check for missing audience or scope enforcement signals.
4) Provide safe confirmation steps using already captured sessions.

Output format:
- Token/Cookie: <name>
  - Observed usage: <hosts/paths>
  - Risk: <scope or audience issue>
  - Evidence: <exact request/response detail>
  - Confidence: <low|medium|high>
  - Confirmation: <safe steps>
