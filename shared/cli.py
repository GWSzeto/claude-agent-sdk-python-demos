"""Shared CLI utilities for Claude Agent SDK demos.

This module provides a reusable CLI wrapper that handles:
- Argument parsing with customizable arguments
- Blanket error handling for SDK and common errors
- Consistent output formatting
- Async execution management
"""

import argparse
import asyncio
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable, Optional, List, Type

from claude_agent_sdk import CLINotFoundError, ProcessError


@dataclass
class CLIArgument:
    """Definition for a CLI argument.

    Attributes:
        name: Argument name (e.g., "name" for positional, "--verbose" for optional)
        help: Help text for the argument
        default: Default value (None for required positional args)
        action: Argument action (e.g., "store_true" for flags)
        choices: List of valid choices
        required: Whether the argument is required (for optional args)
        nargs: Number of arguments (e.g., "?" for optional positional)
        arg_type: Type to convert the argument to
    """
    name: str
    help: str
    default: Any = None
    action: Optional[str] = None
    choices: Optional[List[str]] = None
    required: bool = False
    nargs: Optional[str] = None
    arg_type: Optional[Type] = None
    short: Optional[str] = None  # Short flag (e.g., "-v" for "--verbose")


@dataclass
class AgentCLI:
    """Reusable CLI wrapper for Claude Agent SDK demos.

    Attributes:
        name: Name of the CLI tool
        description: Description shown in help
        arguments: List of CLI arguments
        epilog: Additional help text shown at the end
    """
    name: str
    description: str
    arguments: list[CLIArgument] = field(default_factory=list)
    epilog: str | None = None

    def parse_args(self, args: list[str] | None = None) -> argparse.Namespace:
        """Parse command-line arguments.

        Args:
            args: Optional list of arguments (defaults to sys.argv)

        Returns:
            Parsed arguments namespace
        """
        parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
            epilog=self.epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        for arg in self.arguments:
            kwargs: dict[str, Any] = {"help": arg.help}

            if arg.default is not None:
                kwargs["default"] = arg.default
            if arg.action is not None:
                kwargs["action"] = arg.action
            if arg.choices is not None:
                kwargs["choices"] = arg.choices
            if arg.nargs is not None:
                kwargs["nargs"] = arg.nargs
            if arg.arg_type is not None:
                kwargs["type"] = arg.arg_type

            # Handle positional vs optional arguments
            if arg.name.startswith("-"):
                if arg.required:
                    kwargs["required"] = True
                if arg.short:
                    parser.add_argument(arg.short, arg.name, **kwargs)
                else:
                    parser.add_argument(arg.name, **kwargs)
            else:
                # Positional argument
                parser.add_argument(arg.name, **kwargs)

        return parser.parse_args(args)

    def run(
        self,
        agent_func: Callable[..., Awaitable[None]],
        args: argparse.Namespace,
        show_header: bool = True
    ) -> int:
        """Run the agent function with error handling.

        Args:
            agent_func: Async function to run the agent
            args: Parsed arguments namespace
            show_header: Whether to show a header with run info

        Returns:
            Exit code (0 for success, 1 for error)
        """
        if show_header:
            self._print_header(args)

        try:
            asyncio.run(agent_func(args))
            return 0

        except CLINotFoundError:
            print("\n[ERROR] Claude Code CLI not found.")
            print("Install with: npm install -g @anthropic-ai/claude-code")
            return 1

        except ProcessError as e:
            print(f"\n[ERROR] Process failed with exit code: {e.exit_code}")
            if e.stderr:
                print(f"Details: {e.stderr}")
            return 1

        except KeyboardInterrupt:
            print("\n[CANCELLED] Interrupted by user.")
            return 130  # Standard exit code for SIGINT

        except json.JSONDecodeError as e:
            print(f"\n[ERROR] Failed to parse JSON: {e}")
            return 1

        except FileNotFoundError as e:
            print(f"\n[ERROR] File not found: {e}")
            return 1

        except PermissionError as e:
            print(f"\n[ERROR] Permission denied: {e}")
            return 1

        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {type(e).__name__}: {e}")
            return 1

    def _print_header(self, args: argparse.Namespace) -> None:
        """Print a header with run information."""
        print(f"{self.name}")
        print("-" * 50)

        # Print non-default arguments
        for key, value in vars(args).items():
            if value is not None and not key.startswith("_"):
                print(f"  {key}: {value}")

        print("-" * 50)


def run_agent_cli(
    cli: AgentCLI,
    agent_func: Callable[..., Awaitable[None]],
    args: list[str] | None = None,
    show_header: bool = True
) -> int:
    """Convenience function to parse args and run an agent.

    Args:
        cli: AgentCLI instance with configuration
        agent_func: Async function to run the agent
        args: Optional list of arguments (defaults to sys.argv)
        show_header: Whether to show a header with run info

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parsed_args = cli.parse_args(args)
    return cli.run(agent_func, parsed_args, show_header)


# Import json here for the error handling
import json
