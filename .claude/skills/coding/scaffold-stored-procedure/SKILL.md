---
name: scaffold-stored-procedure
description: Interactively scaffold a Python dynamic-SQL stored-procedure class file from a fact-table schema and business spec — including helpers, public method, _build_query, and a runnable __main__ smoke test
domain: coding
requires_script: false
---

## Usage

Invoke with `/scaffold-stored-procedure` then answer the 10-step interview below.
The skill emits **one Python file** per fact table — nothing else (no wrappers, YAML configs, or test boilerplate).

**Optimization priority:** runtime first, readability second. SQL emitted should be lean (predicate pushdown, narrow projections, broadcast-friendly joins); the Python that builds it can be verbose.

**Mental model:**
- One SP class per fact table. The class is a **dynamic-SQL builder** — it does not run queries; it returns a SQL string.
- All dimensional filters are flat parameters on a single public method. The method composes a SQL string with optional WHERE clauses, optional GROUP BYs, and optional join subqueries.
- `"across"` is a sentinel meaning *"don't filter on this dim, but DO group by it"* — it is the linchpin of the design.

**Inputs collected in order:**

### Step 1 — Identity
- **Output file path** — full path; the skill is repo-agnostic. File name should follow `get_<domain>_kpis.py` convention (e.g. `get_impact_kpis.py`, `get_roi_kpis.py`, `get_price_kpis.py`).
- **Method name** — `snake_case`, must start with `get_`; drives PascalCase class name (strip `get_` prefix)
- **SQL dialect** — Databricks SQL / Snowflake / BigQuery / Postgres / T-SQL / MySQL

### Step 2 — Fact table
- Fully-qualified name (e.g. `catalog.schema.fact_sales`)
- All columns with types
- Which columns are FKs to dim tables
- Which columns are measure columns (to aggregate)
- Which columns are inline-denormalized dim attributes (Variant C — no join needed)

### Step 3 — Dimension tables (repeat for each)
- Fully-qualified name
- Primary key column
- FK column on the fact table
- Columns to expose as filters and/or SELECT columns

### Step 4 — Time model
- Does the dataset have a time dimension?
- **Default: canonical** (`year` int + `period` quarter/half/month/FY codes + `period_type` granularity tag)
- Only tailor if the user explicitly says their time model differs (weekly, fiscal-year offset, date-only, etc.)
- **Ask explicitly: is the time dimension at weekly or sub-monthly granularity?** If yes, `normalize_time`'s quarterly period-code logic (Q1/Q2/FY/H1/H2) will not apply — adapt to use `year` + `week_number` (or `iso_week`) instead, and drop period/period_type from the signature. Time parameters remain `year`, `quarter`, `week`, etc. — never encode periods as "Period A / Period B" text literals.

### Step 5 — Release-date semantics
- **Default: quarterly cutoff** at 15th of next quarter's first month — confirm once: *"Quarterly publish cadence — keep, change, or omit?"*

### Step 6 — Helper methods (3.1–3.6)
For each helper below, propose **canonical as the default**:
- `_sanitize_input` — SQL-injection blocker; ask if the allowed-char regex needs widening
- `_escape_sql_string` — single-quote escaping; confirm dialect is single-quote based
- `_validate_year` — integer year guard; omit if dataset has no year column
- `_parse_filter_param` — multi-value splitter on `|||#$#|||` delimiter; ask if upstream uses a different delimiter
- `_determine_current_period_info` — quarterly release-cutoff period computer; **include by default without prompting**
- `normalize_time` — 6-step time-triplet normalizer (~250 lines); **include by default without prompting**

### Step 7 — Per-filter configuration
For each filter parameter:
- Default value when caller passes `None` (`["across"]` for dims, `["all"]` for demographics, `None` for required)
- Apply `_sanitize_input`? (yes for free-text like country/brand; no for enum-controlled like period codes)
- Known value-fix hardcodes (e.g. `"megabrand" → "mega brand"`) — emit only what the user supplies

