# Local MCP Setup

Each developer runs MCP servers locally. This guide covers installation, authentication, and wiring into Claude Code.

## Prerequisites

- Node.js 18+ (for npm-based servers)
- Claude Code CLI or VS Code extension
- Azure DevOps PAT
- GitHub PAT
- Azure AD app registration (for MS Graph)

## Step 1 — Install MCP servers

```bash
# ADO server
npm install -g @modelcontextprotocol/server-azure-devops

# GitHub server
npm install -g @modelcontextprotocol/server-github

# MS Graph (Teams, Outlook, SharePoint)
npm install -g @modelcontextprotocol/server-msgraph
```

## Step 2 — Create credentials

### ADO Personal Access Token
1. Go to `https://dev.azure.com/<your-org>/_usersSettings/tokens`
2. Create a token with scopes: `Work Items (Read & Write)`, `Code (Read)`, `Build (Read)`
3. Copy the token

### GitHub Personal Access Token
1. Go to GitHub → Settings → Developer Settings → Personal access tokens
2. Create a token with scopes: `repo`, `read:org`
3. Copy the token

### MS Graph (Azure AD App)
1. Go to Azure Portal → Azure Active Directory → App registrations → New registration
2. Name: `automation-central-mcp-local`
3. Add delegated permissions: `Mail.ReadWrite`, `Calendars.Read`, `Files.ReadWrite`, `Sites.ReadWrite.All`, `ChannelMessage.Send`
4. Grant admin consent
5. Create a client secret, copy it

## Step 3 — Set environment variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, or Windows Environment Variables):

```bash
export ADO_ORG_URL="https://dev.azure.com/<your-org>"
export ADO_PAT="<your-ado-pat>"
export GITHUB_TOKEN="<your-github-pat>"
export AZURE_TENANT_ID="<your-tenant-id>"
export AZURE_CLIENT_ID="<your-app-client-id>"
export AZURE_CLIENT_SECRET="<your-app-client-secret>"
```

## Step 4 — Configure Claude Code

Copy `mcp-settings.template.json` and merge it into your Claude Code settings.

In Claude Code, open settings (`/config`) and add the MCP servers section, or manually edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "azure-devops": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-azure-devops"],
      "env": {
        "ADO_ORG_URL": "${ADO_ORG_URL}",
        "ADO_PAT": "${ADO_PAT}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "ms-graph": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-msgraph"],
      "env": {
        "AZURE_TENANT_ID": "${AZURE_TENANT_ID}",
        "AZURE_CLIENT_ID": "${AZURE_CLIENT_ID}",
        "AZURE_CLIENT_SECRET": "${AZURE_CLIENT_SECRET}"
      }
    }
  }
}
```

## Step 5 — Verify

In Claude Code chat, ask: `"What ADO projects do I have access to?"`. If MCP is wired up correctly, Claude will query ADO and return a list.

## Troubleshooting

| Problem | Fix |
|---|---|
| `Command not found: npx` | Install Node.js 18+ |
| `ADO 401 Unauthorized` | Check PAT expiry and scopes |
| `MS Graph 403` | Ensure admin consent was granted for the app permissions |
| MCP server not appearing | Restart Claude Code after editing settings |

## Tested versions

| Server | Version | Date tested |
|---|---|---|
| `@modelcontextprotocol/server-azure-devops` | — | — |
| `@modelcontextprotocol/server-github` | — | — |
| `@modelcontextprotocol/server-msgraph` | — | — |

> Update this table when you set up or upgrade a server.
