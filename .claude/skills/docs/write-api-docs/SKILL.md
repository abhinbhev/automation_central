---
name: write-api-docs
description: Generate API reference documentation from source code, OpenAPI specs, or a description — covers endpoints, auth, request/response schemas, and error codes
domain: docs
requires_script: false
---

## Usage

Invoke with `/write-api-docs` then provide one of:
- A path to the API source code (FastAPI, Flask, Azure Functions, etc.) — the agent will read the route definitions
- An OpenAPI/Swagger spec file (`.json` or `.yaml`)
- A description of the API if no code exists yet

Optionally specify:
- **Audience:** internal consumers | external partners | public
- **Format:** Markdown (default) | OpenAPI YAML | table-only reference

## Output

A complete API reference at `docs/api/<service-name>.md`:

```markdown
# [Service Name] API Reference

**Version:** x.y
**Base URL:** `https://<host>/api/v1`
**Auth:** [Bearer token / API key / OIDC — how to obtain and pass it]
**Last updated:** YYYY-MM-DD | **Owner:** [team]

---

## Authentication

[How to authenticate. Include token format, header name, and how to obtain credentials.
Never include actual tokens — reference the secret store.]

---

## Endpoints

### POST /resource

**Description:** [What this endpoint does in one sentence]
**Auth required:** Yes / No
**Rate limit:** X req/min (if applicable)

**Request**

```http
POST /api/v1/resource
Authorization: Bearer <token>
Content-Type: application/json

{
  "field_one": "string",       // required — description
  "field_two": 42,             // optional — description, default: 0
}
```

**Response — 200 OK**

```json
{
  "id": "uuid",
  "status": "created",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error responses**

| Code | Meaning | When it occurs |
|------|---------|----------------|
| 400 | Bad Request | Missing required field |
| 401 | Unauthorized | Token missing or expired |
| 404 | Not Found | Resource ID does not exist |
| 422 | Unprocessable Entity | Field validation failed |
| 500 | Internal Server Error | Unexpected server failure |

---

## Data Models

### ResourceModel

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string (UUID) | Yes | Unique identifier |
| name | string | Yes | Display name, max 100 chars |
| status | enum | Yes | `active`, `inactive`, `pending` |

---

## Examples

### Example: Create a resource (Python)

```python
import httpx

response = httpx.post(
    "https://<host>/api/v1/resource",
    headers={"Authorization": f"Bearer {token}"},
    json={"field_one": "value"},
)
response.raise_for_status()
print(response.json())
```

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | YYYY-MM-DD | Added `field_two` to POST /resource |
```

## Steps

1. Read the source code or spec file; identify all routes, methods, and schemas
2. Infer request/response shapes from type annotations, Pydantic models, or docstrings
3. If auth is unclear, ask — do not guess
4. Draft the full reference — every endpoint documented, all fields listed
5. Flag any endpoint where behaviour could not be confirmed from the code
6. Show for review; confirm base URL and auth mechanism before writing
7. Write to `docs/api/<service-name>.md` on approval
