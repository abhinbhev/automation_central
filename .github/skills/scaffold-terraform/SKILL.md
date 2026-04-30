---
name: scaffold-terraform
description: "Scaffold a Terraform module for Azure infrastructure from a description"
mode: agent
---

Generate a Terraform module for the following Azure infrastructure requirements.

Clarify only if the target environment, region variable, or resource names are genuinely ambiguous.

**Module structure — always produce all four files:**
- `main.tf` — resource definitions
- `variables.tf` — all inputs with `type`, `description`, and `default` where appropriate
- `outputs.tf` — all useful outputs with `description`
- `versions.tf` — required providers with locked versions (`~> X.Y`)

**Standards (always enforce):**
- Terraform >= 1.5 in the `required_version` constraint
- `snake_case` for all resource and variable names
- No hardcoded regions, subscription IDs, or tenant IDs — parameterise via variables
- Required tags on every resource:
  ```hcl
  tags = {
    environment = var.environment
    team        = var.team
    managed_by  = "terraform"
  }
  ```
- Use `locals {}` for repeated expressions — never duplicate values
- Use `data` sources for existing resources; never hardcode resource IDs
- Mark sensitive variables with `sensitive = true`
- Remote state: Azure Storage backend with state locking

After generating:
- List all variables the team must set (especially those without defaults)
- Note any manual prerequisites (resource groups, role assignments, service principals)
- Flag any security concerns (open NSG rules, public endpoints, over-permissive IAM)
- Remind to run `terraform fmt` and `terraform validate` before committing
