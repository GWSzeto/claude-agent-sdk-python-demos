
import sys
from pathlib import Path
import json

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, TextBlock, ToolUseBlock, create_sdk_mcp_server, tool, HookMatcher, AgentDefinition
from mock_data import add_label, archive_email, get_emails_by_ids, get_inbox_stats, remove_label, search_emails
from shared.cli import AgentCLI, CLIArgument, run_agent_cli

agents = {
    "triage-agent": AgentDefinition(
        description="Email prioritization specialist. Use for inbox triage, urgency detection, and priority labeling.",
        prompt="""You are an email triage specialist. Your job is to:
        1. Identify urgent and high-priority emails
        2. Classify emails by urgency: P0 (critical), P1 (high), P2 (medium), P3 (low)
        3. Label emails appropriately using the label_emails tool

        Priority Criteria:
        - P0: Keywords "urgent", "critical", "production down", "ASAP"; from executives
        - P1: Customer support without urgen keywords; overdue invoices; P0/P1 bug reports
        - P2: Internal communications; meetings requests
        - P3: Newsletters; marketing; FYI emails""",
        tools=["mcp__email__search_inbox", "mcp__email__read_emails", "mcp__email__label_emails"],
        model="sonnet"
    ),
    "support-agent": AgentDefinition(
        description="Customer support email handler. Use for support tickets, bug reports, and customer issues.",
        prompt="""You are a customer support email specialist. Your job is to:
        1. Identify and categorize support tickets
        2. Detect urgency based on keywords and customer type
        3. Label tickets appropriately for follow-up
        4. Summarize open issues

        Urgency Detection:
        - keywords: "urgen", "cirtical", "down", "broken", "not working", "production"
        - Enbterprise customers (check for "enterprise" label)
        - Bug reports marked P0 or P1

        Label Convention:
        - urgen: Needs immediate attention
        - enterprise: From enterprise customer
        - bug-report: Technical issue reported
        - billing: Payment/invoice related

        Search Patterns:
        - Support emails: `to:support` or `label:support`
        - Recent tickets: `to:support newer_than:1d`
        - Bug reports: `label:bug-report` or `subject:bug`

        Never archive support emails - only search, read, and label.
        """,
        tools=["mcp__email__search_inbox", "mcp__email__read_emails", "mcp__email__label_emails"],
        model="sonnet"
    ),
    "newletter-agent": AgentDefinition(
        description="Newletter management specialist. Use for newsletter organization, archival, and subscription management.",
        prompt="""You are a newsletter management specialist. Your job is to:
        1. Identify newsletter from common sources
        2. Archive old newsletters (older than 30 days by default)
        4. Report archival statistics

        Newsletter Sources to Identify:
        - techcrunch.com, morningbrew.com, hackernews.com
        - substack.com, medium.com
        - Any email with "newsletter", "digest", "weekly" in subject

        Search Patterns:
        - All newsletters: `label:newsletter`
        - Old newsletters: `label:newsletter older_than:30d`
        - By source: `from:techcrunch.com` or `from:morningbrew.com`

        Archival Rules:
        - Archive if older than threshold (default 30 days)
        - Skip if has "important" label
        - Report count of archived vs skipped

        You can only search and archive - do not label newsletters as urgen.
        """,
        tools=["mcp__email__search_inbox", "mcp__email__read_emails", "mcp__email__archive_emails"],
        model="haiku"
    )
}


@tool("search_inbox", "Searches the inbox for emails matching a query", {"query": str})
async def search_inbox(args: dict) -> dict:
    query = args["query"]
    results = search_emails(query)

    return { "content": [{"type": "text", "text": json.dumps(results, indent=2)}] }


@tool("read_emails", "Reads emails based on their IDs", {"ids": list[str]})
async def read_emails(args: dict) -> dict:
    ids = args["ids"]
    # Handle string input (LLM sometimes passes strings instead of lists)
    if isinstance(ids, str):
        ids = [id.strip() for id in ids.replace(',', ' ').split() if id.strip()]
    results = get_emails_by_ids(ids)

    return { "content": [{"type": "text", "text": json.dumps(results, indent=2)}] }


@tool("send_email", "Compose and send an email", {"to": str, "subject": str, "body": str})
async def send_email(args: dict) -> dict:
    (to, subject, body) = args["to"], args["subject"], args["body"]

    return { "content": [{"type": "text", "text": "success"}] }


@tool("archive_emails", "Archive emails by their IDs", {"ids": list[str]})
async def archive_emails(args: dict) -> dict:
    ids = args["ids"]
    # Handle string input (LLM sometimes passes strings instead of lists)
    if isinstance(ids, str):
        ids = [id.strip() for id in ids.replace(',', ' ').split() if id.strip()]

    archived = []
    failed = []
    for id in ids:
        result = archive_email(id)
        if result:
            archived.append(id)
        else:
            failed.append(id)

    if failed:
        return { "content": [{"type": "text", "text": f"Archived {len(archived)} emails. Failed to archive: {', '.join(failed)}"}] }
    return { "content": [{"type": "text", "text": f"Successfully archived {len(archived)} emails: {', '.join(archived)}"}] }