### Step 8 — Measure pattern (pick one)
- **Variant A** — column-list whitelist; aggregate per selected measure; ask for full whitelist and default subset
- **Variant B-kpi** — single `value` column; extra `kpi_dim(kpi, sub_kpi)`; filter on kpi/sub_kpi
- **Variant B-imagery** — 1–2 fixed measures; `metric="across"` expands to all; includes `debug_mode`
- **Variant C** — denormalized fact; brand-attr filters go in outer WHERE; no brand-dim subquery
- **Variant D** (composite SP) — refuse; document as hand-write only

For Variants A, B-kpi, and C, **classify each measure column by aggregation type** (ask the user for each):

| Type | When to use | SQL pattern |
|---|---|---|
| **Additive** | Raw counts, volumes, costs, spend — quantities that sum correctly | `SUM(f.col)` |
| **Pre-computed ratio** | ROI, rates, shares — stored as a result, not raw components | `SUM(f.col * w.weight) / NULLIF(SUM(w.weight), 0)` or `SUM(f.num) / NULLIF(SUM(f.den), 0)` |
| **Rate / index** | CPI, weather, distribution % — economy-wide or relative indices | `AVG(f.col)` |
| **Mixed-type** | One column storing different signal types (e.g. spend AND rates) | `CASE WHEN LOWER(s.type) = 'x' THEN SUM(f.col) ELSE AVG(f.col) END` |

For **pre-computed ratios**, ask:
- Are both numerator and denominator stored separately on the fact? → use `SUM(num) / NULLIF(SUM(den), 0)` directly
- Only the final ratio is stored? → ask for a weight column (volume, spend, units) to use as a proxy → use volume-weighted mean; requires joining the weight table
- Which table provides the weight, and what JOIN key links it to the fact?

For **mixed-type** signals, ask:
- Which dimension column indicates the type (e.g. `dim_signal.subcategory`)?
- Which value(s) of that column map to additive behavior (e.g. `'media'` = spend → `SUM`)?
- What should all other values do (`AVG` is the safe default for rates and binary flags)?

> ⚠️ **GROUP BY gotcha for mixed-type metrics**: The CASE WHEN condition references a dim column (e.g. `s.subcategory`). Databricks/Spark SQL strict mode requires every non-aggregated column referenced **anywhere in SELECT** — including inside CASE WHEN conditions — to appear in GROUP BY. Always unconditionally append the type-column to GROUP BY even when the user did not request it as a breakdown dimension. Example fix:
> ```python
> group_cols = [c.split(' AS ')[0] for c in sel]
> if "s.subcategory" not in group_cols:
>     group_cols.append("s.subcategory")
> q += f"GROUP BY {', '.join(group_cols)}"
> ```

**Guard weight-table JOINs** with a `need_weight = "<metric>" in requested_metrics` flag — only emit the JOIN when the weighted metric is actually requested, to keep the query lean when the user asks for a subset of metrics.

### Step 9 — Runtime optimizations
- Are string filter columns stored lowercase in the warehouse? (affects `LOWER(col)` vs lowercase-input)
- What are the fact table's partition columns? (emit those filters first inside subquery WHERE)
- Any dims small enough to broadcast? (Databricks `/*+ BROADCAST(alias) */` hints)
- Suggest aggregate-before-join CTE for extremely large facts? (off by default)

### Step 10 — Smoke test
- Representative `__main__` values (single-country, single-entity call); always emit a meaningful invocation

## Output

A single `.py` file at the user-specified path structured as:
1. Module docstring (one line)
2. Imports (`datetime`, `typing.Any`, `pandas` only if used, project logger or stdlib `logging`)
3. PascalCase class declaration (method name minus `get_` prefix)
4. Class docstring
5. Six private helpers (§3.1–3.6 — include/tailor/omit per Step 6)
6. Public method with full flat-union signature (`str | None = None` for all filters, `datetime | None = None` for release date last, optional `debug_mode: bool = False`)
7. `_build_query(self, ...) -> str` method
8. `if __name__ == "__main__":` smoke test

