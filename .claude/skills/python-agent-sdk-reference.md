# Python Agent SDK Reference

This skill provides the complete API reference for the Python Claude Agent SDK.

## Installation

```bash
pip install claude-agent-sdk
```

## Choosing Between `query()` and `ClaudeSDKClient`

| Feature             | `query()`                     | `ClaudeSDKClient`                  |
| :------------------ | :---------------------------- | :--------------------------------- |
| **Session**         | Creates new session each time | Reuses same session                |
| **Conversation**    | Single exchange               | Multiple exchanges in same context |
| **Streaming Input** | Supported                     | Supported                          |
| **Interrupts**      | Not supported                 | Supported                          |
| **Hooks**           | Not supported                 | Supported                          |
| **Custom Tools**    | Not supported                 | Supported                          |
| **Continue Chat**   | New session each time         | Maintains conversation             |

## Core Functions

### `query()`

Creates a new session for each interaction. Returns an async iterator of messages.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None
) -> AsyncIterator[Message]
```

**Example:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
import asyncio

async def main():
    options = ClaudeAgentOptions(
        model="sonnet",
        max_turns=10,
        cwd="/path/to/project",
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep"]
    )

    async for message in query(prompt="Hello", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

asyncio.run(main())
```

### `ClaudeSDKClient`

Maintains a conversation session across multiple exchanges. **Required for hooks and custom tools.**

```python
class ClaudeSDKClient:
    def __init__(self, options: ClaudeAgentOptions | None = None)
    async def connect(self, prompt: str | AsyncIterable[dict] | None = None) -> None
    async def query(self, prompt: str | AsyncIterable[dict], session_id: str = "default") -> None
    async def receive_messages(self) -> AsyncIterator[Message]
    async def receive_response(self) -> AsyncIterator[Message]
    async def interrupt(self) -> None
    async def disconnect(self) -> None
```

**Example with context manager:**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(
        model="sonnet",
        allowed_tools=["Read", "Write", "Bash"]
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("What files are in this directory?")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)

asyncio.run(main())
```

## ClaudeAgentOptions

Configuration dataclass for Claude Code queries.

```python
@dataclass
class ClaudeAgentOptions:
    tools: list[str] | ToolsPreset | None = None
    allowed_tools: list[str] = field(default_factory=list)
    system_prompt: str | SystemPromptPreset | None = None
    mcp_servers: dict[str, McpServerConfig] | str | Path = field(default_factory=dict)
    permission_mode: PermissionMode | None = None
    max_turns: int | None = None
    model: str | None = None
    cwd: str | Path | None = None
    can_use_tool: CanUseTool | None = None
    hooks: dict[HookEvent, list[HookMatcher]] | None = None
    # ... additional options
```

**Key Properties:**

| Property | Type | Description |
|:---------|:-----|:------------|
| `allowed_tools` | `list[str]` | List of allowed tool names |
| `model` | `str \| None` | Claude model to use (e.g., "sonnet", "opus", "haiku") |
| `max_turns` | `int \| None` | Maximum conversation turns |
| `cwd` | `str \| Path \| None` | Current working directory |
| `permission_mode` | `PermissionMode \| None` | Permission mode for tool usage |
| `hooks` | `dict[HookEvent, list[HookMatcher]] \| None` | Hook configurations (ClaudeSDKClient only) |
| `can_use_tool` | `CanUseTool \| None` | Tool permission callback function |

## Message Types

### Message Union
```python
Message = UserMessage | AssistantMessage | SystemMessage | ResultMessage | StreamEvent
```

### AssistantMessage
```python
@dataclass
class AssistantMessage:
    content: list[ContentBlock]
    model: str
```

### SystemMessage
```python
@dataclass
class SystemMessage:
    subtype: str
    data: dict[str, Any]
```

### ResultMessage
```python
@dataclass
class ResultMessage:
    subtype: str
    duration_ms: int
    is_error: bool
    num_turns: int
    session_id: str
    total_cost_usd: float | None = None
    result: str | None = None
```

## Content Block Types

```python
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock
```

### TextBlock
```python
@dataclass
class TextBlock:
    text: str
```

### ToolUseBlock
```python
@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]
```

### ToolResultBlock
```python
@dataclass
class ToolResultBlock:
    tool_use_id: str
    content: str | list[dict[str, Any]] | None = None
    is_error: bool | None = None
