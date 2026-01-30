# Claude Agent SDK Examples (Python)

A recreation of the Claude Agent SDK demos built from Anthropic, but in Python.

It utilizes the patterns mentioned from the [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) article, so it's not a 1:1 recreation.

This repo was made purely for educational purposes in order to get more practice building with the `claude-agent-sdk` along with applying the patterns mentioned from the article.

Each of the Agents include an `iteration.md` file that can be fed into claude code so that it can give you instructions on how to build each of the agents from the ground up.

## What's Inside

| Agent | What It Does | Pattern Used |
|-------|--------------|--------------|
| `hello-world` | Basic setup | Getting started |
| `email-agent` | Sort and write emails | Routing, Tools |
| `excel-agent` | Edit spreadsheets | Evaluator-Optimizer |
| `resume-generator` | Create resumes from web info | Tools |
| `content-pipeline-agent` | Pull out and summarize content | Prompt Chaining |
| `task-breakdown-agent` | Turn goals into task lists | Orchestrator-Workers |

## How to Use

1. Copy the contents from `base-prompt.txt` and pass that into claude-code
2. Pick an agent folder
3. Deed in the `iteration.md` file into claude-code
4. Follow the instructions given from claude-code

## Setup

```bash
git clone <repository-url>
cd claude-agent-python

python -m venv venv
source venv/bin/activate

pip install claude-agent-sdk pydantic
```

You need Python 3.11 or newer and an Anthropic API key.

## Folder Layout

```
claude-agent-python/
├── hello-world/              # Start here
├── email-agent/
├── excel-agent/
├── resume-generator/
├── content-pipeline-agent/
├── task-breakdown-agent/
└── .claude/skills/           # Helper docs for Claude
```

## Skills

A few supporting skills were created in `.claude/skills/` to help guide how the agents should be created:

- `building-effective-agents` — Patterns from Anthropic's article
- `structured-outputs-reference` — Get typed JSON responses
- `subagents-sdk-reference` — Use worker agents
- `agent-skills-reference` — Make custom skills

## Links

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Claude Agent SDK Docs](https://docs.anthropic.com/en/docs/claude-code/sdk)
- [Agent SDK Reference - Python](https://platform.claude.com/docs/en/agent-sdk/python)
- [Structured Outputs from Agents](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)
- [Subagents in the SDK](https://platform.claude.com/docs/en/agent-sdk/subagents)
- [Agent Skills in the SDK](https://platform.claude.com/docs/en/agent-sdk/skills)
