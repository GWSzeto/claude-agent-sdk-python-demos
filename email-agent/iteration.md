# Email Agent - Python Implementation Iterations

## TypeScript Demo Analysis

### Key Agentic Components

The TypeScript email-agent demo is a full-stack email client with these agentic components:

1. **MCP Tools**:
   - `search_inbox` - Query emails using Gmail-style syntax
   - `read_emails` - Retrieve full email content by message IDs

2. **Action Templates** (5 pre-defined):
   - Send payment reminders
   - Archive old newsletters
   - Summarize CEO weekly updates
   - Label urgent customer support emails
   - Forward bug reports to engineering

3. **Event Listeners** (6 types):
   - `email_received`, `email_sent`, `email_starred`
   - `email_archived`, `email_labeled`, `scheduled_time`

4. **Full Stack**: React frontend, Express backend, IMAP integration, WebSocket

### Workflow

```
User Query → search_inbox → read_emails → AI Analysis → Take Action
                                              ↓
                          (archive, label, forward, summarize, etc.)
```

---

## Python Implementation Approach

### Simplified Scope

We'll focus on the core agentic components without the full-stack UI:
- Mock email data (no IMAP integration)
- MCP tools for email operations
- Action templates as callable functions
- CLI interface for interaction

### Mock Data Structure

```python
MOCK_EMAILS = [
    {
        "id": "msg-001",
        "from": "ceo@company.com",
        "to": "team@company.com",
        "subject": "Weekly Update - Q4 Goals",
        "body": "Team, here are our Q4 priorities...",
        "date": "2024-01-15T09:00:00Z",
        "labels": ["important", "internal"],
        "is_read": True,
        "folder": "inbox"
    },
    # More emails...
]
```

### MCP Tools

| Tool | Purpose | New/Existing |
|------|---------|--------------|
| `search_inbox` | Search emails with Gmail-style queries | From TypeScript |
| `read_emails` | Get full email content by IDs | From TypeScript |
| `send_email` | Compose and send email (mock) | **NEW** |
| `archive_emails` | Move emails to archive | **NEW** |
| `label_emails` | Add/remove labels from emails | **NEW** |
| `get_email_stats` | Get inbox statistics | **NEW** |

---

## Iteration 1: Project Setup with Mock Email Data

**Goal**: Set up project structure with comprehensive mock email data.

**Requirements**:
- Create `mock_data.py` with 15-20 mock emails covering various scenarios:
  - CEO updates, newsletters, customer support tickets
  - Payment/invoice emails, bug reports
  - Varying dates, read status, labels
- Create helper functions to query the mock data
- Basic project structure with `pyproject.toml`

**Mock Data Scenarios**:
```python
# Categories to include:
# - CEO/Leadership updates (3-4 emails)
# - Newsletter subscriptions: TechCrunch, Morning Brew (3-4 emails)
# - Customer support tickets with urgency levels (3-4 emails)
# - Invoice/payment reminders from vendors (2-3 emails)
# - Bug reports from customers (2-3 emails)
# - General internal communications (2-3 emails)
```

**Helper Functions**:
```python
def search_emails(query: str, limit: int = 30) -> list[dict]:
    """Search emails using simple query matching."""
    pass

def get_emails_by_ids(ids: list[str]) -> list[dict]:
    """Get emails by their message IDs."""
    pass

def get_inbox_stats() -> dict:
    """Return statistics about the inbox."""
    pass
```

**Expected Structure**:
```
email-agent/
├── mock_data.py      # Mock emails and helper functions
├── pyproject.toml    # Project configuration
└── iteration.md      # This file
```

**Key Concepts Tested**:
- Data modeling for emails
- Query/filter functions
- Project organization

---

## Iteration 2: Basic MCP Tools (search_inbox, read_emails)

**Goal**: Create the core email MCP tools matching the TypeScript demo.

**Requirements**:
- Create `search_inbox` tool with Gmail-style query support
- Create `read_emails` tool to fetch full email content
- Set up MCP server with `create_sdk_mcp_server()`
- Basic agent that can search and read emails

**Gmail Query Syntax to Support**:
```
from:sender@email.com     - Filter by sender
to:recipient@email.com    - Filter by recipient
subject:keyword           - Filter by subject
is:unread                 - Unread emails only
is:read                   - Read emails only
label:important           - Filter by label
has:attachment            - Has attachments (mock)
newer_than:7d             - Within last N days
older_than:30d            - Older than N days
```

