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

## Iteration 4: Action Templates

**Goal**: Implement pre-defined action templates that users can execute.

**Requirements**:
- Create action template system for common email workflows
- Implement 3 action templates from the TypeScript demo:
  1. Archive old newsletters
  2. Summarize CEO updates
  3. Label urgent customer support emails
- Actions should be invokable by name with parameters

**Action Template Structure**:
```python
@dataclass
class ActionTemplate:
    id: str
    name: str
    description: str
    parameters: dict[str, Any]  # Parameter definitions with defaults
    prompt_template: str         # Prompt to send to agent

ACTION_TEMPLATES = {
    "archive_old_newsletters": ActionTemplate(
        id="archive_old_newsletters",
        name="Archive Old Newsletters",
        description="Archive newsletter emails older than N days",
        parameters={"days_old": {"type": int, "default": 30}},
        prompt_template="Search for newsletter emails older than {days_old} days and archive them."
    ),
    "summarize_ceo_updates": ActionTemplate(
        id="summarize_ceo_updates",
        name="Summarize CEO Updates",
        description="Generate a summary of CEO weekly update emails",
        parameters={"weeks_back": {"type": int, "default": 4}},
        prompt_template="Find CEO update emails from the past {weeks_back} weeks and provide a summary."
    ),
    "label_urgent_support": ActionTemplate(
        id="label_urgent_support",
        name="Label Urgent Support Emails",
        description="Label urgent customer support emails",
        parameters={"hours_back": {"type": int, "default": 24}},
        prompt_template="Find customer support emails from the last {hours_back} hours containing urgent keywords and label them as 'urgent'."
    )
}
```

**MCP Tool for Actions**:
```python
@tool("execute_action", "Execute a pre-defined email action template", {
    "action_id": str,
    "parameters": dict  # Override default parameters
})
async def execute_action(args: dict) -> dict:
    action_id = args["action_id"]
    params = args.get("parameters", {})

    template = ACTION_TEMPLATES.get(action_id)
    if not template:
        return {"content": [{"type": "text", "text": f"Unknown action: {action_id}"}]}

    # Merge defaults with provided params
    final_params = {**template.parameters_defaults, **params}
    prompt = template.prompt_template.format(**final_params)

    return {"content": [{"type": "text", "text": f"Executing: {prompt}"}]}

@tool("list_actions", "List all available action templates", {})
async def list_actions(args: dict) -> dict:
    actions = [{"id": a.id, "name": a.name, "description": a.description}
               for a in ACTION_TEMPLATES.values()]
    return {"content": [{"type": "text", "text": json.dumps(actions, indent=2)}]}
```

**Test Prompts**:
```
"What actions are available?"
"Execute the archive_old_newsletters action"
"Run the summarize_ceo_updates action for the last 2 weeks"
"Label urgent support emails from the last 12 hours"
```

**Key Concepts Tested**:
- Template-based workflows
- Parameter merging and defaults
- Dynamic prompt generation

---

## Iteration 5: Hooks and CLI Integration (Final)

**Goal**: Add hooks for monitoring and complete CLI with shared module.

**Requirements**:
- PreToolUse hook to log all email operations
- PostToolUse hook to track action statistics
- CLI using shared `AgentCLI` module
- Interactive and single-command modes

**Hook Implementations**:
```python
# Track statistics across the session
session_stats = {"searches": 0, "emails_read": 0, "emails_archived": 0, "emails_labeled": 0}

async def log_email_operation(input_data: dict, tool_use_id: str | None, context: HookContext) -> dict:
    """Log all email tool operations."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[EMAIL-OP] {tool_name}")
    return {}

async def track_statistics(output_data: dict, tool_use_id: str | None, context: HookContext) -> dict:
    """Track usage statistics after tool execution."""
    tool_name = output_data.get('tool_name', 'unknown')
    if tool_name == 'search_inbox':
        session_stats['searches'] += 1
    elif tool_name == 'read_emails':
        session_stats['emails_read'] += 1
    # ... etc
    return {}
```

**CLI Configuration**:
```python
cli = AgentCLI(
    name="Email Agent",
    description="AI-powered email management using Claude Agent SDK",
    arguments=[
        CLIArgument(
            name="--query",
            short="-q",
            help="Direct query to execute (e.g., 'Find unread emails from CEO')"
        ),
        CLIArgument(
            name="--action",
            short="-a",
            help="Execute a pre-defined action (e.g., 'archive_old_newsletters')"
        ),
        CLIArgument(
            name="--interactive",
            short="-i",
            help="Run in interactive mode",
            action="store_true"
        ),
        CLIArgument(
            name="--verbose",
            short="-v",
            help="Show detailed tool usage",
            action="store_true"
        ),
        CLIArgument(
            name="--stats",
            short="-s",
            help="Show session statistics at end",
            action="store_true"
        ),
    ]
)
```

**Usage Examples**:
```bash
# Direct query
python email_agent.py -q "Find all unread emails and summarize them"

# Execute action
python email_agent.py -a archive_old_newsletters

# Execute action with parameters
python email_agent.py -a summarize_ceo_updates --params '{"weeks_back": 2}'

# Interactive mode
python email_agent.py -i

# With statistics
python email_agent.py -q "Archive newsletters" --stats
```

**Key Concepts Tested**:
- PreToolUse and PostToolUse hooks
- Session state management
- Shared CLI integration
- Multiple execution modes

---

## Comparison Checklist

| Feature | TypeScript Demo | Python Implementation |
|---------|-----------------|----------------------|
| Email Search | `search_inbox` via IMAP | `search_inbox` MCP tool (mock) |
| Read Emails | `read_emails` via IMAP | `read_emails` MCP tool (mock) |
| Send Email | Full IMAP send | `send_email` tool (mock) |
| Archive | Gmail API | `archive_emails` tool (mock) |
| Labels | Gmail labels | `label_emails` tool (mock) |
| Actions | 5 templates | 3 templates (subset) |
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
| `execute_action` | Run action templates | **NEW** |
| `list_actions` | List available actions | **NEW** |

## Mock Data Categories

Ensure `mock_data.py` includes emails from:
1. **CEO/Leadership** (3-4): Weekly updates, announcements
2. **Newsletters** (4-5): TechCrunch, Morning Brew, Hacker News - varying ages
3. **Customer Support** (3-4): Tickets with varying urgency (urgent, normal)
4. **Invoices/Payments** (2-3): Overdue and upcoming
5. **Bug Reports** (2-3): From customers with severity levels
6. **Internal** (2-3): Team communications, meeting notes