@tool("label_emails", "Add or remove labels from emails", {"ids": list[str], "add_labels": list[str], "remove_labels": list[str]})
async def label_emails(args: dict) -> dict:
    ids = args["ids"]
    add_labels_list = args.get("add_labels", [])
    remove_labels_list = args.get("remove_labels", [])

    # Handle string inputs (LLM sometimes passes strings instead of lists)
    if isinstance(ids, str):
        ids = [id.strip() for id in ids.replace(',', ' ').split() if id.strip()]
    if isinstance(add_labels_list, str):
        add_labels_list = [l.strip() for l in add_labels_list.replace(',', ' ').split() if l.strip()]
    if isinstance(remove_labels_list, str):
        remove_labels_list = [l.strip() for l in remove_labels_list.replace(',', ' ').split() if l.strip()]

    try:
        for id in ids:
            for label in add_labels_list:
                add_label(id, label)
            for label in remove_labels_list:
                remove_label(id, label)

        return { "content": [{"type": "text", "text": f"Successfully updated labels for {len(ids)} emails"}] }
    except Exception as e:
        return { "content": [{"type": "text", "text": f"failed to label emails: {e}"}] }


@tool("get_email_stats", "Get statistics about the inbox", {})
async def get_email_stats(args: dict) -> dict:
    stats = get_inbox_stats()
    return { "content": [{"type": "text", "text": json.dumps(stats, indent=2)}] }


async def log_email_operation(input_data, tool_use_id, context):
    tool_name = input_data.get("tool_name", "unknown")

    if tool_name.startswith("mcp__email__"):
        operation = tool_name.replace("mcp__email__", "")
        print(f"[EMAIL-OP] {operation}")
    elif tool_name == "Skill":
        skill_name = input_data.get("tool_input", {}).get("skill", "unknown")
        print(f"[SKILL] Invoking: {skill_name}")

    return {}


email_tools = create_sdk_mcp_server(
    name="email",
    version="1.0.0",
    tools=[search_inbox, read_emails, archive_emails, label_emails, get_email_stats, send_email]
)


async def run_agent(args):
    # Determine prompt based on CLI args (check query first since archive_newsletters has a default)
    if args.query:
        prompt = args.query
    elif args.triage:
        prompt = "Triage my inbox and identify urgent emails."
    elif args.process_all:
        prompt = """You MUST delegate to subagents for this task. Do NOT use the email tools directly.

Spawn these three subagents in parallel using the Task tool:
1. triage-agent - to identify and label urgent/priority emails
2. support-agent - to categorize customer support tickets
3. newsletter-agent - to archive newsletters older than 30 days

Use the Task tool three times to spawn all agents. After all complete, synthesize a unified summary."""
    elif args.agent:
        agent_prompts = {
            "triage": "Use the triage-agent to identify and label urgent/priority emails in my inbox.",
            "support": "Use the support-agent to categorize and summarize customer support tickets.",
            "newsletter": "Use the newsletter-agent to archive newsletters older than 30 days."
        }
        prompt = agent_prompts.get(args.agent, "Give me a summary of my inbox.")
    else:
        prompt = "Give me a summary of my inbox."

    # Conditionally enable hooks based on verbose flag
    options = ClaudeAgentOptions(
        mcp_servers={"email": email_tools},
        allowed_tools=[
            "mcp__email__search_inbox",
            "mcp__email__read_emails",
            "mcp__email__archive_emails",
            "mcp__email__label_emails",
            "mcp__email__get_email_stats",
            "mcp__email__send_email",
            "Skill",
            "Task",
        ],
        setting_sources=["project"],
        cwd=str(Path(__file__).parent),
        agents=agents,
        hooks={"PreToolUse": [HookMatcher(hooks=[log_email_operation])]} if args.verbose else {}
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"[ASSISTANT] {block.text}")

                    if isinstance(block, ToolUseBlock):
                        print(f"[TOOL] name: {block.name}, input: {block.input}")

            elif isinstance(message, ResultMessage):
                print(f"[RESULT] {message.result}")

cli = AgentCLI(
    name="Email Agent",
    description="AI-powered email management using Claude Agent SDK with Skills",
    arguments=[
        CLIArgument(name="--query", short="-q", help="Direct query to execute"),
        CLIArgument(name="--triage", short="-t", help="Run email triage workflow", action="store_true"),
        CLIArgument(name="--archive-newsletters", help="Archive newsletters older than N days", arg_type=int, default=30),
        CLIArgument(name="--verbose", short="-v", help="Show detailed tool and skill usage", action="store_true"),
        CLIArgument(name="--process-all", short="-p", help="Run comprehensive inbox processing with all subagents", action="store_true"),
        CLIArgument(name="--agent", short="-a", help="Use specific subagent", choices=["triage", "support", "newsletter"]),
    ]
)

if __name__ == "__main__":
    exit_code = run_agent_cli(cli, run_agent)
    sys.exit(exit_code)
