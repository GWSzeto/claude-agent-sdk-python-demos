from pathlib import Path
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, TextBlock, ToolUseBlock, create_sdk_mcp_server, tool
import asyncio
import json
from mock_data import add_label, archive_email, get_emails_by_ids, get_inbox_stats, remove_label, search_emails

@tool("search_inbox", "Searches the inbox for emails matching a query", {"query": str})
async def search_inbox(args: dict) -> dict:
    query = args["query"]
    results = search_emails(query)

    return { "content": [{"type": "text", "text": json.dumps(results, indent=2)}] }


@tool("read_emails", "Reads emails based on their IDs", {"ids": list[str]})
async def read_emails(args: dict) -> dict:
    ids = args["ids"]
    results = get_emails_by_ids(ids)

    return { "content": [{"type": "text", "text": json.dumps(results, indent=2)}] }


@tool("send_email", "Compose and send an email", {"to": str, "subject": str, "body": str})
async def send_email(args: dict) -> dict:
    (to, subject, body) = args["to"], args["subject"], args["body"]

    return { "content": [{"type": "text", "text": "success"}] }


@tool("archive_emails", "Archive emails by their IDs", {"ids": list[str]})
async def archive_emails(args: dict) -> dict:
    ids = args["ids"]

    for id in ids:
        result = archive_email(id)
        if not result:
            return { "content": [{"type": "text", "text": f"failed to archive email {id}"}] }

    return { "content": [{"type": "text", "text": "success"}] }


@tool("label_emails", "Add or remove labels from emails", {"ids": list[str], "add_labels": list[str], "remove_labels": list[str]})
async def label_emails(args: dict) -> dict:
    (ids, add_labels, remove_labels) = args["ids"], args["add_labels"], args["remove_labels"]
    
    try:
        for id in ids:
            for label in add_labels:
                add_label(id, label)
            for label in remove_labels:
                remove_label(id, label)

        return { "content": [{"type": "text", "text": "success"}] }
    except Exception as e:
        return { "content": [{"type": "text", "text": f"failed to label emails: {e}"}] }

@tool("get_email_stats", "Get statistics about the inbox", {})
async def get_email_stats(args: dict) -> dict:
    stats = get_inbox_stats()
    return { "content": [{"type": "text", "text": json.dumps(stats, indent=2)}] }


email_tools = create_sdk_mcp_server(
    name="email",
    version="1.0.0",
    tools=[search_inbox, read_emails, archive_emails, label_emails, get_email_stats, send_email]
)

options = ClaudeAgentOptions(
        mcp_servers={"email": email_tools},
        allowed_tools=[
            "mcp__email__search_inbox", 
            "mcp__email__read_emails",
            "mcp__email__archive_emails", 
            "mcp__email__label_emails", 
            "mcp__email__get_email_stats",
            "mcp__email__send_email",
            "Skill"
        ],
    setting_sources=["project"],
    cwd=str(Path(__file__).parent)
)

async def main():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Triage my inbox and identify urgent emails")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"[ASSISTANT] {block.text}")

                    if isinstance(block, ToolUseBlock):
                        print(f"[TOOL] name: {block.name}, input: {block.input}")

            elif isinstance(message, ResultMessage):
                print(f"[RESULT] {message.result}")


asyncio.run(main())

