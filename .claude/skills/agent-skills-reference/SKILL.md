---
name: agent-skills-reference
description: Reference for creating and using Agent Skills in the Claude Agent SDK. Use when implementing skills in Python agents, creating SKILL.md files, or configuring skill discovery with setting_sources.
---

# Agent Skills Reference

Agent Skills are modular, filesystem-based capabilities that extend Claude with domain-specific expertise. Skills load on-demand and eliminate repetitive guidance across conversations.

## Skill Structure

Every Skill requires a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
[Clear, step-by-step guidance for Claude to follow]

## Examples
[Concrete examples of using this Skill]
```

### Field Requirements

**name** (required):
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain "anthropic" or "claude"

**description** (required):
- Maximum 1024 characters
- Include both what the Skill does AND when Claude should use it
- Use trigger keywords that match user requests

## Skill Locations

Skills are discovered from filesystem directories:

| Location | Scope | Loaded When |
|----------|-------|-------------|
| `.claude/skills/` | Project (shared via git) | `setting_sources` includes `"project"` |
| `~/.claude/skills/` | User (personal, all projects) | `setting_sources` includes `"user"` |

## Using Skills in the SDK

### Configuration

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",  # Project with .claude/skills/
    setting_sources=["user", "project"],  # REQUIRED to load skills
    allowed_tools=["Skill", "Read", "Write", "Bash"]  # Enable Skill tool
)

async for message in query(
    prompt="Help me with this task",
    options=options
):
    print(message)
```

### Key Configuration Options

| Option | Required | Description |
|--------|----------|-------------|
| `setting_sources` | Yes | Must include `"project"` and/or `"user"` to load skills |
| `allowed_tools` | Yes | Must include `"Skill"` to enable skill invocation |
| `cwd` | No | Working directory containing `.claude/skills/` |

### Common Mistake

```python
# WRONG - Skills won't be loaded (missing setting_sources)
options = ClaudeAgentOptions(
    allowed_tools=["Skill"]
)

# CORRECT - Skills will be loaded
options = ClaudeAgentOptions(
    setting_sources=["user", "project"],  # Required!
    allowed_tools=["Skill"]
)
```

## Progressive Loading Architecture

Skills use three-level loading to minimize context usage:

| Level | When Loaded | Content |
|-------|-------------|---------|
| **1: Metadata** | Always (startup) | `name` and `description` from frontmatter (~100 tokens) |
| **2: Instructions** | When triggered | SKILL.md body content (<5k tokens) |
| **3: Resources** | As needed | Bundled files, scripts, references (unlimited) |

## Multi-File Skills

Skills can include additional resources:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Additional documentation
├── EXAMPLES.md        # Extended examples
└── scripts/
    └── helper.py      # Utility scripts
```

Reference these in SKILL.md:
```markdown
For detailed API reference, see [REFERENCE.md](REFERENCE.md).
Run the helper script: `python scripts/helper.py`
```

## Best Practices

### Writing Effective Descriptions

The description determines when Claude invokes your Skill. Include:
- What the Skill does
- When to use it (trigger keywords)
- File types or domains it handles

```yaml
# Good - specific and trigger-rich
description: Process PDF documents including text extraction, form filling, and merging. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

# Bad - too vague
description: Helps with documents.
```

### Instruction Guidelines

1. **Be specific**: Provide step-by-step workflows
2. **Include examples**: Show concrete usage patterns
3. **Reference resources**: Link to bundled files for detailed info
4. **Use code blocks**: Format commands and code clearly

## Discovering Available Skills

Ask Claude directly:

```python
async for message in query(
    prompt="What Skills are available?",
    options=ClaudeAgentOptions(
        setting_sources=["user", "project"],
        allowed_tools=["Skill"]
    )
):
    print(message)
```

## Troubleshooting

### Skills Not Found

1. **Check setting_sources**: Must be configured to load skills
2. **Verify cwd**: Must point to directory containing `.claude/skills/`
3. **Check filesystem**:
   ```bash
   ls .claude/skills/*/SKILL.md
   ls ~/.claude/skills/*/SKILL.md
   ```

### Skill Not Being Invoked

1. **Verify "Skill" in allowed_tools**
2. **Check description keywords**: Must match user request patterns
3. **Test directly**: Ask "Use the [skill-name] skill to..."

## Security Considerations

- Only use Skills from trusted sources
- Audit all bundled files before use
- Skills can invoke tools and execute code
- External URL fetching poses additional risks
