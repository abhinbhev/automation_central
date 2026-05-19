---
name: scaffold-sp-wrapper
description: "Interactively scaffold the async wrapper functions layer (`<usecase>_functions.py`) that sits between SP class files and the LangGraph orchestrator — covers raw SP wrappers, release-date caching, post_processing(), and @register_function concept functions"
mode: agent
---

You are scaffolding a `<usecase>_functions.py` wrapper layer. This file sits between SP class files (see `scaffold-stored-procedure`) and the LangGraph orchestrator. It contains: the release-date singleflight cache, raw async SP wrapper functions, a single `post_processing()` dispatch function, and `@register_function` concept functions.

All canonical code patterns are embedded in the Claude skill at `.claude/skills/coding/scaffold-sp-wrapper/SKILL.md` under ## Reference Patterns. Use those patterns directly.

---

## Interview (run in order)

### Step 1 — File identity
Ask together:
- Full output file path (`<usecase>_functions.py`). **The file name must be `<use_case_name>_functions.py` using the exact `use_case_name` string — do not shorten or alias it.**
- Use case name string (e.g. `gai_copilot_marketing_brand_guidance_ghq`). This must match:
  1. The file name prefix
  2. The subdirectory name under `stored_procedures/` in every lazy import
  Using a short alias (e.g. `watchtower_mmm` when the SP subdir is `gai_copilot_marketing_watchtower_ghq`) causes `ModuleNotFoundError`. Always confirm the exact subdir name.
- Logger import path (fallback: `import logging; logger = logging.getLogger(__name__)`)

### Step 2 — Release-date cache
Ask as one block:
- Release-date table FQN + column names (`country`, `release_date`)
- Date formats to try (default: `%d-%m-%Y` then `%Y-%m-%d`)
- No release-date concept? → omit `get_release_dates` and both module-level cache dicts entirely

### Step 3 — Raw SP wrappers (loop until done)
For each wrapper collect:
- SP function name + SP class name + relative module path
- Full parameter list (all `str = None` except confirmed demographic defaults like `age="All"`)
- Country-scoped vs global release-date call
- `decimal_precision` (default `1`)
- Return shape: 4-tuple or 5-tuple (highlights); `stored_proc` as plain string or multilingual dict
- Title-case columns (default: country, brand, brand_family, age, gender, region, income, life_cycle, price_segment, abi_comp, zone, market_maturity, global_brand, imagery)
- Special transforms: column renames, boolean → label replacements
- `table_references` list (uppercase, no schema prefix)
- Static lookup (no SP class)? → emit slim `SELECT * FROM <table>` form

### Step 4 — `post_processing()` function
One function, one `elif stored_proc_name == "..."` branch per SP (in case of multiple SPs that can share a post-processing pattern, use conditional logic within the branch to handle differences). For each SP, ask:
- Wide (melt needed) or long format (already has `value` column)?
- KPI sort order for melted SPs
- Column renames for display (internal → UI name)
- Decimal precision (default `1`)

### Step 5 — `@register_function` concept functions (loop until done)
For each:
- Registered name, source name (unique, human-readable), optional aliases
- Dummy (`pass`) or real orchestrator? If real: which raw wrappers, which params pass through?
- Docstring (becomes `function_purpose` in LLM prompt — must be complete)
- **For dummies**: create one dummy per distinct `source_name` in `_SECTION_SOURCE_MAP` — NOT one per intent. Exception (Watchtower-style): when every intent maps to its own unique section, one-per-intent = one-per-section, which is fine. Dummies are section label stubs for the response renderer, not routing targets.

---

## Generation rules

### File structure (top to bottom)
1. Module imports: `asyncio`, `time`, `datetime`, `Decimal`, `numpy as np`, `pandas as pd`, logger, `register_function`
2. Module-level: `_release_date_cache: dict[str, tuple] = {}` + `_release_date_inflight: dict[str, asyncio.Future] = {}`
3. `async def get_release_dates(...)` — singleflight cache, normalize country to uppercase, try both date formats, cache failures as `(None, None, None, None)`
4. Raw SP wrappers with `# <n>. <label>` section comments
5. `post_processing(df, stored_proc_name, ...)` — single dispatch function
6. `@register_function` functions

