---
name: subagents-sdk-reference
description: Reference for creating and using subagents in the Claude Agent SDK. Use when implementing subagents in Python agents, defining AgentDefinition, configuring tool restrictions, or running parallel tasks.
---

# Subagents in the Claude Agent SDK

Subagents are separate agent instances that your main agent can spawn to handle focused subtasks. Use subagents to isolate context, run tasks in parallel, and apply specialized instructions without bloating the main agent's prompt.

## Benefits

| Benefit | Description |
|---------|-------------|
| **Context Isolation** | Subagents maintain separate context, preventing information overload |
| **Parallelization** | Multiple subagents can run concurrently for faster workflows |
| **Specialized Instructions** | Each subagent can have tailored prompts with specific expertise |
| **Tool Restrictions** | Subagents can be limited to specific tools for safety |

## Creating Subagents

Define subagents using the `agents` parameter in `ClaudeAgentOptions`:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    # Task tool is REQUIRED for subagent invocation
    allowed_tools=["Read", "Grep", "Glob", "Task"],
    agents={
        "code-reviewer": AgentDefinition(
            # description: tells Claude when to use this subagent
            description="Expert code review specialist. Use for quality, security, and maintainability reviews.",
            # prompt: defines the subagent's behavior and expertise
            prompt="""You are a code review specialist with expertise in security, performance, and best practices.

When reviewing code:
- Identify security vulnerabilities
- Check for performance issues
- Verify adherence to coding standards
- Suggest specific improvements

Be thorough but concise in your feedback.""",
            # tools: restricts what the subagent can do
            tools=["Read", "Grep", "Glob"],
            # model: override the default model (optional)
            model="sonnet"
        ),
        "test-runner": AgentDefinition(
            description="Runs and analyzes test suites. Use for test execution and coverage analysis.",
            prompt="""You are a test execution specialist. Run tests and provide clear analysis of results.""",
            tools=["Bash", "Read", "Grep"]
        )
    }
)

async for message in query(prompt="Review the authentication module", options=options):
    if hasattr(message, "result"):
        print(message.result)
```

## AgentDefinition Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | `str` | Yes | Natural language description of when to use this agent |
| `prompt` | `str` | Yes | The agent's system prompt defining its role and behavior |
| `tools` | `list[str]` | No | Allowed tool names. If omitted, inherits all tools |
| `model` | `"sonnet" \| "opus" \| "haiku" \| "inherit"` | No | Model override. Defaults to main model |

**Important**: Subagents cannot spawn their own subagents. Don't include `Task` in a subagent's `tools` array.

## Invoking Subagents

### Automatic Invocation

Claude automatically decides when to invoke subagents based on the task and each subagent's `description`. Write clear, specific descriptions so Claude can match tasks appropriately.

### Explicit Invocation

To guarantee Claude uses a specific subagent, mention it by name:

```python
prompt = "Use the code-reviewer agent to check the authentication module"
```

## Dynamic Agent Configuration

Create agent definitions dynamically based on runtime conditions:

```python
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        # Use more capable model for high-stakes reviews
        model="opus" if is_strict else "sonnet"
    )

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Task"],
    agents={
        "security-reviewer": create_security_agent("strict")
    }
)
```

## Detecting Subagent Invocation

Subagents are invoked via the Task tool. Check for `tool_use` blocks with `name: "Task"`:

```python
async for message in query(prompt="Use the code-reviewer agent", options=options):
    # Check for subagent invocation
    if hasattr(message, 'content') and message.content:
        for block in message.content:
            if getattr(block, 'type', None) == 'tool_use' and block.name == 'Task':
                print(f"Subagent invoked: {block.input.get('subagent_type')}")

    # Check if message is from within a subagent's context
    if hasattr(message, 'parent_tool_use_id') and message.parent_tool_use_id:
        print("  (running inside subagent)")

    if hasattr(message, "result"):
        print(message.result)
```

## Resuming Subagents

Resumed subagents retain their full conversation history. To resume:

1. Capture `session_id` from messages during the first query
2. Extract `agentId` from message content
3. Pass `resume=session_id` in the second query's options

```python
import re
import json

def extract_agent_id(text: str) -> str | None:
    """Extract agentId from Task tool result text."""
    match = re.search(r"agentId:\s*([a-f0-9-]+)", text)
    return match.group(1) if match else None

async def main():
    agent_id = None
    session_id = None

    # First invocation
    async for message in query(
        prompt="Use the Explore agent to find all API endpoints",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Grep", "Glob", "Task"])
    ):
        if hasattr(message, "session_id"):
            session_id = message.session_id
        if hasattr(message, "content"):
            content_str = json.dumps(message.content, default=str)
            extracted = extract_agent_id(content_str)
            if extracted:
                agent_id = extracted
        if hasattr(message, "result"):
            print(message.result)

    # Second invocation - resume and ask follow-up
    if agent_id and session_id:
        async for message in query(
            prompt=f"Resume agent {agent_id} and list the top 3 most complex endpoints",
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Grep", "Glob", "Task"],
                resume=session_id
            )
        ):
            if hasattr(message, "result"):
                print(message.result)
```

## Tool Restrictions

Control what tools subagents can access:

- **Omit `tools` field**: agent inherits all available tools
- **Specify tools**: agent can only use listed tools

### Common Tool Combinations

| Use Case | Tools | Description |
|----------|-------|-------------|
| Read-only analysis | `Read`, `Grep`, `Glob` | Examine code without modifying |
| Test execution | `Bash`, `Read`, `Grep` | Run commands and analyze output |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` | Full read/write, no command execution |
| Full access | (omit field) | Inherits all tools from parent |

## Built-in Subagent

Without defining custom subagents, Claude can spawn the built-in `general-purpose` subagent when `Task` is in `allowed_tools`. Useful for delegating research or exploration tasks.

## Troubleshooting

### Claude Not Delegating to Subagents

1. **Include the Task tool**: must be in `allowed_tools`
2. **Use explicit prompting**: mention subagent by name in prompt
3. **Write clear description**: explain exactly when the subagent should be used

### Subagent Not Using Expected Tools

Verify the `tools` list in `AgentDefinition` includes the needed tools. Remember that if `tools` is omitted, the subagent inherits all parent tools.

## Example: Parallel Code Review

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Task"],
    agents={
        "style-checker": AgentDefinition(
            description="Code style and formatting reviewer",
            prompt="Check code style, naming conventions, and formatting.",
            tools=["Read", "Grep", "Glob"],
            model="haiku"  # Fast model for simple checks
        ),
        "security-scanner": AgentDefinition(
            description="Security vulnerability scanner",
            prompt="Identify security vulnerabilities and suggest fixes.",
            tools=["Read", "Grep", "Glob"],
            model="sonnet"
        ),
        "test-coverage": AgentDefinition(
            description="Test coverage analyzer",
            prompt="Analyze test coverage and identify untested code paths.",
            tools=["Bash", "Read", "Grep"]
        )
    }
)

# Claude can run these in parallel for faster reviews
async for message in query(
    prompt="Run all review agents on the authentication module",
    options=options
):
    if hasattr(message, "result"):
        print(message.result)
```
