---
mode: agent
description: Scaffold a GitHub Actions or Azure Pipelines CI/CD workflow from a description
---

Generate a CI/CD pipeline configuration from the following requirements.

Clarify only if target platform, environments, or required secrets are not specified.

**GitHub Actions standards:**
- Pin all actions to a full commit SHA or explicit version tag — never `@main` or `@master`
- Use `env:` block for all secrets — never inline
- Add `name:` to every step
- Use `concurrency:` to cancel in-progress runs on the same branch
- Cache dependencies (`pip`, `npm`, etc.) where applicable
- Use OIDC (`azure/login@v2` with `client-id`, `tenant-id`, `subscription-id`) for Azure auth — not long-lived secrets

**Azure Pipelines standards:**
- Use `displayName:` on every step
- Reference secrets via `$(VAR_NAME)` from variable groups — never hardcoded
- Production stages require a branch condition (`main` only) or manual approval gate
- Multi-stage pipelines: `CI` → `CD-staging` → `CD-production`

After generating the YAML:
- List every secret or variable the team must configure manually (name + where to set it)
- Note any manual steps required (role assignments, environment approvals, DNS)
- Flag any security or cost concerns with the proposed approach
