# automation_central

Central hub for the ABI engineering team's AI-assisted agents, skills, scripts, and templates. Supports both **Claude Code** and **GitHub Copilot** as AI frameworks, with shared Python scripts and templates underneath.

## What's here

| Directory | Purpose |
|---|---|
| `.claude/agents/` | Claude Code agent modes (7 agents) |
| `.claude/skills/` | Claude Code skills invoked with `/skill-name` (26 skills) |
| `.github/agents/` | GitHub Copilot agent modes (7 agents) |
| `.github/prompts/` | GitHub Copilot slash-command prompts (6 prompts) |
| `.github/instructions/` | Scoped coding instructions (Python, ADO, Terraform) |
| `scripts/` | Python scripts called by skills (14 scripts) |
| `templates/` | HTML presentation templates, Word, Excel, ADO, IaC templates |
| `configs/` | MCP server configs, conda environment |
| `docs/` | Documentation, onboarding, catalog |

## Quick Start

1. Clone and open this folder as a VS Code workspace
2. Install recommended extensions — VS Code will prompt you, or run **Extensions: Show Recommended Extensions**
3. Set up the Python environment:
   ```bash
   conda env create -f configs/envs/conda-env.yml
   conda activate automation-central
   ```
4. Configure MCP servers → see [docs/mcp-setup.md](mcp-setup.md)
5. Try your first skill in Claude Code: type `/meeting-minutes` and paste some notes

Full onboarding walkthrough: [docs/onboarding.md](onboarding.md)

## Automation Catalog

Full list of all skills, agents, and scripts: [docs/automation-catalog.md](automation-catalog.md)

> The catalog is auto-generated. Run `python scripts/repo/generate_catalog.py` to rebuild it after adding new skills.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) or [docs/contributing.md](contributing.md). TL;DR: branch off `main`, add your skill/agent/script, run the validator, open a PR.

## Frameworks Supported

| Framework | Config location | How to activate |
|---|---|---|
| **Claude Code** | `.claude/` | Open this folder as workspace; Claude Code loads `.claude/CLAUDE.md` automatically |
| **GitHub Copilot** | `.github/` | Open this folder as workspace; Copilot reads `.github/copilot-instructions.md` |
