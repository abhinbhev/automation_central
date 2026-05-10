---
name: scaffold-stored-procedure
description: "Interactively scaffold a Python dynamic-SQL stored-procedure class file from a fact-table schema and business spec — including helpers, public method, _build_query, and a runnable __main__ smoke test"
mode: agent
---

You are scaffolding a Python stored-procedure (SP) class file. One SP class per fact table. The class is a **dynamic-SQL builder** — it does not run queries itself; it returns a SQL string. Follow the 10-step interview below, then emit the complete file.

---

## Interview (run in order — batch related questions per step)

### Step 1 — Identity
Ask together:
- Full output file path (repo-agnostic). File name should follow `get_<domain>_kpis.py` convention (e.g. `get_impact_kpis.py`, `get_roi_kpis.py`, `get_price_kpis.py`).
- Method name (`snake_case`, must start with `get_`; class name = PascalCase, strip `get_` prefix)
- SQL dialect: Databricks SQL / Snowflake / BigQuery / Postgres / T-SQL / MySQL

### Step 2 — Fact table
Ask together:
- Fully-qualified table name
- All columns with types
- FK columns → which dim table each points to
- Measure columns (will be aggregated with SUM)
- Any dim attributes stored directly on the fact (denormalized — Variant C)

### Step 3 — Dimension tables
Loop until user says "done":
- FQN, primary key column, FK column on fact, columns to expose as filters/selects

### Step 4 — Time model
Offer **canonical default** (year int + period codes + period_type granularity). Only tailor if user explicitly flags a different model.

**Ask explicitly: is the time dimension at weekly or sub-monthly granularity?** If yes, `normalize_time`'s quarterly period-code logic (Q1/Q2/FY/H1/H2) will not apply — adapt to use `year` + `week_number` (or `iso_week`) instead, and drop `period`/`period_type` from the signature. Time parameters remain `year`, `quarter`, `week`, etc. — never encode periods as "Period A / Period B" text literals.

### Step 5 — Release-date semantics
One question: *"Quarterly publish cadence with 15th-of-next-quarter cutoff — keep, change, or omit?"* Default: keep.

### Step 6 — Helper methods
For helpers 3.1–3.4, present a one-line assumption and ask canonical / tailored / omit (default: canonical):
- `_sanitize_input` — blocks SQL-injection; regex `[a-zA-Z0-9\s_\-\.]`; ask if filter values may contain `&`, `/`, etc.
- `_escape_sql_string` — single-quote escaping + NULL handling; confirm single-quote dialect
- `_validate_year` — int-range guard 1900–2100; omit if no year column
- `_parse_filter_param` — splits on `|||#$#|||` or comma; ask if upstream uses a different delimiter

Helpers 3.5 (`_determine_current_period_info`) and 3.6 (`normalize_time`) are **auto-included** — no prompt — unless Steps 4/5 said omit.

### Step 7 — Per-filter configuration
For every filter parameter ask:
- Default when caller passes `None` — `["across"]` for dims, `["all"]` for demographics, `None` for strict-required
- Apply `_sanitize_input`? Yes for free-text (country, brand); no for enum-controlled (period codes, demographic buckets)
- Known value-fix hardcodes (e.g. `"megabrand" → "mega brand"`) — emit only what the user provides

### Step 8 — Measure pattern
Ask which variant:
- **A** — column-list whitelist; aggregate per selected measure; ask for full whitelist + default subset
- **B-kpi** — single `value` column; extra `kpi_dim(kpi, sub_kpi)`; filter on kpi/sub_kpi
- **B-imagery** — 1–2 fixed measures; `metric="across"` expands all; includes `debug_mode`
- **C** — denormalized fact; brand-attr filters in outer WHERE; no brand-dim subquery
- **D** (composite SP) — refuse; document as hand-write only

For Variants A, B-kpi, and C, **classify each measure column by aggregation type** (ask for each):

| Type | When to use | SQL pattern |
|---|---|---|
| **Additive** | Raw counts, volumes, costs, spend | `SUM(f.col)` |
| **Pre-computed ratio** | ROI, rates, shares stored as a result column | `SUM(f.col * w.weight) / NULLIF(SUM(w.weight), 0)` or `SUM(num) / NULLIF(SUM(den), 0)` |
| **Rate / index** | CPI, weather, distribution % — relative indices | `AVG(f.col)` |
| **Mixed-type** | One column storing spend AND rates depending on a type dim | `CASE WHEN LOWER(s.type) = 'x' THEN SUM(f.col) ELSE AVG(f.col) END` |

For **pre-computed ratios**, ask:
- Are numerator and denominator stored separately? → `SUM(num) / NULLIF(SUM(den), 0)`
- Only the ratio is stored? → ask for a weight column (volume/spend/units) and which table provides it → volume-weighted mean pattern; requires joining that table

