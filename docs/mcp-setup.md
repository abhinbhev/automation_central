# MCP Server Setup

MCP (Model Context Protocol) servers give Claude Code live access to external systems — ADO, GitHub, Teams, Outlook, SharePoint.

## Phase 1 — Local (current)

Each team member runs MCP servers on their own machine. See [configs/mcp/local/README.md](../configs/mcp/local/README.md) for the step-by-step guide.

## Phase 2 — Centralized (future)

When a shared MCP server is provisioned, see [configs/mcp/remote/README.md](../configs/mcp/remote/README.md).

Skills reference MCP tools by name only — switching from local to centralized requires no changes to skills.

## MCP Servers Used

| Server | What it enables | Install |
|---|---|---|
| `azure-devops` | Create/update work items, query boards, manage sprints | `npm i -g @modelcontextprotocol/server-azure-devops` |
| `github` | Read PRs, issues, diffs, repo contents | `npm i -g @modelcontextprotocol/server-github` |
| `microsoft-teams` | Draft and send Teams messages | via MS Graph MCP |
| `ms-graph` | Outlook email, SharePoint, OneDrive access | `npm i -g @modelcontextprotocol/server-msgraph` |
| `filesystem` | Read/write local files (templates, outputs) | built-in to Claude Code |

## Auth Notes

- **ADO**: Personal Access Token (PAT) with `Work Items Read & Write`, `Code Read`, `Build Read` scopes
- **GitHub**: Personal Access Token with `repo`, `read:org` scopes
- **MS Graph**: Azure AD app registration with delegated permissions — see `configs/mcp/local/README.md` for the app setup guide

Never commit tokens or secrets. Store them in environment variables or your OS credential store.
