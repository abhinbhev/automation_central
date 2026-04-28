---
name: pipeline-docs
description: Document a data pipeline — inputs, outputs, transformations, schedule, dependencies, and failure handling. Accepts DAG config, pipeline code, or a description.
domain: data-ml
requires_script: false
---

## Usage

Invoke with `/pipeline-docs` then provide:
- Pipeline name and purpose
- Any of: Airflow DAG file, Azure Data Factory config, dbt model YAML, Python script, or a plain description
- Owner team and on-call contact (or `[TBD]`)

## Output

A complete pipeline documentation document:

```markdown
# Pipeline: <name>
**Owner:** [team]
**Last updated:** YYYY-MM-DD
**Schedule:** Daily at 02:00 UTC
**SLA:** Data available by 04:00 UTC

---

## Overview
[2-3 sentences: what does this pipeline do, why does it exist, who depends on it]

## Data Flow

\`\`\`mermaid
flowchart LR
  A[Source: Salesforce API] --> B[Ingest: Bronze Layer]
  B --> C[Transform: dbt models]
  C --> D[Load: Gold Layer / Power BI]
\`\`\`

## Inputs

| Source | Type | Frequency | Schema |
|--------|------|-----------|--------|
| Salesforce API | REST | Daily | [schema-docs link] |
| Reference table `dim_region` | Azure SQL | Static | [schema-docs link] |

## Transformations

| Step | Description | Tool |
|------|-------------|------|
| 1. Ingest | Pull records updated since last run, land in Bronze | Python / ADF |
| 2. Deduplicate | Remove duplicate order records by `order_id` | dbt |
| 3. Enrich | Join with `dim_region` on `region_code` | dbt |
| 4. Aggregate | Daily order counts and revenue by region | dbt |

## Outputs

| Destination | Table / Path | Consumers |
|-------------|-------------|-----------|
| Azure Data Lake | `gold/sales/daily_summary` | Power BI, Data Science team |

## Dependencies

- Upstream: `pipeline-crm-ingest` must complete before this runs
- Downstream: `pipeline-reporting-refresh` depends on this completing

## Schedule & SLA

- Runs: daily at 02:00 UTC (cron: `0 2 * * *`)
- Expected duration: ~45 minutes
- SLA breach: alert if not complete by 04:00 UTC

## Failure Handling

| Failure | Behaviour | Alert |
|---------|-----------|-------|
| Source API unavailable | Retry 3× with 10 min backoff, then fail | PagerDuty P2 |
| Transformation error | Fail the run, do not write partial data | Teams `#data-alerts` |
| SLA breach | No automatic action | Teams `#data-alerts` |

## Runbook
On failure → see [incident runbook](link) or use `/incident-runbook`.

## Change History
| Date | Change | Author |
|------|--------|--------|
| YYYY-MM-DD | Initial | [name] |
```

## Steps

1. Identify the pipeline name, schedule, and owner from the input
2. Parse the DAG/config/code or description to extract: sources, transforms, destinations
3. Build the Mermaid data flow diagram
4. Document inputs and outputs as tables
5. List each transformation step with the tool used
6. Identify upstream and downstream dependencies
7. Document failure modes and alerts
8. Ask for missing fields (SLA, on-call contacts) or mark as `[TBD]`
