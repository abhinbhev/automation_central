---
name: scaffold-sp-wrapper
description: Interactively scaffold the async wrapper functions layer (`<usecase>_functions.py`) that sits between SP class files and the LangGraph orchestrator — covers raw SP wrappers, release-date caching, post_processing(), and @register_function concept functions
domain: coding
requires_script: false
---

## Usage

Invoke with `/scaffold-sp-wrapper` then answer the interview below.
The skill emits **one Python file** (`<usecase>_functions.py`) per use case, or adds individual wrapper blocks to an existing file.
Read alongside `/scaffold-stored-procedure` — the SP class is the layer below this one.

**What this layer does (in order per request):**
1. Cleans raw parameter strings from the argument extractor via `clean_and_join_values`
2. Fetches the release date for the given country (singleflight-cached, per use case)
3. Instantiates the SP class and calls its public method to produce a SQL string
4. Executes the SQL against Databricks and converts the response to a DataFrame
5. Post-processes the DataFrame (title-case, rename, replace boolean labels)
6. Returns a standard tuple consumed by the LangGraph node upstream

**Two distinct function types in one file:**

| Type | Decorated? | Body | Purpose |
|---|---|---|---|
| **Raw SP wrapper** | No | Real logic (clean → execute → return df) | One per SP class; fetches data from one table |
| **Registered concept function** | Yes (`@register_function`) | `pass` (dummy) or real multi-SP orchestration | What the template selector LLM picks |

**Inputs collected in order:**

### Step 1 — File identity
- **Output file path** — full path to `<usecase>_functions.py`; skill is repo-agnostic. **The file name must be `<use_case_name>_functions.py` using the exact `use_case_name` string — do not shorten or alias it.**
- **Use case name** — the string used as `use_case_name` default. This MUST match:
  1. The file name prefix (`<use_case_name>_functions.py`)
  2. The subdirectory name under `stored_procedures/` used in every lazy import (`from .stored_procedures.<use_case_name>.<module> import ...`)
  Using a short alias (e.g. `watchtower_mmm`) when the SP subdir is named `gai_copilot_marketing_watchtower_ghq` causes `ModuleNotFoundError` at runtime. Always confirm the exact subdirectory name with the user before writing the file.
- **Logger import path** — project-specific; fall back to `import logging; logger = logging.getLogger(__name__)`

### Step 2 — Release-date cache
- **Release-date table FQN** — `<catalog>.<schema>.COUNTRY_RELEASE_DATE_DIM` (ask for actual FQN)
- **Column names** in that table — defaults `country` (uppercase match) + `release_date`
- **Date formats to try** — defaults `%d-%m-%Y` then `%Y-%m-%d`; ask if different
- **No release-date concept?** — if real-time table with no publication lag, omit `get_release_dates` entirely and both module-level cache dicts

### Step 3 — Raw SP wrappers (repeat per SP / fact table)
For each wrapper:
- SP function name (matches SP class public method name)
- SP class name + module path relative to this file (for the lazy import inside the function body)
- Parameter list (mirrors SP class signature — full `str = None` defaults; demographic defaults like `age="All"`)
- Country-scoped or global? (`get_release_dates(country=country)` vs `get_release_dates(country=None)`)
- `decimal_precision` — default `1`; ask if different (e.g. `2` for financials, `0` for counts)
- Return shape: **4-tuple** `(df, query, table_refs, stored_proc)` or **5-tuple** `(df, query, table_refs, change_columns, stored_proc)` — 5-tuple only for "highlights" wrappers with YoY change indicators
- `stored_proc` value: plain string (e.g. `"get_brand_direct_kpis"`) or multilingual dict `{"en": "...", "es": "...", "pt": "..."}`
- Title-case columns (default list: `country`, `brand`, `brand_family`, `age`, `gender`, `region`, `income`, `life_cycle`, `price_segment`, `abi_comp`, `zone`, `market_maturity`, `global_brand`, `imagery`)
- Special transforms: column renames (e.g. `abi_comp` → `abi_or_competitor`), boolean → label replacements
- `table_references` list — uppercase table names for lineage (fact + all dim tables)
- Static lookup (no SP class)? — emit slim raw-SQL form (`SELECT * FROM <table>`) instead of full SP pattern

