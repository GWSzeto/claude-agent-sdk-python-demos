# Hello World - Python Implementation Iterations

## TypeScript Demo Analysis

### Key Agentic Components

The TypeScript hello-world demo demonstrates these core SDK concepts:

1. **`query()` function** - The main entry point that spawns a Claude agent subprocess and returns an async iterable of messages
2. **Configuration options** - `prompt`, `maxTurns`, `cwd`, `model`, `allowedTools`
3. **Hooks system** - `PreToolUse` hooks to intercept and validate tool calls before execution
4. **Message streaming** - Async iteration over agent messages with type filtering (`assistant`, `system`, `result`)

### Data Flow

```
User Prompt → query() → Claude Subprocess → Message Stream → Process & Display
                             ↓
                       Hook Interception
                       (PreToolUse validation)
```

---

## Iteration 1: Bare Bones Agent

**Goal**: Get a Claude agent to respond to a simple prompt using the Python SDK.

**Requirements**:
- Use the `claude-agent-sdk` Python package
- Send a single prompt: "Hello, Claude! Please introduce yourself in one sentence."
- Print Claude's text response to the console
- No configuration beyond the prompt

**Expected Output**:
```
Claude says: [A one-sentence self-introduction]
```

**Key Concepts Tested**:
- Basic SDK import and setup
- Async iteration over query results
- Extracting text content from assistant messages

---

## Iteration 2: Model and Turn Configuration

**Goal**: Add configuration options for model selection and turn limits.

**Requirements**:
- All of Iteration 1
- Configure the model to use "sonnet" (or parameterize it)
- Set `max_turns` to 10
- Set a working directory (`cwd`) for the agent

**Expected Output**:
```
Claude says: [Response from specified model]
```

**Key Concepts Tested**:
- Understanding SDK configuration options
- Working directory setup
- Model selection

---

## Iteration 3: Allowed Tools Configuration

**Goal**: Restrict which tools the agent can use.

**Requirements**:
- All of Iteration 2
- Specify an `allowed_tools` list containing: `["Read", "Write", "Bash", "Glob", "Grep"]`
- Change the prompt to ask Claude to do something that uses a tool (e.g., "List the files in the current directory")

**Expected Output**:
```
Claude says: [Description of files found, demonstrating tool usage]
```

**Key Concepts Tested**:
- Tool permission system
- Observing tool usage through the message stream

---

## Iteration 4: Message Type Handling

**Goal**: Properly handle different message types from the agent.

**Requirements**:
- All of Iteration 3
- Handle and display all three message types:
  - `system` - Log system messages
  - `assistant` - Display Claude's text responses
  - `result` - Show tool execution results
- Format output to clearly distinguish message types

**Expected Output**:
```
[SYSTEM] ...
[ASSISTANT] Claude says: ...
[RESULT] Tool: Glob, Output: ...
```

**Key Concepts Tested**:
- Message type discrimination
- Understanding the full message stream
- Structured output formatting

---

## Iteration 5: PreToolUse Hook - Basic

**Goal**: Implement a basic hook that logs all tool calls before execution.

**IMPORTANT**: Hooks are **NOT supported** with `query()`. You must switch to `ClaudeSDKClient`.

**Requirements**:
- Refactor from `query()` to `ClaudeSDKClient` (context manager pattern)
- Add a `PreToolUse` hook that:
  - Logs the tool name and input parameters
  - Returns `{}` to allow the tool to proceed
- Keep the same prompt and configuration
- Use `HookMatcher` to register the hook

**Hook Callback Signature**:
```python
async def my_hook(
    input_data: dict[str, Any],      # Contains 'tool_name' and 'tool_input'
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    # Return {} to allow, or hookSpecificOutput to block
    return {}
```

**Expected Output**:
```
[HOOK] Tool 'Bash' called with input: {'command': 'ls -la', ...}
[ASSISTANT] Claude says: I'll list all the files...
[ASSISTANT] Claude says: The directory contains...
```

**Code Structure**:
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
    tool_name = input_data.get('tool_name', 'unknown')
    tool_input = input_data.get('tool_input', {})
    print(f"[HOOK] Tool '{tool_name}' called with input: {tool_input}")
    return {}  # Allow the tool to proceed

