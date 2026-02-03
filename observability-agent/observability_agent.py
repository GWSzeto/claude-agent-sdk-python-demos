from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, create_sdk_mcp_server, tool
import asyncio

@tool("add", "stages the changes in the git repo", {})
async def add(args):
    return {}

git_tools = create_sdk_mcp_server(
    name="git",
    version="1.0.0",
    tools=[add],
)

options = ClaudeAgentOptions(
    mcp_servers={"git": git_tools},
    allowed_tools=["mcp__git__add"],
    disallowed_tools=["Bash", "Task", "WebSearch", "WebFetch"],
    permission_mode="acceptEdits",
)


prompt = """Analyze the CI health for facebook/react repository.

Examine the most recent runs fo the 'CI' workflow and provide:
1. Current status and what triggered the run (push, PR, schedule, etc.)
2. If failing: iedntify the specific failing jobs/tests and assess severity
3. If passing: note an\ concerning patterns (long duration, flaky history)
4. Recommend actions with priotiy (critical/high/medium/low)

Provide a concise operational summary suitable for an on-call engineer.
Do not create issues or PRs - this is a read-only analysis.
"""


messages = []
async def main():
    async with ClaudeSDKClient() as agent:
        await agent.query(prompt)

        async for message in agent.receive_response():
            print(message)
            messages.append(message)


asyncio.run(main())
