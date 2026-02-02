from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ToolUseBlock, query
import asyncio

from claude_agent_sdk.types import TextBlock

async def main():
    messages = []
    async for msg in query(
        prompt="Research the latest trends in AI agents and give me a brief summary and relevant citations links.",
        options=ClaudeAgentOptions(allowed_tools=["WebSearch"]),
    ):
        if isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, TextBlock):
                    print(f"[ASSISTANT]: {block.text}")
                if isinstance(block, ToolUseBlock):
                    print(f"[TOOL]: {block.name}")
        messages.append(msg)

asyncio.run(main())
