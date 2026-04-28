---
mode: agent
description: Generate API reference documentation from source code, an OpenAPI spec, or a description — endpoints, auth, schemas, error codes, examples
---

Generate API reference documentation for the following service or API.

**Input — provide one of:**
- A path to the API source code (FastAPI, Flask, Azure Functions, etc.)
- An OpenAPI/Swagger spec file (`.json` or `.yaml`)
- A description of the API if no code exists yet

**Optionally specify:**
- Audience: `internal` (default) | `external partner` | `public`
- Format: `markdown` (default) | `openapi-yaml` | `table-only`

**Clarify before writing if:**
- Base URL / environment URLs are not obvious from the code
- Authentication mechanism is unclear — never guess; always ask

---

## API docs structure (always produce all sections)

```markdown
# [Service Name] API Reference

**Version:** x.y | **Base URL:** `https://<host>/api/v1`
**Auth:** [mechanism and how to obtain credentials]
**Last updated:** YYYY-MM-DD | **Owner:** [team]

---

## Authentication
[Token format, header name, how to obtain — reference secret store, never include real tokens]

---

## Endpoints

### [METHOD] /path

**Description:** [one sentence]
**Auth required:** Yes / No | **Rate limit:** X req/min

**Request**
[HTTP block with headers and body, annotated with field descriptions]

**Response — 200 OK**
[JSON response block]

**Error responses**
| Code | Meaning | When it occurs |
|------|---------|----------------|

---

## Data Models

[Table per model: field | type | required | description]

---

## Examples

[Working code example in Python using httpx — real structure, placeholder values only for secrets/URLs]

---

## Changelog
| Version | Date | Change |
```

**Rules:**
- Read every route definition and Pydantic/dataclass model before writing
- Every field in request and response bodies must be documented
- Flag any endpoint whose behaviour could not be confirmed from the code
- Never include real tokens, passwords, or connection strings — use `<token>` placeholders
- Show for review before writing to `docs/api/<service-name>.md`
