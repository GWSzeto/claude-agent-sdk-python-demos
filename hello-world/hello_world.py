#!/usr/bin/env python3
"""Hello World Agent - Demonstrates Claude Agent SDK with hooks and CLI."""

import sys
from pathlib import Path
from typing import Any

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
)

from shared.cli import AgentCLI, CLIArgument, run_agent_cli


async def log_tool_use(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all tool usage before execution."""
    tool_name = input_data.get('tool_name', 'unknown')
    tool_input = input_data.get('tool_input', {})
    print(f"[HOOK] Tool '{tool_name}' called with input: {tool_input}")
    return {}


async def validate_script_writes(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Validate that script files are written to custom_scripts directory."""
    tool_input = input_data.get('tool_input', {})
    file_path = tool_input.get('file_path', '')

    if file_path.endswith(('.py', '.ts', '.js')):
        if 'custom_scripts' not in file_path:
            print(f"[HOOK] Blocking: {file_path} - scripts must be in custom_scripts/")
            return {
                'hookSpecificOutput': {
                    'hookEventName': 'PreToolUse',
                    'permissionDecision': 'deny',
                    'permissionDecisionReason': 'Script files (.py, .js, .ts) must be written to custom_scripts directory'
                }
            }

    return {}


async def run_agent(args) -> None:
    """Run the Claude agent with the given configuration."""
    options = ClaudeAgentOptions(
        model=args.model,
        max_turns=10,
        cwd=str(Path(__file__).parent / "agent"),
        allowed_tools=["Read", "Write", "Bash", "Glob", "Grep"],
        hooks={
            'PreToolUse': [
                HookMatcher(hooks=[log_tool_use]),
                HookMatcher(matcher='Write|Edit', hooks=[validate_script_writes])
            ]
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(args.prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"[ASSISTANT] Claude says: {block.text}")
                    elif isinstance(block, ToolUseBlock):
                        print(f"[TOOL] name: {block.name}, input: {block.input}")

            elif isinstance(message, SystemMessage):
                if args.verbose:
                    print(f"[SYSTEM] {message.subtype}: {message.data}")

            elif isinstance(message, ResultMessage):
                if args.verbose:
                    print(f"[RESULT] {message.result}")
                    print(f"[RESULT] Duration: {message.duration_ms}ms, Turns: {message.num_turns}")


# Define CLI configuration
cli = AgentCLI(
    name="Hello World Agent",
    description="Demonstrates Claude Agent SDK with hooks and CLI",
    arguments=[
        CLIArgument(
            name="--prompt",
            short="-p",
            help="The prompt to send to Claude",
            default="List all the files and folders in the current directory."
        ),
        CLIArgument(
            name="--model",
            short="-m",
            help="The Claude model to use",
            default="sonnet",
            choices=["sonnet", "opus", "haiku"]
        ),
        CLIArgument(
            name="--verbose",
            short="-v",
            help="Show all message types (System, Result)",
            action="store_true"
        ),
    ],
    epilog="""
Examples:
  python hello_world.py
  python hello_world.py --prompt "Create a hello.py in custom_scripts/"
  python hello_world.py --model haiku --verbose
"""
)


if __name__ == "__main__":
    exit_code = run_agent_cli(cli, run_agent)
    sys.exit(exit_code)
