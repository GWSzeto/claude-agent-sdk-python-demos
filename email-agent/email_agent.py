from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, TextBlock, ToolUseBlock, create_sdk_mcp_server, tool
import asyncio
import json
from mock_data import get_emails_by_ids, search_emails

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

email_tools = create_sdk_mcp_server(
    name="email",
    version="1.0.0",
    tools=[search_inbox, read_emails]
)

options = ClaudeAgentOptions(
        mcp_servers={"email": email_tools},
        allowed_tools=["mcp__email__search_inbox", "mcp__email__read_emails"],
)

async def main():
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Search for all unread emails")

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