**Tool Definitions**:
```python
@tool("search_inbox", "Search emails using Gmail-style query syntax", {"query": str, "limit": int})
async def search_inbox(args: dict) -> dict:
    query = args["query"]
    limit = args.get("limit", 30)
    results = search_emails(query, limit)
    return {"content": [{"type": "text", "text": json.dumps(results, indent=2)}]}

@tool("read_emails", "Get full content of emails by their IDs", {"ids": list})
async def read_emails(args: dict) -> dict:
    ids = args["ids"]
    emails = get_emails_by_ids(ids)
    return {"content": [{"type": "text", "text": json.dumps(emails, indent=2)}]}
```

**Test Prompts**:
```
"Search for all unread emails"
"Find emails from the CEO"
"Show me emails with 'invoice' in the subject"
"Get the full content of email msg-001"
```

**Expected Output**:
```
[TOOL] search_inbox called with: {"query": "from:ceo@company.com"}
[ASSISTANT] I found 3 emails from the CEO. Here's a summary...
```

**Key Concepts Tested**:
- MCP tool creation with `@tool` decorator
- Query parsing and filtering
- Multiple tools in one MCP server

---

## Iteration 3: Email Action Tools (send, archive, label)

**Goal**: Add tools for email actions - sending, archiving, and labeling.

**Requirements**:
- Create `send_email` tool (mock - just logs the action)
- Create `archive_emails` tool (updates email status in mock data)
- Create `label_emails` tool (add/remove labels)
- Create `get_email_stats` tool for inbox statistics

**Tool Definitions**:
```python
@tool("send_email", "Compose and send an email", {
    "to": str,
    "subject": str,
    "body": str,
    "cc": str  # optional
})
async def send_email(args: dict) -> dict:
    # Mock sending - log the email details
    return {"content": [{"type": "text", "text": f"Email sent to {args['to']}"}]}

@tool("archive_emails", "Archive emails by their IDs", {"ids": list})
async def archive_emails(args: dict) -> dict:
    # Update mock data to mark emails as archived
    pass

@tool("label_emails", "Add or remove labels from emails", {
    "ids": list,
    "add_labels": list,      # Labels to add
    "remove_labels": list    # Labels to remove
})
async def label_emails(args: dict) -> dict:
    pass

@tool("get_email_stats", "Get statistics about the inbox", {})
async def get_email_stats(args: dict) -> dict:
    stats = get_inbox_stats()
    return {"content": [{"type": "text", "text": json.dumps(stats, indent=2)}]}
```

**Statistics to Track**:
```python
{
    "total_emails": 20,
    "unread_count": 5,
    "by_folder": {"inbox": 15, "archive": 5},
    "by_label": {"important": 4, "urgent": 2, "newsletter": 6},
    "by_sender_domain": {"company.com": 8, "techcrunch.com": 3}
}
```

**Test Prompts**:
```
"Archive all newsletters older than 30 days"
"Label the urgent customer emails as 'priority'"
"Send a reply to the CEO about the Q4 goals"
"Give me statistics about my inbox"
```

**Key Concepts Tested**:
- State mutation in mock data
- Complex tool parameters
- Multiple related tools working together

---

## Iteration 4: Agent Skills for Email Workflows

**Goal**: Create Agent Skills to provide domain-specific email management expertise.

**Background**: Agent Skills are filesystem-based capabilities that extend Claude with specialized knowledge. Unlike MCP tools (which execute code), Skills provide instructions, workflows, and best practices that Claude follows autonomously.

**Requirements**:
- Create 3 Skills in `.claude/skills/` directory:
  1. `email-triage` - Guidelines for prioritizing and organizing emails
  2. `newsletter-management` - Workflow for handling newsletter subscriptions
  3. `support-response` - Best practices for handling customer support emails
- Each Skill needs a `SKILL.md` file with YAML frontmatter
- Configure `setting_sources` to load Skills from the project

**Skill Directory Structure**:
```
email-agent/
├── .claude/
│   └── skills/
│       ├── email-triage/
│       │   └── SKILL.md
│       ├── newsletter-management/
│       │   └── SKILL.md
│       └── support-response/
│           └── SKILL.md
├── email_agent.py
├── mock_data.py
└── ...
```

**Skill 1: email-triage/SKILL.md**:
```yaml
---
name: email-triage
description: Guidelines for prioritizing and organizing emails. Use when asked to triage, prioritize, or organize an inbox.
---

# Email Triage Skill

## Priority Levels

Assign emails to priority levels based on these criteria:

### P0 - Critical (Immediate Action)
- Keywords: "urgent", "critical", "production down", "ASAP", "emergency"
- From: CEO, CTO, or executive leadership
- Customer support with "enterprise" label

### P1 - High (Same Day)
- Customer support tickets without urgent keywords
- Invoices marked overdue
- Bug reports with "P0" or "P1" priority

### P2 - Medium (This Week)
- Internal team communications
- Meeting requests
- Non-urgent customer inquiries

### P3 - Low (When Available)
- Newsletters
- Marketing emails
- FYI/informational emails

## Triage Workflow

1. Search for unread emails: `is:unread`
2. Identify P0/P1 emails first using keyword search
3. Label appropriately: "priority-critical", "priority-high", etc.
4. Summarize findings for the user

## Example Queries

- Find urgent emails: `is:unread subject:urgent OR subject:critical`
- Find executive emails: `from:ceo OR from:cto`
- Find overdue invoices: `subject:overdue OR subject:invoice`
```