**Code standards (always enforced):**
- Line length ≤ 120; 4-space indent; double quotes; Python 3.10+ union types (`str | None`, not `Optional[str]`)
- Return type on public method and `_build_query`: `-> str`
- No `SELECT *`, no `LIKE '%x%'`, no `ORDER BY` unless asked, no correlated subqueries, no bare comma joins
- Predicate pushdown: dim-attr WHERE inside dim subquery, never in outer query
- Narrow dim subquery `SELECT`: join key + only columns used downstream
- DROP unused dim JOINs when no filter and no SELECT column references that dim
- INTEGER year literals (skip escaping); boolean filters as `0`/`1` literals
- No `print` or debug logging outside `debug_mode` block and `__main__`
- No imports from sibling SP files
- No `Optional[...]` — use `X | None`
- If parent directory doesn't exist, create it; offer an empty `__init__.py` alongside
- **FQN mandatory in `_build_query`**: every `FROM` and `JOIN` inside the Python string-builder must use the fully-qualified `<catalog>.<schema>.<table>` name collected in Steps 2–3. Never emit bare table names (e.g. `FROM dim_date`). Store each FQN in a local variable (`fact_fqn`, `dim_date_fqn`, etc.) and interpolate it into the f-string, or hardcode the FQN string directly — but never drop the catalog/schema prefix.

## Steps

1. Print the UX sketch header and run Step 1 (Identity) — ask all three questions together
2. Run Step 2 (Fact table) — collect FQN, column list with types, FK map, measure columns, inline-denormalized attrs
3. Run Step 3 (Dims) — loop until user says "no more dims"; collect FQN, PK, FK, filter/select columns each time
4. Run Step 4 (Time model) — offer canonical as default; skip tailoring unless user flags a different model
5. Run Step 5 (Release-date) — one confirmation prompt; default is keep
6. Run Step 6 (Helpers 3.1–3.4) — for each present a one-line assumption summary and ask canonical/tailored/omit; helpers 3.5–3.6 are auto-included silently unless Step 4/5 said omit
7. Run Step 7 (Per-filter config) — collect defaults, sanitize flags, value-fix hardcodes for every filter
8. Run Step 8 (Measure pattern) — identify variant, collect whitelist and default subset; use the Reference Patterns below
9. Run Step 9 (Runtime optimizations) — collect lowercase-storage flag, partition columns, broadcast dims
10. Run Step 10 (Smoke test) — collect representative `__main__` values
11. Generate the full Python file in memory using the patterns in Reference Patterns below — apply all collected decisions; never use placeholder comments like `# TODO`
12. Write the file to the user-specified path; create parent directories if needed
13. Offer an empty `__init__.py` alongside if parent `__init__.py` does not exist
14. Report the file path written and suggest: *run `python <file>.py` to smoke test, then paste the printed SQL into your warehouse query planner*

---

## Reference Patterns

All patterns below are canonical. Use verbatim unless the interview produced a reason to deviate.

### Helper 3.1 — `_sanitize_input`

```python
def _sanitize_input(self, value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Input must be a string")
    dangerous_chars = [
        ";", "--", "/*", "*/", "xp_", "sp_", "exec", "execute",
        "select", "insert", "update", "delete", "drop", "create", "alter",
    ]
    value_lower = value.lower()
    for char in dangerous_chars:
        if char in value_lower:
            raise ValueError(f"Invalid input: contains dangerous sequence '{char}'")
    import re
    if not re.match(r"^[a-zA-Z0-9\s_\-\.\/\&]+$", value):
        raise ValueError("Invalid input: contains invalid characters")
    return value.strip()
```

The canonical regex allows `&` and `/` — required for common category names like `"Sales & Marketing Investments"`. Widen further if filter values may legally contain parentheses, `+`, etc.

### Helper 3.2 — `_escape_sql_string`

```python
def _escape_sql_string(self, value: str) -> str:
    if value is None:
        return "NULL"
    escaped_value = str(value).replace("'", "''")
    return f"'{escaped_value}'"
```

### Helper 3.3 — `_validate_year`

```python
def _validate_year(self, year: str) -> bool:
    try:
        year_int = int(year)
        return 1900 <= year_int <= 2100
    except ValueError:
        logger.warning("Handled ValueError in _validate_year", exc_info=True)
        return False
```

Omit entirely if the dataset has no `year` column.

### Helper 3.4 — `_parse_filter_param`

