# Auth Flow Mapper (Focused)

Goal: build an authenticated/unauthenticated access map and highlight likely
access-control gaps using only Burp evidence.

Rules:
- Use MCP tools only; do not infer endpoints, params, or responses.
- Only report issues supported by evidence.
- Keep confirmation steps non-destructive.
- Ask for more data when evidence is insufficient.

Task:
1) Enumerate endpoints grouped by host and auth state:
   - authenticated (cookies/tokens present)
   - unauthenticated (no auth artifacts)
   - mixed (both observed)
2) For mixed endpoints, compare response characteristics:
   - status code, content-type, response length
   - presence/absence of sensitive fields
3) Identify candidates for broken access control or missing auth checks.
4) Provide safe confirmation steps using existing sessions.

Output format:
- Host: <host>
  - Endpoint: <method> <path>
    - Auth states observed: <authenticated|unauthenticated|mixed>
    - Evidence: <exact observed differences>
    - Risk: <potential access-control issue>
    - Confidence: <low|medium|high>
    - Confirmation: <safe steps>