### Mandatory rules
- **Lazy imports** — every SP class import and `utils_functions` import is inside the function body; never at module level (circular import risk)
- `clean_and_join_values(val)` applied to every parameter before the SP class call, without exception
- `logger.bind(request_id=request_id).info(...)` bind pattern on all operational log lines
- No `logger.debug` / `logger.trace` — use `logger.info` + `logger.warning` only
- `post_processing` is ONE function — never split it per SP
- Dummy `@register_function` functions have body `pass` — create only as many as there are distinct `source_name` values in `_SECTION_SOURCE_MAP`. Do NOT create one dummy per intent — this over-bloats the registry and misleads the template selector LLM.
- **`_SECTION_SOURCE_MAP` must include ALL intents** (not just multi-SP ones). This ensures every intent's result has an explicit display section name, and per-intent summarizer prompts are always reachable. Map each intent to `{stored_proc_name: "Human Section Name"}`.
- **Intent design — prefer table-name intents.** Use plain table names as intent values (e.g. `impact`, `input`, `roi`, `volume`, `price`, `cpi`, `cost`) rather than semantic workflow names (e.g. ~~`media_impact`~~, ~~`all_drivers`~~). Intent = SP routing only. The LLM extracts all dimension filters (category, subcategory, signal) as explicit separate parameters. No forced/hidden params in `_INTENT_MAP`.
- `utils_functions` import lists specific names: never `import *`
- **Never re-aggregate in `post_processing`.** The DataFrame arriving here is already correctly aggregated by the SP SQL. Do not apply `mean()`, `AVG`, or `groupby().agg()` on ratio or price columns — doing so re-introduces weighted-average errors the SP was designed to avoid. Only rounding, melting, renaming, and sorting belong here.
- **Name alignment is mandatory.** The `use_case_name` string, the functions file name prefix, and the `<usecase>` token in every lazy import (`from .stored_procedures.<usecase>.<module>`) must all be the same string. Confirm the exact SP subdirectory name with the user — never invent a short alias.
- **Multi-SP orchestrators return a list, not a tuple.** When an intent routes to more than one SP (e.g. `cpi` = price + cpi), the return value is `list[dict]` of section results — NOT a `pd.concat`-merged 4-tuple. Use a **unified loop** pattern that handles both single-SP and multi-SP intents — avoids duplication and is easier to extend. The 0-result degenerate case returns a 6-tuple of `None`; the 1-result case returns a 6-tuple (records, query, chart, table_refs, change_columns, stored_proc). Never flatten multi-SP results into one DataFrame. See Claude skill for the full canonical pattern.
- **Add `_apply_period_pivot` to `post_processing`** when the use case spans multiple years or quarters. Decision tree: week present → skip; multi-year + quarter → pivot label `2024Q1`; multi-year only → `2024`; single year + multi-quarter → `Q1`; multi-month → `Jan`. Use `_KNOWN_METRICS` allowlist as primary metric detection — never rely on dtype-only inference (numeric dim columns like `is_forecast` or `week_of_year` will be misclassified). See Claude skill for the full implementation.

### `get_release_dates` pattern
```python
async def get_release_dates(request_id="release_date_pull", country: str = "default", use_case_name: str = "<usecase>"):
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
    # ... query Databricks, parse dates, cache result, resolve future, finally pop inflight
```

### Raw SP wrapper pattern
```python
async def <sp_name>(request_id, <params>: str = None, ..., use_case_name: str = "<usecase>") -> tuple:
    """One-sentence description of what data this retrieves."""
    from .stored_procedures.<usecase>.<module> import <ClassName>
    from .utils_functions import clean_and_join_values, execute_databricks_query

    param = clean_and_join_values(param)  # apply to every param
    release_date, _, _, _ = await get_release_dates(request_id=request_id, country=country, use_case_name=use_case_name)
    logger.bind(request_id=request_id).info(f"Release date for country {country} is: {release_date}")

    handler = <ClassName>()
    query = handler.<sp_method>(<params>, release_date=release_date)

    payload = {"query": query, "decimal_precision": 1, "use_case": use_case_name}
    logger.bind(request_id=request_id).info(f"Final payload for databricks is: {payload}")
    response_data = await execute_databricks_query(payload, use_case_name)

    if not response_data:
        logger.warning(f"No data returned from the query with payload {payload}.")
        return pd.DataFrame(), None, None, None
    response_data_df = pd.DataFrame(response_data)

    for col in [<title_case_columns>]:
        if col in response_data_df.columns:
            response_data_df[col] = response_data_df[col].astype(str).str.title()

    table_references = [<UPPERCASE_TABLE_NAMES>]
    stored_proc = "<sp_name>"
    return response_data_df, query, table_references, stored_proc
```

### After writing the file
Print:
1. File path written
2. `__init__.py` reminder: add `from . import <usecase>_functions` to `analysis_template_executor/__init__.py`
3. Registry verification: `python -c "from <pkg>.analysis_template_executor.function_registry import REGISTRY; print(list(REGISTRY.keys()))"`

---

## Relevant Skills

- `.claude/skills/coding/scaffold-sp-wrapper/SKILL.md`
- `.claude/skills/coding/scaffold-stored-procedure/SKILL.md`