For **mixed-type** signals, ask:
- Which dim column distinguishes the types? Which values → additive, which → rate?

**Guard weight-table JOINs** with a flag (e.g. `need_weight = "metric_name" in requested_metrics`) — only emit the JOIN when the weighted metric is requested.

### Step 9 — Runtime optimizations
Ask together:
- Are string filter columns stored lowercase in the warehouse? (affects whether to emit `LOWER(col)` or lowercase the input string)
- Fact table partition columns? (emit their filters first inside subquery WHERE)
- Any dims small enough to broadcast? (Databricks `/*+ BROADCAST(alias) */`)

### Step 10 — Smoke test
Ask for representative `__main__` values (single-country/entity call). Always emit a real invocation — never a placeholder.

---

## Generation rules

### File structure (top to bottom)
1. Module docstring — one line
2. Imports — `datetime`, `typing.Any`, `pandas` only if used, project logger (ask path) or `import logging; logger = logging.getLogger(__name__)`
3. Class declaration — PascalCase
4. Class docstring
5. Private helpers — in §3.1–3.6 order
6. Public method — flat-union signature; all filter params `str | None = None`; `release_date: datetime | None = None` last; optional `debug_mode: bool = False`
7. `_build_query(self, ...) -> str`
8. `if __name__ == "__main__":` smoke test

### Code standards (non-negotiable)
- Python 3.10+ union types (`str | None`, never `Optional[str]`)
- Return type on public method and `_build_query`: `-> str`
- Line length ≤ 120; 4-space indent; double quotes
- No `SELECT *` · No `LIKE '%x%'` · No `ORDER BY` unless requested · No correlated subqueries · No bare comma joins
- Predicate pushdown: dim-attr WHERE always inside dim subquery
- Narrow dim subquery SELECT: join key + only columns used downstream
- DROP unused JOINs when no filter and no SELECT column references that dim
- Integer year literals (no escaping); boolean filters as `0`/`1`
- No debug logging outside `debug_mode` block and `__main__`
- No imports from sibling SP files

### `_build_query` logic
- Build `select_columns` and `group_by_columns` lists incrementally
- "across" sentinel → add dim to SELECT + GROUP BY but drop WHERE filter on that dim
- Multiple filter values → add to GROUP BY; single value → constant (no GROUP BY)
- Dim subquery pattern:
  ```sql
  INNER JOIN (
      SELECT <pk>, <filter_and_select_cols>
      FROM <fqn>
      WHERE 1=1
        [AND LOWER(col) IN ('val1','val2')]  -- or col IN (...) if stored lowercase
        [AND int_col IN (2023, 2024)]
        [AND bool_col = 0]
  ) <alias> ON f.<fk> = <alias>.<pk>
  ```
- GROUP BY reuses `select_columns` (minus aggregates) — never ordinals
- Broadcast hint: `/*+ BROADCAST(alias) */` immediately after SELECT when dims are broadcast-eligible (Databricks only)

### Aggregation correctness rules (non-negotiable)

**Never use `AVG()` on a pre-computed ratio column.** Use one of these patterns:

**Sum-over-sum** (numerator + denominator both on fact):
```sql
SUM(f.numerator_col) / NULLIF(SUM(f.denominator_col), 0) AS metric_name
```

**Volume-weighted mean** (only ratio stored; weight on another table):
```sql
SUM(f.ratio_col * w.volume_col) / NULLIF(SUM(w.volume_col), 0) AS metric_name
-- requires: INNER JOIN weight_table w ON f.key = w.key
```

**Conditional aggregation by signal type** (one column stores different natures):
```sql
CASE WHEN LOWER(s.subcategory) = 'media' THEN SUM(f.value) ELSE AVG(f.value) END AS value
-- requires: dim_signal s already joined for subcategory access
```

**Conditional weight-table JOIN guard** (only join when the weighted metric is requested):
```python
need_weight = "price_cop" in metric_f   # set before _build_query
# emit INNER JOIN weight_table only when need_weight is True
```

**`NULLIF` returning NULL is correct** — when `SUM(weight) = 0` for a group (e.g. no volume for a segment that period), the metric returns `NULL`. This is the right behavior; do not substitute `0` unless the business explicitly asks.

**Country-code casing** — `_parse_filter_param` lowercases all values. If the warehouse stores codes as uppercase (`'CO'`, `'BR'`), emit `LOWER(country_code) = LOWER(param)` — not `country_code = param`. Silent zero-row results are the symptom of getting this wrong.

### Output
Write the file to the user-specified path. Create parent directories if needed. Offer an empty `__init__.py` alongside if one doesn't exist. After writing, print:
- File path written
- Suggested smoke-test command: `python <file>.py`
- Next step: paste the printed SQL into the warehouse query planner to verify partition pruning and join strategy

---

## Relevant Skills

- `.claude/skills/coding/scaffold-stored-procedure/SKILL.md`