### Step 4 — `post_processing()` function
One function per use case (NOT one per SP — it uses `stored_proc_name` as a switch):
- For each SP: wide format (melt needed, multi-measure columns → `kpi`/`value`) or long format (already has `value` column, no melt)?
- KPI sort order for melted SPs (use-case specific — ask user)
- Column renames inside `post_processing` (display names differ from SQL column names)
- `decimal_precision` for rounding — default `1`
- Any custom sort columns beyond KPI order?

### Step 5 — `@register_function` concept functions
For each registered function:
- Registered name (the key the template selector LLM outputs; auto-generates camelCase alias)
- Source name (human-readable label shown in UI / prompts — must be unique across all dummies)
- Aliases (optional; only needed for non-standard camelCase variants)
- **Dummy** (`pass` body) or **real orchestrator** (calls one or more raw wrappers)?
- If real: which raw wrappers does it call? Which parameters pass through?
- Docstring — the `function_purpose` field fed to the template selector LLM; must be complete and accurate

## Output

A single `<usecase>_functions.py` file structured as:
1. Module imports (`asyncio`, `time`, `datetime`, `Decimal`, `numpy`, `pandas`, logger, `register_function`)
2. Module-level cache dicts (`_release_date_cache`, `_release_date_inflight`) — omit if no release-date concept
3. `get_release_dates()` async function — singleflight + cache pattern — omit if no release-date concept
4. Raw SP wrapper functions — one per fact table, with `# <n>. <label>` section comments
5. `post_processing()` — single dispatch function keyed on `stored_proc_name`
6. `@register_function` dummy and real concept functions

**Code standards (always enforced):**
- Python 3.10+ union types; line length ≤ 120; 4-space indent; double quotes
- **Lazy imports mandatory** — all SP class imports and `utils_functions` imports stay inside the function body (never hoisted to module level — causes circular imports)
- `logger.bind(request_id=request_id).info(...)` — always use the bind pattern for tracing
- No `logger.debug` or `logger.trace` — use `logger.info` for operational info, `logger.warning` for non-fatal failures
- `clean_and_join_values(val)` applied to every parameter without exception before passing to SP class
- All SP wrapper params default to `None` except confirmed demographic defaults (e.g. `age="All"`)
- `utils_functions` import must list specific names (`clean_and_join_values`, `execute_databricks_query`), never `import *`
- `post_processing` is ONE function, not one per SP — never split it

**After writing the file, remind the user to:**
- Add `from . import <usecase>_functions` to `analysis_template_executor/__init__.py`
- Verify registry: `python -c "from <pkg>.analysis_template_executor.function_registry import REGISTRY; print(list(REGISTRY.keys()))"`

## Steps

1. Run Step 1 (File identity) — ask all three questions together
2. Run Step 2 (Release-date cache) — one prompt block; default is keep with canonical singleflight pattern (see Reference Patterns below)
3. Run Step 3 (Raw SP wrappers) — loop; collect all details per wrapper before moving to next; use the canonical anatomy pattern
4. Run Step 4 (`post_processing`) — collect melt/pivot/sort/rename decisions per SP
5. Run Step 5 (`@register_function`) — loop; collect dummy vs real, name, source_name, docstring
6. Generate the full Python file in memory using the patterns below — no `# TODO` stubs; no `pass` except in dummy functions
7. Write the file to the user-specified path; create parent directories if needed
8. Print the file path, the `__init__.py` reminder, and the registry verification command

---

## Reference Patterns

### Module imports (canonical)

```python
import asyncio
import time
from datetime import datetime
from decimal import Decimal

import numpy as np
import pandas as pd
from engine.utils.logger_util import logger          # ask user for actual path

from .function_registry import register_function
```

`time` is imported for convention even if unused. `Decimal` is used in `post_processing()` for float detection.

### Module-level cache state

```python
_release_date_cache: dict[str, tuple] = {}
_release_date_inflight: dict[str, asyncio.Future] = {}
```

