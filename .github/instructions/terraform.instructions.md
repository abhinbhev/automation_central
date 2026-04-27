---
applyTo: "**/*.tf,**/*.tfvars"
---

# Terraform Standards

- Terraform >= 1.5, provider versions pinned in `versions.tf`
- Module structure: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`, `README.md`
- Variable names: `snake_case`, descriptive, with `description` and `type` always set
- Outputs: always include a `description`
- Use `locals {}` for repeated expressions; avoid duplicating values
- Tag all resources with at minimum: `environment`, `team`, `managed_by = "terraform"`
- No hardcoded regions or subscription IDs — parameterize via variables
- Run `terraform fmt` and `terraform validate` before committing