**Skill 2: newsletter-management/SKILL.md**:
```yaml
---
name: newsletter-management
description: Workflow for managing newsletter subscriptions and archiving old newsletters. Use when asked about newsletters, subscriptions, or archiving marketing emails.
---

# Newsletter Management Skill

## Newsletter Sources

Common newsletter senders to identify:
- techcrunch.com
- morningbrew.com
- hackernews.com
- substack.com
- Medium digests

## Archival Policy

- Archive newsletters older than 30 days by default
- Never archive newsletters with "important" label
- Keep newsletters that were starred

## Management Workflow

1. Search for newsletters: `label:newsletter`
2. Identify old newsletters: `label:newsletter older_than:30d`
3. Archive in batches using `archive_emails` tool
4. Report count of archived emails

## Query Patterns

- All newsletters: `label:newsletter`
- Old newsletters: `label:newsletter older_than:30d`
- Specific source: `from:techcrunch.com`
```

**Skill 3: support-response/SKILL.md**:
```yaml
---
name: support-response
description: Best practices for handling customer support emails and bug reports. Use when dealing with support tickets, bug reports, or customer issues.
---

# Customer Support Response Skill

## Urgency Detection

Identify urgent support emails by:
- Keywords: "urgent", "critical", "down", "broken", "not working", "production"
- Enterprise customers (check for "enterprise" label)
- Bug reports marked P0 or P1

## Response Priority

1. **Production issues**: Acknowledge within 1 hour
2. **Enterprise customers**: Acknowledge within 4 hours
3. **Bug reports**: Triage within 24 hours
4. **General inquiries**: Respond within 48 hours

## Labeling Convention

- `urgent` - Needs immediate attention
- `enterprise` - From enterprise customer
- `bug-report` - Technical issue reported
- `billing` - Payment/invoice related

## Workflow

1. Search recent support emails: `to:support newer_than:1d`
2. Identify urgent issues with keyword search
3. Label appropriately using `label_emails` tool
4. Summarize open tickets for review

## Escalation Criteria

Escalate to engineering if:
- "data loss" mentioned
- Multiple customers report same issue
- Production environment affected
```

**Agent Configuration with Skills**:
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

options = ClaudeAgentOptions(
    mcp_servers={"email": email_tools},
    allowed_tools=[
        "mcp__email__search_inbox",
        "mcp__email__read_emails",
        "mcp__email__send_email",
        "mcp__email__archive_emails",
        "mcp__email__label_emails",
        "mcp__email__get_email_stats",
        "Skill"  # Enable Skills
    ],
    setting_sources=["project"],  # Load Skills from .claude/skills/
    cwd="/path/to/email-agent"     # Project directory
)
```

**Test Prompts**:
```
"Triage my inbox and identify urgent emails"
"Archive old newsletters from the past month"
"Help me handle the customer support tickets"
"What skills are available for email management?"
```

**Key Concepts Tested**:
- Skill creation with SKILL.md and YAML frontmatter
- `setting_sources` configuration for Skill discovery
- Combining MCP tools with Skills
- Domain-specific workflows and best practices

---

## Iteration 5: Hooks and CLI Integration (Final)

**Goal**: Add hooks for monitoring and complete CLI with shared module.

**Requirements**:
- PreToolUse hook to log all email operations
- Integrate Skills with CLI workflow
- CLI using shared `AgentCLI` module
- Support for direct queries and skill-based workflows

**Hook Implementation**:
```python
from typing import Any
from claude_agent_sdk import HookContext