These must be at module level (not inside any function) so they persist across calls in the same process lifetime.

### `get_release_dates()` — full singleflight pattern

```python
async def get_release_dates(
    request_id="release_date_pull",
    country: str = "default",
    use_case_name: str = "<usecase>",
):
    from .utils_functions import execute_databricks_query

    if country and country != "default":
        country = country.upper()

    cache_key = f"{use_case_name}:{country}"

    if cache_key in _release_date_cache:
        return _release_date_cache[cache_key]

    inflight = _release_date_inflight.get(cache_key)
    if inflight is not None:
        try:
            return await inflight
        except Exception:
            logger.warning("Suppressed Exception in get_release_dates", exc_info=True)

    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    _release_date_inflight[cache_key] = fut

    try:
        query = f"""
            SELECT release_date
            FROM <catalog>.<schema>.COUNTRY_RELEASE_DATE_DIM
            WHERE country = '{country}'
        """
        payload = {"query": query, "decimal_precision": 1, "use_case": use_case_name}
        response_data = await execute_databricks_query(payload, use_case_name)

        release_date = None
        if response_data:
            raw = response_data[0].get("release_date")
            for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    release_date = datetime.strptime(str(raw), fmt)
                    break
                except (ValueError, TypeError):
                    pass

        result = (release_date, query, ["COUNTRY_RELEASE_DATE_DIM"], "get_release_dates")
        _release_date_cache[cache_key] = result
        fut.set_result(result)
        return result

    except Exception as e:
        result = (None, None, None, None)
        _release_date_cache[cache_key] = result
        if not fut.done():
            fut.set_exception(e)
        return result

    finally:
        _release_date_inflight.pop(cache_key, None)
```

**Returns:** 4-tuple `(release_date: datetime | None, query: str | None, table_references: list | None, stored_proc: str | None)`
**Callers unpack as:** `release_date, _, _, _ = await get_release_dates(...)`

For global (country-less) wrappers call with `country=None` — requires a `'DEFAULT'` row in the release-date table.

### Raw SP wrapper — canonical anatomy

```python
# <n>. <Human label>
async def <sp_name>(
    request_id,
    <param>: str = None,        # mirrors SP class signature exactly
    ...,
    use_case_name: str = "<usecase>",
) -> tuple:
    """One sentence describing what data this retrieves."""
    from .stored_procedures.<usecase>.<sp_module> import <ClassName>
    from .utils_functions import clean_and_join_values, execute_databricks_query

    # Step 1: clean all params
    param = clean_and_join_values(param)
    ...

    # Step 2: get release date
    release_date, _, _, _ = await get_release_dates(
        request_id=request_id, country=country, use_case_name=use_case_name
    )
    logger.bind(request_id=request_id).info(f"Release date for country {country} is: {release_date}")

    # Step 3: build query
    handler = <ClassName>()
    query = handler.<sp_method>(param=param, ..., release_date=release_date)

    # Step 4: execute
    payload = {"query": query, "decimal_precision": 1, "use_case": use_case_name}
    logger.bind(request_id=request_id).info(f"Final payload for databricks is: {payload}")
    response_data = await execute_databricks_query(payload, use_case_name)

    # Step 5: handle empty
    if not response_data:
        logger.warning(f"No data returned from the query with payload {payload}.")
        return pd.DataFrame(), None, None, None
    response_data_df = pd.DataFrame(response_data)

    # Step 6: title-case string columns
    for col in ["country", "brand", "brand_family", "age", "gender", "region",
                "income", "life_cycle", "price_segment", "abi_comp", "zone",
                "market_maturity", "global_brand", "imagery"]:
        if col in response_data_df.columns:
            response_data_df[col] = response_data_df[col].astype(str).str.title()

    # Step 7: special transforms (column renames, boolean → label)
    # e.g.:
    # if "with_home_market" in response_data_df.columns:
    #     response_data_df = response_data_df.rename(columns={"with_home_market": "Home Market"})
    # if "Home Market" in response_data_df.columns:
    #     response_data_df["Home Market"] = response_data_df["Home Market"].replace(
    #         {True: "With Home Market", False: "Without Home Market"}
    #     )

    table_references = ["FACT_TABLE", "DIM1", ...]  # uppercase, no schema prefix
    stored_proc = "<sp_name>"                        # or multilingual dict for highlights

    return response_data_df, query, table_references, stored_proc
```

