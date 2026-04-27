# Centralized MCP Setup (Future)

This directory will hold the configuration and setup guide for a team-hosted MCP server.

## Status

Not yet provisioned. Current setup: each developer runs MCP servers locally (see [../local/README.md](../local/README.md)).

## When to migrate

Switch to a centralized server when:
- More than ~5 developers are using the tools (reduces per-dev setup friction)
- You want centralized audit logging of AI-tool actions
- You want to manage credentials in one place (secrets manager rather than per-dev env vars)

## Planned approach

Options to evaluate when this is needed:
1. **Azure Container Apps** — host MCP server containers, expose via HTTPS, auth via Azure AD
2. **Azure API Management** — proxy and rate-limit MCP tool calls
3. **Self-hosted VM** — simpler, lower cost for small teams

## Switching skills to remote

Skills reference MCP tool names (e.g., `mcp__azure_devops__create_work_item`). Tool names are identical regardless of server location. The only change is in each developer's Claude Code settings: replace the `command`/`args` local invocation with an `url` pointing to the remote server endpoint.

```json
{
  "mcpServers": {
    "azure-devops": {
      "url": "https://<your-mcp-server>/azure-devops",
      "headers": {
        "Authorization": "Bearer ${MCP_AUTH_TOKEN}"
      }
    }
  }
}
```