```python
def _parse_filter_param(self, param: str | None) -> list[str] | None:
    if not param or param.strip() == "":
        return None
    param = param.strip()
    if param.lower() == "across":
        return ["across"]
    if "|||#$#|||" in param:
        return [p.strip().lower() for p in param.split("|||#$#|||")]
    return [p.strip().lower() for p in param.split(",")]
```

`|||#$#|||` is the real multi-value delimiter used by the upstream argument extractor — not a typo. Ask before normalizing to comma-only.

### Helper 3.5 — `_determine_current_period_info`

```python
def _determine_current_period_info(
    self, country: str | None = None, release_date: datetime | None = None
) -> dict[str, Any]:
    today = datetime.now()
    current_year = today.year
    current_month = today.month
    if release_date is None:
        release_date = datetime(current_year, (current_month // 3) * 3 + 1, 15)
    if today < release_date:
        logger.info(
            f"Current date {today} is before release date {release_date}, "
            "adjusting period to previous month."
        )
        current_month -= 1
        if current_month == 0:
            current_month = 12
            current_year -= 1
    if 1 <= current_month <= 3:
        current_period = "Q1"
    elif 4 <= current_month <= 6:
        current_period = "Q2"
    elif 7 <= current_month <= 9:
        current_period = "Q3"
    else:
        current_period = "Q4"
    return {"year": current_year, "month": current_month, "period": current_period}
```

Include by default. The `country` arg is currently unused but kept for future per-country release calendars — preserve it.

### Helper 3.6 — `normalize_time` (paste verbatim)

