---
name: schema-docs
description: Document a database or data schema — tables, columns, types, relationships, and business context. Accepts SQL DDL, JSON Schema, or a description. Can run schema_documenter.py to introspect live databases.
domain: data-ml
requires_script: true
script: scripts/data/schema_documenter.py
---

## Usage

Invoke with `/schema-docs` then provide one of:
- SQL DDL (`CREATE TABLE ...` statements)
- JSON Schema definition
- A database connection + table names (for live introspection via the script)
- A description of the tables and their relationships

Optionally provide:
- Business context: what does this data represent?
- Audience: `technical` (includes types, constraints) or `business` (plain-language descriptions)

## Output

A structured schema documentation document:

```markdown
# Schema: <schema/database name>
**Last updated:** YYYY-MM-DD
**Source system:** [name]
**Owner:** [team]

## Overview
[2-3 sentences describing what this schema represents and how it's used]

## Tables

### `orders`
| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| order_id | BIGINT | No | Primary key. Unique identifier for each order. |
| customer_id | BIGINT | No | FK → `customers.customer_id` |
| status | VARCHAR(20) | No | Order status: `pending`, `shipped`, `delivered`, `cancelled` |
| created_at | TIMESTAMP | No | UTC timestamp of order creation |

**Indexes:** `idx_orders_customer_id`, `idx_orders_created_at`
**Relationships:**
- `customer_id` → `customers.customer_id` (N:1)
- `order_id` → `order_items.order_id` (1:N)

## Entity Relationship Diagram

\`\`\`mermaid
erDiagram
  ORDERS {
    BIGINT order_id PK
    BIGINT customer_id FK
    VARCHAR status
    TIMESTAMP created_at
  }
  CUSTOMERS {
    BIGINT customer_id PK
    VARCHAR name
  }
  ORDERS }o--|| CUSTOMERS : "placed by"
\`\`\`

## Glossary
| Term | Definition |
|------|------------|
| order | A customer's purchase request containing one or more items |
```

## Steps

1. Parse the provided DDL, JSON Schema, or description
2. For each table/entity: extract column names, types, nullable, PKs, FKs
3. Write a plain-language description for each column (infer from name if not provided)
4. Identify relationships (FK references or described joins)
5. Generate the Mermaid ER diagram
6. Add a glossary for domain-specific terms
7. If live introspection is requested: call `scripts/data/schema_documenter.py`
8. Offer to save output as `.md` or post to Confluence

## Audience Modes

| Mode | Includes |
|------|---------|
| `technical` | Types, nullability, indexes, constraints, DDL snippets |
| `business` | Plain-language column descriptions, no DDL, ER diagram kept simple |