```

## Hooks (ClaudeSDKClient Only)

**IMPORTANT:** Hooks are NOT supported with `query()`. You must use `ClaudeSDKClient`.

### Hook Events
```python
HookEvent = Literal[
    "PreToolUse",       # Called before tool execution
    "PostToolUse",      # Called after tool execution
    "UserPromptSubmit", # Called when user submits a prompt
    "Stop",             # Called when stopping execution
    "SubagentStop",     # Called when a subagent stops
    "PreCompact"        # Called before message compaction
]
```

### HookMatcher
```python
@dataclass
class HookMatcher:
    matcher: str | None = None        # Tool name or pattern (e.g., "Bash", "Write|Edit")
    hooks: list[HookCallback] = field(default_factory=list)
    timeout: float | None = None      # Timeout in seconds (default: 60)
```

### HookCallback Signature
```python
HookCallback = Callable[
    [dict[str, Any], str | None, HookContext],
    Awaitable[dict[str, Any]]
]
```

Parameters:
- `input_data`: Hook-specific input data containing `tool_name`, `tool_input`, etc.
- `tool_use_id`: Optional tool use identifier
- `context`: HookContext with additional information

### PreToolUseHookInput
```python
class PreToolUseHookInput(BaseHookInput):
    hook_event_name: Literal["PreToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
```

### Hook Return Values

To **allow** the tool:
```python
return {}  # Empty dict allows the tool to proceed
```

To **block** the tool:
```python
return {
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': 'Reason for blocking'
    }
}
```

### Complete Hook Example
```python
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    HookContext,
    AssistantMessage,
    TextBlock
)
from typing import Any

async def log_tool_use(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all tool usage before execution."""
    tool_name = input_data.get('tool_name', 'unknown')
    tool_input = input_data.get('tool_input', {})
    print(f"[HOOK] Tool '{tool_name}' called with input: {tool_input}")
    return {}  # Allow the tool to proceed

async def validate_file_writes(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Block writes to certain directories."""
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    if tool_name in ['Write', 'Edit']:
        file_path = tool_input.get('file_path', '')
        if file_path.startswith('/system/'):
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': 'Cannot write to /system/ directory'
                }
            }
    return {}

async def main():
    options = ClaudeAgentOptions(
        model="sonnet",
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep"],
        hooks={
            'PreToolUse': [
                HookMatcher(hooks=[log_tool_use]),  # Applies to all tools
                HookMatcher(matcher='Write|Edit', hooks=[validate_file_writes])
            ]
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("List files in current directory")

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

asyncio.run(main())
```

## Permission Callback (Alternative to Hooks)

For simpler permission control, use `can_use_tool` instead of hooks:

```python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

async def custom_permission_handler(
    tool_name: str,
    input_data: dict,
    context: dict
) -> PermissionResultAllow | PermissionResultDeny:
    """Custom logic for tool permissions."""

    if tool_name == "Write" and input_data.get("file_path", "").startswith("/system/"):
        return PermissionResultDeny(
            message="System directory write not allowed",
            interrupt=True
        )

    return PermissionResultAllow(updated_input=input_data)

options = ClaudeAgentOptions(
    can_use_tool=custom_permission_handler,
    allowed_tools=["Read", "Write", "Edit"]
)
```

## Custom MCP Tools

### Define Tools with @tool Decorator
```python
from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any

@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{
            "type": "text",
            "text": f"Hello, {args['name']}!"
        }]
    }

# Create MCP server
my_server = create_sdk_mcp_server(
    name="my_tools",
    version="1.0.0",
    tools=[greet]
)

# Use with Claude
options = ClaudeAgentOptions(
    mcp_servers={"tools": my_server},
    allowed_tools=["mcp__tools__greet"]
)
```

## Error Handling

```python
from claude_agent_sdk import (
    query,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError
)

try:
    async for message in query(prompt="Hello"):
        print(message)
except CLINotFoundError:
    print("Please install Claude Code: npm install -g @anthropic-ai/claude-code")
except ProcessError as e:
    print(f"Process failed with exit code: {e.exit_code}")
except CLIJSONDecodeError as e:
    print(f"Failed to parse response: {e}")
```

## Built-in Tools Reference

Common tools available:
- `Read` - Read file contents
- `Write` - Write/create files
- `Edit` - Edit existing files
- `Bash` - Execute shell commands
- `Glob` - Find files by pattern
- `Grep` - Search file contents
- `WebSearch` - Search the web
- `WebFetch` - Fetch web content
- `Task` - Spawn subagents