**Extended 5-tuple for "highlights" wrappers** (YoY change indicators):
```python
return response_data_df, query, table_references, change_columns, stored_proc
# stored_proc is a multilingual dict: {"en": "Brand Highlights", "es": "...", "pt": "..."}
# change_columns = get_change_columns(response_data) imported from utils_functions
```

**Static lookup (no SP class) — slim form:**
```python
async def get_lookup_table(request_id="lookup_pull", use_case_name: str = "<usecase>"):
    from .utils_functions import execute_databricks_query
    query = "SELECT * FROM <catalog>.<schema>.<TABLE>"
    payload = {"query": query, "decimal_precision": 1, "use_case": use_case_name}
    response_data = await execute_databricks_query(payload, use_case_name)
    if not response_data:
        return pd.DataFrame(), None, None, None
    return pd.DataFrame(response_data), query, ["TABLE"], "get_lookup_table"
```

### `post_processing()` — structural template

```python
def post_processing(df: pd.DataFrame, stored_proc_name: str, ...) -> pd.DataFrame:
    if stored_proc_name == "<sp_name_a>":
        # Wide → long melt
        id_cols = ["year", "period", "period_type", "country", ...]
        value_cols = [c for c in df.columns if c not in id_cols]
        df = df.melt(id_vars=id_cols, value_vars=value_cols, var_name="kpi", value_name="value")
        kpi_order = ["<kpi1>", "<kpi2>", ...]  # user-supplied
        df["kpi"] = pd.Categorical(df["kpi"], categories=kpi_order, ordered=True)
        df = df.sort_values("kpi")

    elif stored_proc_name == "<sp_name_b>":
        # Already long — no melt; apply column renames + sorting

    # Shared: build Year Period label
    if "year" in df.columns and "period" in df.columns:
        df["Year Period"] = df["year"].astype(str) + " " + df["period"].str.upper()

    # Pivot if exactly 2 time combinations; else keep long
    # Strip cohort columns with only one distinct value = "All"
    # Round floats; fill NaN → None
    for col in df.select_dtypes(include="float").columns:
        df[col] = df[col].round(1)
    df = df.where(df.notna(), other=None)

    return df
```

`post_processing` is **a single function per use case** keyed on `stored_proc_name`. Never split it. When adding a new SP, add an `elif` branch.

Column renames (display names differ from SQL names) go in `post_processing`, not in the wrapper.

### Universal period pivot helper — `_apply_period_pivot`

When a query spans multiple years or quarters, long-format results (one row per period) are hard to compare. Add this helper and call it at the **end** of `post_processing` to pivot the data wide.

