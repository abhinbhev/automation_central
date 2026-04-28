---
name: ado-pipeline-yaml
description: Generate azure-pipelines.yml for a service or repo. Supports CI, CD, and multi-stage pipelines for Python, Node.js, Terraform, and Docker workloads.
domain: devops
requires_script: false
---

## Usage

Invoke with `/ado-pipeline-yaml` then provide:
- What the pipeline is for (e.g., "Python FastAPI service, deploy to Azure App Service")
- Target environments (e.g., `dev`, `staging`, `prod`)
- Key requirements: run tests, build Docker image, deploy IaC, etc.
- Trigger rules: on PR, on push to main, scheduled, manual

## Output

A complete `azure-pipelines.yml` with:
- `trigger` and `pr` blocks
- `stages` for CI and CD
- Named steps (every step has a `displayName`)
- Secrets referenced via `$(VAR_NAME)` — never hardcoded
- Comments explaining non-obvious sections

## Pipeline Patterns

### Python CI

```yaml
stages:
  - stage: CI
    jobs:
      - job: Test
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '3.11'
          - script: pip install -r requirements.txt
            displayName: Install dependencies
          - script: pytest tests/ --jq-report
            displayName: Run tests
          - task: PublishTestResults@2
```

### Multi-Stage CI → Dev → Prod

```yaml
stages:
  - stage: CI
  - stage: DeployDev
    dependsOn: CI
    condition: succeeded()
  - stage: DeployProd
    dependsOn: DeployDev
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
```

### Terraform

```yaml
steps:
  - script: terraform init
    displayName: Terraform Init
  - script: terraform plan -out=tfplan
    displayName: Terraform Plan
  - script: terraform apply tfplan
    displayName: Terraform Apply
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
```

## Steps

1. Identify the stack, stages, and trigger rules from the input
2. Select the appropriate pattern(s) from above
3. Generate the complete YAML
4. Add comments for non-obvious blocks
5. Highlight any variables that need to be configured in ADO Library
6. Suggest a `azure-pipelines.yml` file path and variable group name

## Security Checklist (always apply)

- All secrets via `$(VAR_NAME)` linked to ADO Variable Group or Key Vault
- `condition` on production deploy stages (branch check or approval gate)
- No `--allow-unauthenticated` or equivalent flags
- Docker builds use non-root user in Dockerfile (flag if deploying containers)