```python
def normalize_time(
    self,
    year: str | None,
    period: str | None,
    period_type: str | None,
    current_year: int,
    current_month: int,
    current_period: str,
) -> dict:
    year_filters: list[int] = []
    period_filters: list[str] = []
    across_year = 0
    across_period = 0

    # Step 1: split delimited strings
    if year is not None and year.lower() != "across":
        year_filters = self._parse_filter_param(year)
        year_filters = [int(y) for y in year_filters if self._validate_year(y)]
    elif year is not None and year.lower() == "across":
        across_year = 1

    if period is not None and period.lower() != "across":
        period_filters = self._parse_filter_param(period)
    elif period is not None and period.lower() == "across":
        across_period = 1

    # Step 2: determine defaults
    latest_year = current_year
    latest_period = current_period
    latest_period_type = "qtr"
    if current_month in (1, 2, 3):
        latest_period = "fy"
        latest_year = current_year - 1
        latest_period_type = "full year"
    elif 4 <= current_month <= 6:
        latest_period = "q1"
    elif 7 <= current_month <= 9:
        latest_period = "q2"
    elif 10 <= current_month <= 12:
        latest_period = "q3"

    if period is None and period_type is None:
        passed_year = year_filters[0] if len(year_filters) > 0 else None
        if (passed_year is not None) and (passed_year < current_year):
            period_filters.append("fy")
            period_type = "full year"
        else:
            period_filters.append(latest_period)
            period_type = latest_period_type

    # Step 3: infer period_type from period value when missing
    sample_period = None
    if period_type is None and len(period_filters) > 0:
        sample_period = period_filters[0]
        if sample_period.startswith("q"):
            period_type = "qtr"
        elif sample_period.startswith("h"):
            period_type = "half year"
        elif sample_period == "fy":
            period_type = "full year"
        elif sample_period in ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"):
            period_type = "r12m"

    if len(period_filters) == 0 and period_type is not None:
        pt_low = period_type.lower()
        if pt_low in ("ytd", "mth"):
            if 1 <= current_month <= 3:
                ytd_month = "dec"
            elif 4 <= current_month <= 6:
                ytd_month = "mar"
            elif 7 <= current_month <= 9:
                ytd_month = "jun"
            else:
                ytd_month = "sep"
            period_filters.append(ytd_month)
        elif pt_low == "qtr":
            period_filters.append(latest_period)
        elif pt_low == "half year":
            period_filters.append("h2" if 1 <= current_month <= 6 else "h1")
        elif pt_low == "full year":
            period_filters.append("fy")
        elif pt_low.startswith("r"):
            if 1 <= current_month <= 3:
                period_filters.append("dec")
            elif 4 <= current_month <= 6:
                period_filters.append("mar")
            elif 7 <= current_month <= 9:
                period_filters.append("jun")
            else:
                period_filters.append("sep")

    # Step 4: cross-type repairs
    sample_type = period_type.lower() if period_type is not None else None
    sample_period = period_filters[0] if len(period_filters) > 0 else None
    if sample_type in ("ytd","mth") and (sample_period and sample_period.startswith("q")):
        mapping = {"q1":"mar","q2":"jun","q3":"sep","q4":"dec"}
        period_filters = [mapping.get(sample_period, sample_period)]
        sample_period = period_filters[0]
    if (sample_type and sample_type.startswith("r")) and (
        (sample_period and sample_period.startswith("h")) or sample_period == "fy"
    ):
        mapping = {"h1":"jun","h2":"dec","fy":"dec"}
        period_filters = [mapping.get(sample_period, sample_period)]
        sample_period = period_filters[0]
    if sample_type == "qtr" and sample_period in (
        "jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec","fy","h1","h2"
    ):
        if sample_period in ("jan","feb","mar"):
            new_p = "q1"
        elif sample_period in ("apr","may","jun"):
            new_p = "q2"
        elif sample_period in ("jul","aug","sep"):
            new_p = "q3"
        else:
            new_p = "q4"
        period_filters = [new_p]
        sample_period = new_p
    if sample_type == "ytd" and (
        sample_period == "fy" or (sample_period and sample_period.startswith("h"))
    ):
        mapping = {"fy":"dec","h1":"jun","h2":"dec"}
        period_filters = [mapping.get(sample_period, sample_period)]
        sample_period = period_filters[0]
    if sample_type == "across":
        period_type = None
        sample_type = None
    if (sample_type and sample_type.startswith("r")) and (sample_period and sample_period.startswith("q")):
        mapping = {"q1":"mar","q2":"jun","q3":"sep","q4":"dec"}
        period_filters = [mapping.get(sample_period, sample_period)]
        sample_period = period_filters[0]

    # Step 5: final fallback defaults
    if period_type is None:
        period_type = latest_period_type
    if len(year_filters) == 0:
        year_filters.append(latest_year)
    if len(period_filters) == 0:
        period_filters.append(latest_period)

    # Step 6: auto-include prior year for single-period requests
    if len(year_filters) * len(period_filters) == 1:
        base_year = year_filters[0]
        if (base_year - 1) not in year_filters:
            year_filters.append(base_year - 1)

    return {
        "year_filters": year_filters,
        "period_filters": period_filters,
        "across_year": across_year,
        "across_period": across_period,
        "period_type": period_type,
        "latest_year": latest_year,
        "latest_period": latest_period,
        "latest_period_type": latest_period_type,
        "final_period_type": period_type,
    }
```

### `_build_query` — Variant A (canonical star schema)

```python
# across flags per dim
across_country = country_filters and country_filters[0] == "across"
# ... repeat for each filter

select_columns = ["t.year", "t.period", "t.period_type"]
group_by_columns = []
# conditionally append dim columns + their group-by membership
kpi_columns = [f"SUM(f.{kpi}) as {kpi}" for kpi in kpi_filters]

query = f"""
SELECT {", ".join(select_columns + kpi_columns)}
FROM {fact_fqn} f
INNER JOIN (
    SELECT time_id, year, period, period_type
    FROM {time_dim_fqn}
    WHERE 1=1
      [AND year IN ({year_list})]
      [AND LOWER(period) IN ({period_list})]
      [AND LOWER(period_type) = {escape(period_type)}]
) t ON f.time_id = t.time_id
INNER JOIN (
    SELECT brand_id, country, brand, ...
    FROM {brand_dim_fqn}
    WHERE 1=1
      [AND LOWER(country) IN ({country_list})]
      [AND LOWER(brand) IN ({brand_list})]
) b ON f.brand_id = b.brand_id
INNER JOIN (
    SELECT cohort_id, age, gender, income, region
    FROM {cohort_dim_fqn}
    WHERE 1=1
      [AND LOWER(age) IN ({age_list})]
) c ON f.cohort_id = c.cohort_id
[GROUP BY {", ".join(select_columns)}]
"""
```