async def main():
    options = ClaudeAgentOptions(
        model="sonnet",
        max_turns=10,
        cwd="...",
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep"],
        hooks={
            'PreToolUse': [HookMatcher(hooks=[log_tool_use])]
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("List all the files and folders in the current directory.")

        async for message in client.receive_response():
            # Handle messages...
```

**Key Concepts Tested**:
- Switching from `query()` to `ClaudeSDKClient`
- Hook registration with `HookMatcher`
- Hook callback signature (`input_data`, `tool_use_id`, `context`)
- Accessing `tool_name` and `tool_input` from `input_data`

---

## Iteration 6: PreToolUse Hook - Validation & Blocking

**Goal**: Implement the full hook logic from the TypeScript demo that validates and blocks certain tool calls.

**Requirements**:
- All of Iteration 5
- Implement a validation hook that:
  - Intercepts `Write` and `Edit` tool calls (use `matcher='Write|Edit'`)
  - Checks if the file path ends in `.js`, `.ts`, or `.py`
  - If yes, validates that the path contains `custom_scripts` directory
  - Blocks the tool with a helpful error message if validation fails
  - Allows all other tool calls to proceed

**How to Block a Tool**:
```python
return {
    'hookSpecificOutput': {
        'hookEventName': 'PreToolUse',
        'permissionDecision': 'deny',
        'permissionDecisionReason': 'Your error message here'
    }
}
```

**Expected Output (when blocked)**:
```
[HOOK] Blocking Write: Script files (.py, .js, .ts) must be written to custom_scripts directory
```

**Code Structure**:
```python
async def validate_script_writes(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})

    if tool_name in ['Write', 'Edit']:
        file_path = tool_input.get('file_path', '')

        # Check if it's a script file
        if file_path.endswith(('.py', '.js', '.ts')):
            # Validate it's in custom_scripts
            if 'custom_scripts' not in file_path:
                print(f"[HOOK] Blocking {tool_name}: Script files must be in custom_scripts directory")
                return {
                    'hookSpecificOutput': {
                        'hookEventName': 'PreToolUse',
                        'permissionDecision': 'deny',
                        'permissionDecisionReason': 'Script files (.py, .js, .ts) must be written to custom_scripts directory'
                    }
                }

    return {}  # Allow

# Register with matcher for Write|Edit
options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [
            HookMatcher(hooks=[log_tool_use]),  # Log all tools
            HookMatcher(matcher='Write|Edit', hooks=[validate_script_writes])
        ]
    }
)
```

**Key Concepts Tested**:
- Hook decision logic (allow vs block)
- Using `matcher` pattern to filter which tools trigger the hook
- Path validation logic
- Returning `hookSpecificOutput` with `permissionDecision: 'deny'`

---

## Iteration 7: Full Feature Parity (Final)

**Goal**: Match the TypeScript demo's full functionality with clean, production-ready code.

**Requirements**:
- All previous iterations combined
- Clean code organization (functions, type hints, docstrings)
- Proper error handling with try/except
- Command-line argument support for:
  - `--prompt` - Custom prompt (default: "List files in the current directory")
  - `--model` - Model selection (default: "sonnet")
  - `--verbose` - Show all message types vs just assistant
- Configurable working directory
- Graceful error handling for SDK errors

**Expected Output**:
```
$ python hello_world.py --prompt "Write a hello.py file" --model sonnet --verbose
[SYSTEM] SystemMessage(subtype='init', ...)
[HOOK] Tool 'Write' called with: {'file_path': '.../custom_scripts/hello.py', ...}
[ASSISTANT] Claude says: I'll create a hello.py file for you...
[RESULT] ResultMessage(...)
```

**Code Structure**:
```python
#!/usr/bin/env python3
"""Hello World Agent - Full implementation with hooks and CLI."""

import argparse
import asyncio
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    HookContext,
    AssistantMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    CLINotFoundError,
    ProcessError,
)


async def log_tool_use(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all tool usage before execution."""
    # ...


async def validate_script_writes(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Validate that script files are written to custom_scripts directory."""
    # ...


async def run_agent(prompt: str, model: str, verbose: bool) -> None:
    """Run the Claude agent with the given configuration."""
    # ...


def main():
    parser = argparse.ArgumentParser(description="Hello World Agent")
    parser.add_argument("--prompt", default="List files in the current directory")
    parser.add_argument("--model", default="sonnet", choices=["sonnet", "opus", "haiku"])
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    try:
        asyncio.run(run_agent(args.prompt, args.model, args.verbose))
    except CLINotFoundError:
        print("Error: Claude Code CLI not found. Install with: npm install -g @anthropic-ai/claude-code")
    except ProcessError as e:
        print(f"Error: Process failed with exit code {e.exit_code}")


if __name__ == "__main__":
    main()
```

**Key Concepts Tested**:
- Full SDK feature usage with `ClaudeSDKClient`
- Production code quality (type hints, docstrings, error handling)
- CLI design with argparse
- Error handling for SDK-specific exceptions

---

## Comparison Checklist

| Feature | TypeScript Demo | Python Implementation |
|---------|-----------------|----------------------|
| Basic query | `query({prompt})` | `query(prompt=...)` or `ClaudeSDKClient` |
| Model config | `model: "opus"` | `model="sonnet"` |
| Max turns | `maxTurns: 100` | `max_turns=10` |
| Working dir | `cwd: path.join(...)` | `cwd=str(Path(...))` |
| Allowed tools | `allowedTools: [...]` | `allowed_tools=[...]` |
| PreToolUse hook | `hooks: { PreToolUse: [...] }` | `hooks={'PreToolUse': [HookMatcher(hooks=[...])]}` |
| Hook callback | `(input, ctx) => {...}` | `async def hook(input_data, tool_use_id, context)` |
| Allow tool | `return undefined` | `return {}` |
| Block tool | `return { stopReason: "..." }` | `return {'hookSpecificOutput': {'permissionDecision': 'deny', ...}}` |
| Message iteration | `for await (const msg of q)` | `async for msg in client.receive_response():` |
| Text extraction | `content.find(c => c.type === 'text')` | `isinstance(block, TextBlock)` |

## SDK API Quick Reference

**Hooks require `ClaudeSDKClient`** - The `query()` function does NOT support hooks.

**Hook Callback Signature**:
```python
async def my_hook(
    input_data: dict[str, Any],   # Contains 'tool_name', 'tool_input', 'session_id', etc.
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]
```

**PreToolUseHookInput fields**:
- `hook_event_name`: `"PreToolUse"`
- `tool_name`: Name of the tool (e.g., "Write", "Bash")
- `tool_input`: Dict of tool input parameters
- `session_id`: Current session ID
- `cwd`: Current working directory

**Hook Return Values**:
- Allow: `return {}`
- Block: `return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': '...'}}`
