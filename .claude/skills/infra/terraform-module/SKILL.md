---
name: terraform-module
description: Scaffold a complete Terraform module — main.tf, variables.tf, outputs.tf, versions.tf, and README.md — for any Azure resource or logical grouping.
domain: infra
requires_script: false
---

## Usage

Invoke with `/terraform-module` then provide:
- What the module provisions (e.g., "Azure App Service with managed identity and Key Vault access")
- Resources needed (list them or describe the use case)
- Any naming conventions or tagging standards (uses team defaults if not specified)

## Output

A complete module with these files:

```
modules/<name>/
├── main.tf          # Resource definitions
├── variables.tf     # Input variable declarations with descriptions and types
├── outputs.tf       # Output value declarations
├── versions.tf      # Required provider versions
└── README.md        # Usage docs with example
```

## Team Terraform Conventions (always apply)

- Resource names: `snake_case`
- All resources must have: `environment`, `team`, `managed_by = "terraform"` tags
- Variable descriptions are mandatory
- Sensitive variables: `sensitive = true`
- Use `data` sources for existing resources — never hardcode IDs
- Lock provider versions: `~> X.Y` not `>= X`
- Use `locals {}` for computed name expressions
- Module should be self-contained — no reliance on remote state unless documented

## Template Structure

### `versions.tf`

```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.90"
    }
  }
}
```

### `variables.tf` pattern

```hcl
variable "resource_group_name" {
  description = "Name of the resource group to deploy into."
  type        = string
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "westeurope"
}

variable "tags" {
  description = "Additional tags to merge with the module defaults."
  type        = map(string)
  default     = {}
}
```

### `main.tf` pattern

```hcl
locals {
  common_tags = merge(
    {
      environment = var.environment
      team        = "abi-engineering"
      managed_by  = "terraform"
    },
    var.tags
  )
}
```

## Steps

1. Identify all resources needed from the description
2. Draft the file structure listing (which resources go in `main.tf`)
3. Generate `versions.tf` with appropriate provider versions
4. Generate `variables.tf` — all inputs with descriptions, no defaults for mandatory fields
5. Generate `main.tf` — resources with `locals` for tags and naming
6. Generate `outputs.tf` — expose IDs, names, and connection-relevant attributes
7. Generate `README.md` — with a usage block the caller can copy
8. Flag any resources that may need special permissions or role assignments

## README Template

```markdown
# module: <name>

Provisions <short description>.

## Resources Created
- `azurerm_*` — description

## Usage

\`\`\`hcl
module "<name>" {
  source = "./modules/<name>"
  resource_group_name = "rg-myapp-prod"
  location            = "westeurope"
}
\`\`\`

## Inputs
| Name | Description | Type | Required |
|------|-------------|------|----------|

## Outputs
| Name | Description |
|------|-------------|
```