### `_build_query` — Variant C (denormalized fact, no brand-dim subquery)

Brand-attr filters go in the outer WHERE clause. References `f.country`, `f.brand_family`, etc. directly. Only `time_dim` and `cohort_dim` are joined.

```python
query = f"""
SELECT ...
FROM {fact_fqn} f
INNER JOIN (...) t ON f.time_id = t.time_id
INNER JOIN (...) c ON f.cohort_id = c.cohort_id
WHERE 1=1
  [AND LOWER(f.country) IN ({country_list})]
  [AND LOWER(f.brand_family) IN ({bf_list})]
[GROUP BY ...]
"""
```

### Aggregation Correctness Patterns

**Never use `AVG()` on a pre-computed ratio column.** Averaging ratios ignores the magnitude of each row's denominator, producing a mathematically incorrect result when row sizes differ. Use one of these patterns instead.

#### Pattern 1 — Sum-over-sum ratio (numerator + denominator on same fact)

Use when both components are stored directly on the fact table:

```sql
SUM(f.numerator_col) / NULLIF(SUM(f.denominator_col), 0) AS metric_name
```

Example: ROI where `fact_roi.revenue` and `fact_roi.spend` are both present:
```sql
SUM(fr.revenue) / NULLIF(SUM(fr.spend), 0) AS roi
```

#### Pattern 2 — Volume-weighted mean (pre-computed ratio, weight from joined table)

Use when only the ratio value is stored on the fact and a natural weight (volume, units, spend) lives on another table:

```sql
SUM(f.ratio_col * w.weight_col) / NULLIF(SUM(w.weight_col), 0) AS metric_name
```

Example: average price weighted by volume, joining `fact_actual_volume av`:
```sql
SUM(fp.price_lcu * av.true_volume_hl) / NULLIF(SUM(av.true_volume_hl), 0) AS price_cop
```

The weight table JOIN uses the same dimensional key as the fact (`date_id`, `entity_id`, `country_code`, etc.).

#### Pattern 3 — Conditional aggregation by signal type (CASE-based SUM / AVG)

Use when a single measure column stores values of different natures depending on a type dimension:

```sql
CASE
    WHEN LOWER(s.subcategory) = 'media' THEN SUM(f.input_value)
    ELSE AVG(f.input_value)
END AS input_level
```

The type dimension (`dim_signal`, `dim_kpi`, etc.) must already be joined. This pattern only produces a meaningful result when the query groups by the type dimension — if the query collapses across types, SQLite/Databricks will pick an arbitrary subcategory for the CASE; document this known limitation in the class docstring.

#### Pattern 4 — Conditional weight-table JOIN guard

When Pattern 2 applies only to a subset of the requested metrics, guard the extra JOIN so it is only emitted when needed:

```python
need_weight = "price_cop" in metric_f  # or however the metric list is determined
...
weight_join = ""
if need_weight:
    weight_join = f"""
INNER JOIN (
    SELECT date_id, entity_id, country_code, SUM(volume_col) AS volume_col
    FROM {weight_table_fqn}
    WHERE 1=1
      [AND country_code IN ({country_list})]
    GROUP BY date_id, entity_id, country_code
) w ON f.date_id = w.date_id AND f.entity_id = w.entity_id AND f.country_code = w.country_code
"""
```

Omitting the JOIN when the metric is absent keeps the query lean and avoids unnecessary row-multiplication.

#### NULLIF on weight sum returns NULL — this is correct

`NULLIF(SUM(weight), 0)` returns `NULL` when the weight sum is zero (e.g. no volume in a segment for that period). The metric column in the result will be `NULL` for that row. This is the semantically correct behavior — there is no meaningful average when the denominator is zero. Do not replace with `0` or a fallback value unless the business explicitly requests it.

### Public method body responsibilities (in order)

