from pathlib import Path
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock, ToolUseBlock
import asyncio

PLAN_PROMPT = """Restructure our engineering team for AI focus.

**CONTEXT (from CLAUDE.md):**
You are the Chief of Staff for TechStart Inc, a 50-person B2B SaaS startup that raised $10M Series A.
- Current engineering team: 25 people (Backend: 12, Frontend: 8, Devops: 5)
- Monthly burn rate: ~$500K, Runway: 20 months
- Senior Engineer compensation: $180K-220K + equity

1. **DO NOT use the Write tool** - Output your plan directly in your response text
2. **DO NOT save to any files** - I will handle saving the plan myself
3. **Wrap your ENTIRE plan inside `<plan> </plan>` XML tags** in your response

**Required Format**
<plan>
[Your complete resutrcturing plan here - include all sections, timelines, budgets, and recommendations]

**IMPORTANT**
- The plan content MUST appear directly in your response between the XML tags
- Do NOT use Write, Edit, or any file-saving rools
- You may research and analyze before outputting, but the final plan must in your response text
- Include: team structure, hiring recommendations, timeline, budget impact, and success metrics
- Use the company context provided above - do NOT ask clarifying questions"""


def print_activity(msg):
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(f"[ASSISTANT]: {block.text}")
            if isinstance(block, ToolUseBlock):
                print(f"[TOOL]: {block.name}")

options = ClaudeAgentOptions(
    cwd=f"{Path(__file__).parent}/chief-of-staff-agent",
    settings='{"outputStyle": "executive"}',
    setting_sources=["project"],
    allowed_tools=["Bash", "Read"],
)

messages = []
plan_content = []
write_tool_content = []
write_tool_paths = []

async def main():
    with ClaudeSDKClient() as agent:
        await agent.query(PLAN_PROMPT)
        async for msg in agent.receive_response():
            print_activity(msg)
            messages.append(msg)

asyncio.run(main())
