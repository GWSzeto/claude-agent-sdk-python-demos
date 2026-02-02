from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ToolUseBlock
from claude_agent_sdk.types import TextBlock

RESEARCH_SYSTEM_PROMPT = """You are a research agent specialized in  AI.

When providing research findings:
- Always include source URLs as citations
- format citations as markdown links: [Source Title](URL)
- Group sources in a "Sources:" section at the end of your response"""

options = ClaudeAgentOptions(
    cwd="research_agent",
    system_prompt=RESEARCH_SYSTEM_PROMPT,
    allowed_tools=["WebSearch", "Read"],
    max_buffer_size=10 * 1024 * 1024,
)

def print_activity(msg):
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(f"[ASSISTANT]: {block.text}")
            if isinstance(block, ToolUseBlock):
                print(f"[TOOL]: {block.name}")

async def main():
    messages = []
    async with ClaudeSDKClient(options=options) as research_agent:
        await research_agent.query("Analyze the chart in research_agent/projects_claude.png")
        async for msg in research_agent.receive_response():
            print_activity(msg)
            messages.append(msg)

        await research_agent.query(
            "Based on the chart analysis, search for recent news or data that validates or provides context for these findings. Include source URLs."
        )
        async for msg in research_agent.receive_response():
            print_activity(msg)
            messages.append(msg)