1. Call `_determine_current_period_info` if used
2. Parse every filter param via `_parse_filter_param`; apply per-filter defaults
3. Sanitize free-text filters via `_sanitize_input`
4. Apply value-fix hardcodes (emit only what the user provided)
5. Call `normalize_time` if used
6. Convert boolean filters to `True | False | None`
7. Validate measure selector against whitelist
8. Set any conditional JOIN guard flags (e.g. `need_weight = "metric" in metric_f`)
9. Dispatch to `_build_query`

### `"across"` SELECT/GROUP BY rule

For every filter that is not `None`:
- The dim column appears in the SELECT list
- It appears in GROUP BY **iff** `across_X is True` OR the filter list has more than one value
- Single filter value → constant (no GROUP BY needed); multiple values or "across" → breakdown

### Runtime optimization rules (always-on defaults)

| Rule | Implementation |
|---|---|
| Predicate pushdown | Dim-attr WHERE inside dim subquery, never outer query |
| Narrow projection | Subquery SELECT: join key + only cols used downstream |
| Integer year literals | Skip `_escape_sql_string` for year (already int-validated) |
| Booleans | `0`/`1` literals, not `True`/`False` strings |
| Drop unused JOINs | Omit a dim JOIN entirely if no filter and no SELECT col references it |
| Guard weight JOINs | Only emit weight-table JOIN when the weighted metric is in the requested set |
| IN lists | Prefer `col IN (...)` over chained `OR`s |
| GROUP BY | Reuse select_columns (minus aggregates); never ordinals |
| `WHERE 1=1` | Anchor for conditional clauses |

Ask the user about: `LOWER(col)` vs lowercase-input; partition-column ordering; broadcast hints; aggregate-before-join CTE.
Never emit: `SELECT *`, `LIKE '%x%'`, `ORDER BY` (unless asked), correlated subqueries, bare comma joins.

---

## Notes & Gotchas

- `|||#$#|||` delimiter is real — the upstream argument extractor uses it. Don't normalize without asking.
- `SELECT … GROUP BY <select_columns>` is intentional. Reusing the SELECT list as GROUP BY is correct and survives column-list edits. Don't use ordinals.
- The `country` arg to `_determine_current_period_info` is currently unused — kept for future per-country release calendars. Preserve it.
- No CTEs unless asked. Mix of subquery + CTE styles in one file is the bigger sin.
- `__main__` is the primary smoke test — always emit a meaningful invocation, not a placeholder.
- Variant D (composite SP) calls multiple other SPs and stitches results. It is out of scope — document as hand-write only and refuse to scaffold.
- Type hints in older SP files sometimes lie (`pd.DataFrame` return type on `_build_query`). Always emit `-> str` for `_build_query`.
- **Aggregation rule — never `AVG()` a ratio.** Pre-computed ratios (ROI, price per unit, share) stored as a single column must use volume-weighted mean or sum-over-sum. Simple `AVG()` gives wrong results whenever row sizes differ. See Aggregation Correctness Patterns above.
- **Country-code casing.** `_parse_filter_param` lowercases all values. If the warehouse stores country codes as uppercase (`'CO'`, `'BR'`), emit `LOWER(country_code) = LOWER({esc_c})` — not `country_code = {esc_c}`. Failure to do this causes silent zero-row results for country filters.
- **Weekly time dim.** If `dim_date` is at weekly granularity, `normalize_time`'s quarterly period-code logic (Q1/Q2/FY/H1/H2) does not apply. Use `year` + `week_number` (or `iso_week`) parameters instead, and drop `period` / `period_type` from the signature. Confirm granularity in Step 4 before scaffolding.
- **Mixed-type CASE aggregation collapses incorrectly when `across` collapses multiple types.** Document this in the docstring. The fix is to always group by the signal/type dimension when using Pattern 3.
- **FQN enforcement in `_build_query`.** The FQN collected in Steps 2–3 must appear verbatim in every `FROM` and `JOIN` inside the Python string that `_build_query` builds. Never allow bare table names (e.g. `FROM dim_date` or `FROM fact_impact`) to slip into the emitted SQL — the warehouse requires `<catalog>.<schema>.<table>` for Unity Catalog / BigQuery / Snowflake. If the user provides only a bare name in Step 2/3, ask for the catalog and schema before generating the file.
