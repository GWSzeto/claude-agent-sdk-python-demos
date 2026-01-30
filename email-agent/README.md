# Email Agent

An AI-powered email management system that can search, triage, archive, and label emails.

## What It Does

- Search emails using Gmail-style queries
- Triage inbox by priority (P0-P3)
- Archive old newsletters
- Label and organize emails
- Handle customer support tickets

## Techniques Used

- **MCP Tools** - Custom tools for email operations (search, read, archive, label)
- **Routing** - Directs requests to appropriate workflows based on intent
- **Skills** - Domain knowledge for email triage, newsletter management, and support handling
- **Orchestrator-Workers** - Specialized subagents for parallel email processing (triage, support, newsletters)