async def log_email_operation(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all email and skill operations."""
    tool_name = input_data.get('tool_name', 'unknown')

    # Log MCP tool usage
    if tool_name.startswith('mcp__email__'):
        operation = tool_name.replace('mcp__email__', '')
        print(f"[EMAIL-OP] {operation}")

    # Log Skill invocation
    elif tool_name == 'Skill':
        skill_name = input_data.get('tool_input', {}).get('skill', 'unknown')
        print(f"[SKILL] Invoking: {skill_name}")

    return {}
```

**CLI Configuration**:
```python
from shared.cli import AgentCLI, CLIArgument

cli = AgentCLI(
    name="Email Agent",
    description="AI-powered email management using Claude Agent SDK with Skills",
    arguments=[
        CLIArgument(
            name="--query",
            short="-q",
            help="Direct query to execute (e.g., 'Find unread emails')"
        ),
        CLIArgument(
            name="--triage",
            short="-t",
            help="Run email triage workflow",
            action="store_true"
        ),
        CLIArgument(
            name="--archive-newsletters",
            help="Archive newsletters older than N days",
            arg_type=int,
            default=30
        ),
        CLIArgument(
            name="--verbose",
            short="-v",
            help="Show detailed tool and skill usage",
            action="store_true"
        ),
    ]
)
```

**Main Function**:
```python
async def run_agent(args) -> int:
    options = ClaudeAgentOptions(
        mcp_servers={"email": email_tools},
        allowed_tools=[
            "mcp__email__search_inbox",
            "mcp__email__read_emails",
            "mcp__email__archive_emails",
            "mcp__email__label_emails",
            "mcp__email__get_email_stats",
            "Skill"
        ],
        setting_sources=["project"],
        cwd=str(Path(__file__).parent),
        hooks={
            'PreToolUse': [HookMatcher(hooks=[log_email_operation])]
        } if args.verbose else {}
    )

    # Determine prompt based on CLI args
    if args.triage:
        prompt = "Triage my inbox. Identify urgent emails and prioritize them."
    elif args.archive_newsletters:
        prompt = f"Archive newsletters older than {args.archive_newsletters} days."
    elif args.query:
        prompt = args.query
    else:
        prompt = "Give me a summary of my inbox."

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        # ... handle response
```

**Usage Examples**:
```bash
# Direct query
python email_agent.py -q "Find all unread emails from the CEO"

# Triage workflow (uses email-triage Skill)
python email_agent.py --triage

# Archive newsletters (uses newsletter-management Skill)
python email_agent.py --archive-newsletters 30

# Verbose mode to see Skill invocations
python email_agent.py --triage -v
```

**Expected Output with Verbose**:
```
[SKILL] Invoking: email-triage
[EMAIL-OP] search_inbox
[EMAIL-OP] label_emails
[ASSISTANT] I've triaged your inbox. Found 3 urgent emails:
- P0: "URGENT: Production system down" from john.doe@acmecorp.com
- P1: "Critical Bug: Data loss on form submission" from user@enterprise.com
- P1: "Critical: Data export not working" from alex.wong@startup.co
```

**Key Concepts Tested**:
- Skills integration with hooks
- `setting_sources` for project-level Skills
- Combining MCP tools with Skill-based workflows
- CLI shortcuts for common Skill workflows

---

## Comparison Checklist

| Feature | TypeScript Demo | Python Implementation |
|---------|-----------------|----------------------|
| Email Search | `search_inbox` via IMAP | `search_inbox` MCP tool (mock) |
| Read Emails | `read_emails` via IMAP | `read_emails` MCP tool (mock) |
| Send Email | Full IMAP send | `send_email` tool (mock) |
| Archive | Gmail API | `archive_emails` tool (mock) |
| Labels | Gmail labels | `label_emails` tool (mock) |
| Actions | 5 templates (code-based) | 3 Skills (filesystem-based) |
| Listeners | 6 event types | Hooks (simplified) |
| UI | React frontend | CLI |
| Backend | Express + WebSocket | None (direct SDK) |

## Tools Summary

| Tool | Purpose | Notes |
|------|---------|-------|
| `search_inbox` | Gmail-style query search | Core tool from TS |
| `read_emails` | Get full email content | Core tool from TS |
| `send_email` | Compose/send emails | **NEW** (mock) |
| `archive_emails` | Archive emails | **NEW** (mock) |
| `label_emails` | Manage email labels | **NEW** (mock) |
| `get_email_stats` | Inbox statistics | **NEW** |

## Skills Summary

| Skill | Purpose | Trigger Keywords |
|-------|---------|------------------|
| `email-triage` | Prioritize and organize emails | triage, prioritize, organize, urgent |
| `newsletter-management` | Handle newsletter subscriptions | newsletters, archive, subscriptions |
| `support-response` | Handle customer support emails | support, tickets, bug reports, customer |

## Mock Data Categories

Ensure `mock_data.py` includes emails from:
1. **CEO/Leadership** (3-4): Weekly updates, announcements
2. **Newsletters** (4-5): TechCrunch, Morning Brew, Hacker News - varying ages
3. **Customer Support** (3-4): Tickets with varying urgency (urgent, normal)
4. **Invoices/Payments** (2-3): Overdue and upcoming
5. **Bug Reports** (2-3): From customers with severity levels
6. **Internal** (2-3): Team communications, meeting notes
