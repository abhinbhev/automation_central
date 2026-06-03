# PR-011 — Data Engineer Agent (Claude + Copilot Pair)

**Phase:** 2 — Content Expansion
**Type:** New agent pair + new skills
**Story Points:** 5
**Priority:** P3 — Medium
**Depends on:** PR-005 (Copilot parity — ensures new skills have both frameworks from day one)
**Blocks:** PR-015 (orchestrator needs the DE agent to exist)

---

## Problem Statement

TODO #2 identifies a missing Data Engineer agent. The repo has a `data-ml` domain with 3 skills (`schema-docs`, `pipeline-docs`, `model-card`) but no dedicated agent that embodies a DE persona. The closest existing agent is `coder` — but DEs on the team have distinct workflows: schema documentation, pipeline design, SQL stored procedure scaffolding, and model cards. A dedicated `data-engineer` agent provides the right context, tools, and skill references without conflating DE work with general software engineering.

---

## Scope

### New Agent Pair
- `.claude/agents/data-engineer.agent.md`
- `.github/agents/data-engineer.agent.md`

### Skills to Reference (existing)
- `data-ml/schema-docs`
- `data-ml/pipeline-docs`
- `data-ml/model-card`
- `coding/scaffold-stored-procedure`
- `coding/scaffold-sp-wrapper`
- `coding/scaffold-at-prompts`

### New Skills (if gaps identified during creation)
- `data-ml/eda-report` — exploratory data analysis report (relates to TODO #1 "Ingest EDA for IC skill")
- `data-ml/data-quality-check` — data quality validation spec

---

## Requirements

| ID | Requirement |
|----|-------------|
| R1 | `.claude/agents/data-engineer.agent.md` with valid frontmatter (`name`, `description`, `skills:`) |
| R2 | `.github/agents/data-engineer.agent.md` with valid frontmatter (`description`, `tools:`) |
| R3 | Both agents have `## Relevant Skills` section referencing all 6 existing skills |
| R4 | Both agents pass `validate_agent.py` with zero errors |
| R5 | Agent persona covers: schema documentation, pipeline design, SQL scaffolding, model cards, EDA |
| R6 | Agent boundaries explicitly exclude: infrastructure provisioning (use `devops-engineer`), ADO work item creation (use `ado-manager`) |
| R7 | If `data-ml/eda-report` skill is created: it follows full Claude + Copilot creation workflow |
| R8 | Catalog updated after all additions |
| R9 | `sync_check.py` reports clean after this PR |

---

## User Stories

**US-1 — Data engineer on the team**
> As a data engineer, I want a dedicated agent mode that understands my domain — schemas, pipelines, stored procedures, and ML model cards — so I get relevant, context-rich responses without having to explain my role every time.

*Acceptance Criteria:*
1. Selecting `data-engineer` agent mode in Claude Code/Copilot loads the correct persona.
2. The agent automatically references `schema-docs`, `scaffold-stored-procedure`, and `pipeline-docs` when relevant.
3. The agent declines infra provisioning requests and redirects to `devops-engineer`.
4. The agent description is consistent between Claude and Copilot versions.

**US-2 — EDA reporting**
> As a data engineer or analyst, I want a `/eda-report` skill to generate a structured exploratory data analysis report from a dataset schema or summary statistics.

*Acceptance Criteria:*
1. `.claude/skills/data-ml/eda-report/SKILL.md` exists with all required sections.
2. `.github/skills/eda-report/SKILL.md` exists (Copilot counterpart).
3. The skill produces a structured EDA report with sections: dataset overview, column statistics summary, identified distributions, missing value analysis, recommended next steps.
4. Validator passes on both skill files.

---

## Tasks

| # | Task | Owner | Estimate |
|---|------|-------|----------|
| T1 | Define DE agent persona, capabilities, and boundaries (document before writing) | Dev | 30m |
| T2 | Create `.claude/agents/data-engineer.agent.md` with frontmatter and full body | Dev | 45m |
| T3 | Create `.github/agents/data-engineer.agent.md` (Copilot pair) | Dev | 30m |
| T4 | Run `validate_agent.py` on both files — fix any issues | Dev | 15m |
| T5 | Create `.claude/skills/data-ml/eda-report/SKILL.md` | Dev | 45m |
| T6 | Run `validate_skill.py` on eda-report | Dev | 10m |
| T7 | Create `.github/skills/eda-report/SKILL.md` (Copilot counterpart) | Dev | 20m |
| T8 | Run `generate_catalog.py` | Dev | 5m |
| T9 | Run `sync_check.py` — confirm clean | Dev | 5m |
| T10 | Update `README.md` agent table with `data-engineer` entry | Dev | 10m |

**Total estimate: ~4.5h → 5 story points**

---

## Agent Persona Outline

**Name:** `data-engineer`
**Description:** Data engineering specialist — schema documentation, pipeline design, SQL scaffolding, and ML model cards. Use for data modelling, EDA, and stored procedure development.

**Capabilities:**
- Schema documentation from DDL or live DB connections
- Pipeline documentation (Airflow, ADF, dbt, generic)
- Stored procedure scaffolding (with helpers, public method, `_build_query`)
- SP wrapper functions layer scaffolding
- ML model card generation
- EDA report generation from schema/stats summary
- Analysis Template (AT) prompt scaffolding

**Boundaries:**
- Does not provision infrastructure — use `devops-engineer`
- Does not create ADO work items — use `ado-manager`
- Does not write frontend or API code — use `coder`

---

## Acceptance Criteria (PR-level)

1. Both agent files exist and pass `validate_agent.py` with zero errors.
2. `data-engineer` appears in `docs/automation-catalog.md` after catalog regeneration.
3. `eda-report` Claude and Copilot skills exist and pass validators.
4. `sync_check.py` reports zero agent pair errors and zero parity warnings for new files.
5. Agent `description` is identical between Claude and Copilot frontmatter.

---

## PR Title

`feat(data-ml): add data-engineer agent pair and eda-report skill`
