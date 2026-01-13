# Passive Hunter (Focused)

Goal: surface high-confidence vulnerability candidates from real Burp traffic
without any active scanning or fuzzing.

Rules:
- Use MCP tools only; do not infer endpoints, params, or responses.
- Only report issues supported by evidence.
- Keep confirmation steps non-destructive.
- Ask for more data when evidence is insufficient.

Task:
1) Map the top 50 unique endpoints by host and method.
2) For each endpoint, extract concrete risk signals:
   - Missing auth on sensitive paths
   - Object identifiers in path/params (IDs, UUIDs, emails)
   - Reflection of user input or error details
   - Inconsistent status codes across similar requests
3) Prioritize candidates by impact and evidence quality.
4) Provide a minimal confirmation plan for each candidate.

Output format:
- Host: <host>
  - Endpoint: <method> <path>
    - Signals: <bullet list of concrete signals>
    - Evidence: <exact observed details>
    - Risk hypothesis: <issue type>
    - Confidence: <low|medium|high>
    - Confirmation: <safe steps>