```python
_KNOWN_METRICS = {
    "impact_hl", "nr_lcu", "roi", "actual_hl", "predicted_hl", "smoothed_hl",
    "input_level", "price_cop", "cpi", "cpi_raw", "cost",
    # add use-case-specific metric column names here
}

_known_dim_cols = {
    "country", "brand", "category", "subcategory", "signal", "display_name",
    "year", "quarter", "month", "week", "period", "is_forecast",
    "week_of_year", "source",
}

def _apply_period_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot multi-period results wide so each period becomes a column group.
    
    Decision rules (checked in order):
    1. week present → skip (50+ pivot columns; too wide for LLM consumption)
    2. multi-year + quarter → pivot label: "2024Q1", "2025Q3"
    3. multi-year only → pivot label: "2024", "2025"
    4. single year + multi-quarter → pivot label: "Q1", "Q2"
    5. multi-month → pivot label: "Jan", "Feb"
    6. single period → no pivot; return as-is
    """
    try:
        if "week" in df.columns and df["week"].nunique() > 1:
            return df  # rule 1

        has_year = "year" in df.columns
        has_quarter = "quarter" in df.columns
        has_month = "month" in df.columns

        multi_year = has_year and df["year"].nunique() > 1
        multi_quarter = has_quarter and df["quarter"].nunique() > 1
        multi_month = has_month and df["month"].nunique() > 1

        if not (multi_year or multi_quarter or multi_month):
            return df  # rule 6

        # Build the pivot label
        if multi_year and has_quarter:                         # rule 2
            df["_pivot_label"] = df["year"].astype(str) + df["quarter"].str.upper()
            period_col = "_pivot_label"
        elif multi_year:                                       # rule 3
            period_col = "year"
        elif multi_quarter:                                    # rule 4
            period_col = "quarter"
        else:                                                  # rule 5 — multi-month
            month_map = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                         7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
            df["_pivot_label"] = df["month"].map(month_map)
            period_col = "_pivot_label"

        # Detect metric columns using allowlist first, dtype fallback second
        metric_cols = [c for c in df.columns if c in _KNOWN_METRICS]
        if not metric_cols:
            metric_cols = [
                c for c in df.columns
                if c not in _known_dim_cols
                and df[c].dtype in (float, int)
            ]

        dim_cols = [
            c for c in df.columns
            if c not in metric_cols
            and c != period_col
            and c not in ("_pivot_label", "year", "quarter", "month", "week")
        ]

        if not metric_cols or not dim_cols:
            return df  # not enough structure to pivot

        pivoted = pd.pivot_table(
            df, values=metric_cols, index=dim_cols,
            columns=period_col, aggfunc="first",
        )
        pivoted.columns = [f"{metric}_{period}" for metric, period in pivoted.columns]
        pivoted = pivoted.reset_index()

        if "_pivot_label" in df.columns:
            pivoted = pivoted.drop(columns=["_pivot_label"], errors="ignore")
        return pivoted

    except Exception:
        return df  # always fall back to original on any pivot failure
```

> ⚠️ **Metric detection**: always use `_KNOWN_METRICS` allowlist as the primary check. Never rely solely on `dtype == float/int` — numeric dim columns (e.g. `is_forecast: 0/1`, `week_of_year: 1–52`) will be misclassified as metrics if dtype inference is the only guard.

> ⚠️ **`aggfunc="first"` assumption**: the pivot assumes no duplicate (dim_cols, period) combinations in the result. This holds when the query groups at the same granularity every period. If duplicates are possible, use `aggfunc="sum"` for additive metrics and document the choice.

### `@register_function` patterns

**Dummy (section label for multi-answer flows — body is always `pass`):**

Dummies are **not** one-per-intent. They are section label stubs used by the multi-answer response renderer to label each result section. You only need one dummy per distinct `source` value that appears in `_SECTION_SOURCE_MAP`. The real orchestrator (with `_INTENT_MAP`) handles all routing — the template selector LLM points at the real orchestrator, not at individual dummies.

> **Watchtower-style pattern (recommended)**: When every intent maps to its own section name (e.g. `impact→"Impact"`, `roi→"ROI"`), create one dummy per intent. This makes every result section addressable by the summarizer prompt router, even for single-SP intents. Only strictly necessary for multi-SP intents, but having a dummy for every section is clean and explicit.

Section comment: `# <n>. Dummy Section Functions (one per section name in _SECTION_SOURCE_MAP)`

```python
@register_function("dummy_<section_label>", "<Human Section Name>")
async def dummy_<section_label>():
    pass
```

Example — if `_SECTION_SOURCE_MAP` has entries for `Impact`, `Input`, `ROI`, `Volume`, `Price`, `CPI`, `Cost`, create exactly 7 dummies — one per section name. Do **not** create dummies for intent names; dummies match section names (the values in `_SECTION_SOURCE_MAP`).

**Real orchestrator — single-SP (4-tuple return):**
```python
@register_function(
    "get_factual_data",
    "Factual Data Query",
    aliases=["getFactualData"],
)
async def get_factual_data(request_id, <params>: str = None, ...):
    """Fetches factual KPI data for a brand/country query."""
    df, query, table_refs, stored_proc = await get_brand_direct_kpis(
        request_id=request_id, <params>=<params>, ...
    )
    return df, query, table_refs, stored_proc
```

