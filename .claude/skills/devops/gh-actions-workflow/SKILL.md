---
name: gh-actions-workflow
description: Generate GitHub Actions workflow YAML for CI, CD, scheduled jobs, or automation. Supports Python, Node.js, Docker, and Terraform.
domain: devops
requires_script: false
---

## Usage

Invoke with `/gh-actions-workflow` then provide:
- What the workflow does (e.g., "run pytest on PR, build and push Docker image on merge to main")
- Triggers: `push`, `pull_request`, `schedule`, `workflow_dispatch`, etc.
- Stack: Python / Node.js / Docker / Terraform / other
- Target: where things deploy (Azure, GCP, self-hosted runner, etc.)

## Output

A complete `.github/workflows/<name>.yml` with:
- Pinned action versions (e.g., `actions/checkout@v4`, never `@main`)
- `name:` on every step
- Secrets via `${{ secrets.VAR_NAME }}` — never hardcoded
- `env:` block at job or step level for non-secret config
- Concurrency control to prevent redundant runs

## Workflow Patterns

### Python CI (test + lint)

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v
      - name: Lint
        run: ruff check .
```

### Docker Build + Push (on merge to main)

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    push: ${{ github.ref == 'refs/heads/main' }}
    tags: ${{ secrets.ACR_LOGIN_SERVER }}/app:${{ github.sha }}
```

### Terraform Plan / Apply

```yaml
- name: Terraform Init
  run: terraform init
  env:
    ARM_CLIENT_ID: ${{ secrets.ARM_CLIENT_ID }}
    ARM_CLIENT_SECRET: ${{ secrets.ARM_CLIENT_SECRET }}
    ARM_TENANT_ID: ${{ secrets.ARM_TENANT_ID }}
    ARM_SUBSCRIPTION_ID: ${{ secrets.ARM_SUBSCRIPTION_ID }}
```

## Steps

1. Identify triggers, jobs, and steps from the input
2. Select patterns from above and compose the full workflow
3. Pin all action versions
4. Add concurrency control if appropriate (CI workflows should cancel stale runs)
5. List all secrets that need to be added to the GitHub repo settings
6. Suggest the file path: `.github/workflows/<descriptive-name>.yml`

## Security Rules (always enforce)

- Pin action versions with SHA or version tag — never `@main` or `@latest`
- Never echo secrets in `run:` steps
- Use `pull_request_target` only when you understand the security implications — prefer `pull_request`
- Add `permissions:` block with minimal scope if modifying repo resources
- For deployments: use OIDC (`azure/login` with federated credentials) over long-lived secrets where possible
