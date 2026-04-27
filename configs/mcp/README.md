# MCP Servers

This directory contains configuration and setup guides for MCP (Model Context Protocol) servers.

## What are MCP servers?

MCP servers expose external tools — ADO, GitHub, Teams, Outlook — to AI assistants like Claude Code. Without them, Claude can only generate text; with them, it can actually query ADO, create work items, send Teams messages, and read emails.

## Which servers to install

| Server | Enables | Priority |
|---|---|---|
| `azure-devops` | Work items, sprints, boards, pipelines | High |
| `github` | PRs, issues, code diffs, repo contents | High |
| `ms-graph` | Outlook email, SharePoint, OneDrive, Teams | High |
| `filesystem` | Read/write local files | Built-in to Claude Code |

## Setup

- **Local (per-dev):** [local/README.md](local/README.md) — each developer installs and runs servers locally
- **Centralized (future):** [remote/README.md](remote/README.md) — team-hosted shared servers

## Switching from local to remote

Skills reference MCP tools by name (e.g., `mcp__azure_devops__create_work_item`). The tool names are the same regardless of whether the server is local or remote, so switching is transparent — only the Claude Code settings file changes.