**Real orchestrator — multi-SP intent router (unified loop pattern):**

> **Design principle — simple table-name intents (recommended):**
> Intent values should be plain table names (e.g. `impact`, `input`, `roi`, `volume`, `price`, `cpi`, `cost`), not semantic workflow names (e.g. ~~`media_impact`~~, ~~`all_drivers`~~, ~~`cpi_decomposition`~~).
> - The LLM extracts **all** dimension filters explicitly (category, subcategory, signal, metric) — no forced params in `_INTENT_MAP`
> - Intent = SP routing only
> - When a user asks a semantic question ("media ROI"), the arguments selector maps it to the correct intent + explicit dimension params
> - This keeps `_INTENT_MAP` clean and makes the system easier to extend

Use a **unified loop** that handles both single-SP and multi-SP intents in the same code path:

```python
@register_function("get_data", "Factual Data", aliases=["getData"])
async def get_data(
    request_id,
    intent: str = None,
    section_name: str = "analysis",   # human label for the UI section
    <...params...>,
    use_case_name: str = "<usecase>",
):
    """Routes to the correct SP based on intent. Valid intents: impact, input, roi, volume, price, cpi, cost."""
    from .utils_functions import clean_and_join_values, get_change_columns

    intent = clean_and_join_values(intent) or "default_intent"
    section_name = clean_and_join_values(section_name) or "analysis"
    # ... clean all params ...

    # Intent maps to a fact table (SP name). No dimension filters forced.
    # The LLM extracts category/subcategory/signal/metric explicitly.
    _INTENT_MAP = {
        "impact":  {"sp": "impact",         "metric": "impact_hl"},
        "input":   {"sp": "input",          "metric": "input_level"},
        "roi":     {"sp": "roi",            "metric": "roi"},
        "volume":  {"sp": "volume",         "metric": "actual_hl"},
        "price":   {"sp": "price",          "metric": "price_cop"},
        "cpi":     {"sp": ["price", "cpi"], "metric": "price_cop|||#$#|||cpi"},
        "cost":    {"sp": "cost",           "metric": "cost"},
    }
    config = _INTENT_MAP.get(intent, _INTENT_MAP["impact"])
    sp_target = config["sp"]
    sp_names = [sp_target] if isinstance(sp_target, str) else list(sp_target)
    is_single_intent = isinstance(sp_target, str)

    # Maps intent → stored_proc name → display section name.
    # Include ALL intents explicitly (even single-SP) for clarity.
    _SECTION_SOURCE_MAP = {
        "impact": {"get_impact_kpis": "Impact"},
        "input":  {"get_input_kpis":  "Input"},
        "roi":    {"get_roi_kpis":    "ROI"},
        "volume": {"get_volume_kpis": "Volume"},
        "price":  {"get_price_kpis":  "Price"},
        "cost":   {"get_cost_kpis":   "Cost"},
        "cpi": {
            "get_price_kpis": "Price",
            "get_cpi_kpis":   "CPI",
        },
    }

    # ── Unified loop — runs all mapped SPs ───────────────────────────────────
    results = []
    for sp_name in sp_names:
        df, query, table_refs, stored_proc = await <dispatch_to_sp>(sp_name, **common_kwargs)
        if not df.empty:
            df = await post_processing(df, stored_proc_name=stored_proc)
        results.append((df, query, table_refs, stored_proc))

    valid = [(df, q, tr, sp) for df, q, tr, sp in results if df is not None and not df.empty]

    if len(valid) == 0:
        return None, None, None, None, None, None   # 6-tuple of None per executor contract

    if len(valid) == 1:
        df, query, table_refs, stored_proc = valid[0]
        records = df.to_dict(orient="records")
        change_columns = get_change_columns(records)
        return records, query, None, table_refs, change_columns, stored_proc

    # Multi-result: build section list
    section_results = []
    for df, query, table_refs, stored_proc in valid:
        records = df.to_dict(orient="records")
        source_name = _SECTION_SOURCE_MAP.get(intent, {}).get(stored_proc, section_name.title())
        section_results.append({
            "source": source_name,
            "sql_result": records,
            "sql_query": query,
            "chart_results": None,
            "table_references": table_refs,
            "change_columns": get_change_columns(records),
            "stored_proc": "Watchtower Data",
        })
    return section_results   # list[dict] — NOT a tuple
```

