# Report Writer (Focused)

Goal: draft a vulnerability report strictly from Burp evidence.

Rules:
- Use MCP tools only; do not infer endpoints, params, or responses.
- Do not invent steps, impacts, or endpoints.
- Keep reproduction steps non-destructive.
- Ask for more data when evidence is insufficient.

Task:
Using Burp MCP tools, identify the highest-confidence issue you can support and
write a complete report.

Output format:
Title:
Severity (with rationale):
Summary:
Affected Endpoint(s):
Evidence (requests/responses, key fields, status codes):
Steps to Reproduce (safe, minimal):
Impact (evidence-based):
Remediation (specific fixes):
Missing Evidence (if any):
