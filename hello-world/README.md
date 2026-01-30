# Hello World Agent

A basic introduction to the Claude Agent SDK. This agent demonstrates the fundamental concepts you need to get started.

## What It Does

Sends a simple prompt to Claude and handles the response. Includes optional file operations to show tool usage.

## Techniques Used

- **Basic SDK setup** - Using `query()` and `ClaudeSDKClient`
- **Message handling** - Processing different message types (assistant, system, result)
- **Tool configuration** - Restricting which tools the agent can use
- **Hooks** - Logging and validating tool calls with `PreToolUse` hooks