**Key rules for unified-loop orchestrators:**
- Never `pd.concat` multi-SP results — each SP has different columns and semantics
- `_SECTION_SOURCE_MAP` must include ALL intents (not just multi-SP ones) — enables per-intent summarizer prompt routing
- The `source_name` from `_SECTION_SOURCE_MAP` must exactly match the `at_simple_summarizer/<source_name>/` folder name
- The 0-result degenerate case must return a 6-tuple of `None` to match the executor contract
- The 1-result case returns a 6-tuple (records, query, chart, table_refs, change_columns, stored_proc)
- `get_change_columns(records)` requires importing from `utils_functions`

**`@register_function` decorator behavior:**
- `name` → key in REGISTRY; must match what the template selector LLM outputs
- `source_name` → human-readable label (UI labels, prompts); must be unique across all dummies
- `aliases` → optional alternative names; camelCase is auto-registered for any `snake_case` name
- `function_purpose` → pulled from the function's **docstring**; used by the template selector LLM — must be complete

---

## Notes & Gotchas

- **Lazy imports are mandatory.** Hoisting SP class or `utils_functions` imports to module level causes circular imports at startup. Every such import stays inside the function body.
- **The singleflight inflight dict prevents concurrency storms.** Do not remove it even for low-traffic use cases — it prevents redundant Databricks queries during any burst.
- **`stored_proc` in the return tuple must match the Langfuse key.** It is used to fetch the correct summarizer prompt. If there is no Langfuse prompt yet, match the naming convention and note that the prompt must be added.
- **Highlights wrappers return 5-tuples.** The calling LangGraph node checks tuple length before unpacking. Adding a 5-tuple wrapper requires verifying the node handles both shapes.
- **Dummies: one per section name in `_SECTION_SOURCE_MAP`.** Dummies are NOT one-per-intent unless every intent has its own section (Watchtower style). The template selector LLM routes to the real orchestrator; dummies provide labelling stubs for the response renderer.
- **`post_processing()` is one function, not one per SP.** Never create a separate function per wrapper.
- **`get_release_dates` `SELECT *` exception:** the static lookup form is acceptable only for tiny reference tables with no dynamic filtering. Never apply to fact tables.
- **Column renames happen in `post_processing`, not in the wrapper.** Keep internal column names in the wrapper; `post_processing` handles display names.
- **Intent design: keep intents simple.** Semantic intents (e.g. `media_impact`, `all_drivers`) that force dimension params are an anti-pattern — they bake LLM-layer decisions into the SP layer, make the system brittle to extend, and produce hard-to-debug errors when users combine signals across categories. Prefer table-name intents + explicit LLM-extracted dims.
- **Never re-aggregate in `post_processing`.** The DataFrame arriving here is already correctly aggregated by the SP SQL. Do not apply `AVG()`, `mean()`, or `groupby().agg()` on ratio or price columns inside `post_processing` — doing so would re-introduce the same weighted-average error that the SP was carefully designed to avoid. Rounding, melting, renaming, and sorting are the only transformations that belong here.
- **Name alignment is mandatory.** The `use_case_name` string, the functions file name prefix, and the `<usecase>` token in every lazy import path (`from .stored_procedures.<usecase>.<module>`) must all be the same string. Confirm the exact SP subdirectory name with the user — never invent a short alias.
- **Multi-SP orchestrators return a list, not a tuple.** When an intent routes to more than one SP (e.g. `cpi_decomposition`, `media_full_picture`), the return value is a `list[dict]` of section results, NOT a `pd.concat`-merged 4-tuple. Never flatten multi-SP results into one DataFrame — each SP has different columns and the downstream node needs to handle them independently. The 1-result degenerate case still returns a 4-tuple for backward compatibility.
