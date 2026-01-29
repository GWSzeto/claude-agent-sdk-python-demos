# Task Breakdown Agent - Orchestrator-Workers Pattern

## Pattern Overview

**Orchestrator-Workers** uses a central LLM to dynamically break down tasks, delegate to worker agents, and synthesize results. This pattern excels when:
- Subtasks aren't predefined but determined by context
- Workers can execute independently (potentially in parallel)
- Results need synthesis into a cohesive output

```
                    ┌→ Worker A ─┐
Input → Orchestrator┼→ Worker B ─┼→ Orchestrator → Output
                    └→ Worker C ─┘
```

**Key difference from Parallelization**: Subtasks are dynamically determined by the orchestrator, not hardcoded.

## Agent Concept

The **Task Breakdown Agent** takes a goal and breaks it into actionable tasks across multiple work streams:

```
Goal: "Launch a new feature"
              ↓
      ┌───────────────┐
      │  Orchestrator │  ← Decides work streams based on goal
      └───────┬───────┘
              │
    ┌─────────┼─────────┐
    ↓         ↓         ↓
┌────────┐ ┌────────┐ ┌────────┐
│Technical│ │Testing │ │  Docs  │  ← Workers output markdown
└────────┘ └────────┘ └────────┘
    │         │         │
    └─────────┼─────────┘
              ↓
      ┌───────────────┐
      │  Orchestrator │  ← Synthesizes unified plan
      └───────────────┘
```

**Simplification**: Workers output plain markdown strings—no complex structured data.

---

## Iteration 1: Project Setup with Worker Definitions

**Goal**: Set up project structure and define worker subagents.

### Project Structure

```
task-breakdown-agent/
├── task_breakdown.py   # Main orchestrator + workers
├── iteration.md        # This file
└── pyproject.toml      # Dependencies
```

### Worker Subagent Definitions

Define workers using `AgentDefinition`. Each worker specializes in one type of work stream:

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

# Worker definitions - each outputs markdown task lists
WORKER_AGENTS = {
    "technical-worker": AgentDefinition(
        description="Technical implementation specialist. Use for development, architecture, and coding tasks.",
        prompt="""You are a technical task breakdown specialist.

Given a goal and work stream, output a markdown list of specific, actionable technical tasks.

Format your output as:
## Technical Tasks
- [ ] Task 1 description
- [ ] Task 2 description
...

Keep tasks specific and actionable. Include implementation details where helpful.""",
        tools=[],  # No tools needed - just generates text
        model="haiku"  # Fast model for simple output
    ),

    "testing-worker": AgentDefinition(
        description="Testing and QA specialist. Use for test planning, quality assurance, and validation tasks.",
        prompt="""You are a testing task breakdown specialist.

Given a goal and work stream, output a markdown list of specific testing tasks.

Format your output as:
## Testing Tasks
- [ ] Task 1 description
- [ ] Task 2 description
...

Include unit tests, integration tests, and validation steps.""",
        tools=[],
        model="haiku"
    ),

    "documentation-worker": AgentDefinition(
        description="Documentation specialist. Use for docs, guides, and communication tasks.",
        prompt="""You are a documentation task breakdown specialist.

Given a goal and work stream, output a markdown list of documentation tasks.

Format your output as:
## Documentation Tasks
- [ ] Task 1 description
- [ ] Task 2 description
...

Include user docs, API docs, and internal documentation.""",
        tools=[],
        model="haiku"
    ),

    "operations-worker": AgentDefinition(
        description="Operations and deployment specialist. Use for infrastructure, deployment, and monitoring tasks.",
        prompt="""You are an operations task breakdown specialist.

Given a goal and work stream, output a markdown list of operational tasks.

Format your output as:
## Operations Tasks
- [ ] Task 1 description
- [ ] Task 2 description
...

Include deployment, monitoring, and infrastructure tasks.""",
        tools=[],
        model="haiku"
    )
}
```

### Key Concepts

| Concept | Implementation |
|---------|----------------|
| **Worker Definition** | `AgentDefinition(description, prompt, tools, model)` |
| **No tools** | Workers just generate text, no file access needed |
| **Fast model** | Use `haiku` for simple markdown output |
| **Clear prompts** | Each worker knows exactly what format to output |

---

## Iteration 2: Orchestrator Identifies Work Streams

**Goal**: Create the orchestrator that dynamically decides which work streams apply to a goal.

### Pydantic Model for Work Streams

```python
from pydantic import BaseModel

class WorkStreamPlan(BaseModel):
    """Orchestrator's decision on which work streams to pursue."""
    goal: str
    work_streams: list[str]  # e.g., ["technical", "testing", "documentation"]
    reasoning: str  # Why these work streams were chosen
```

### Orchestrator Step 1: Analyze Goal

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async def identify_work_streams(goal: str) -> WorkStreamPlan | None:
    """Orchestrator analyzes goal and decides which work streams apply."""

    result = None
    async for message in query(
        prompt=f"""Analyze this goal and identify which work streams are needed to accomplish it.

Goal: {goal}

Available work streams:
- technical: Development, architecture, coding tasks
- testing: Test planning, QA, validation
- documentation: User docs, API docs, guides
- operations: Deployment, infrastructure, monitoring

Choose only the work streams that are relevant to this specific goal.
Explain your reasoning briefly.""",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": WorkStreamPlan.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            result = WorkStreamPlan.model_validate(message.structured_output)

    return result
```

### Key Concepts

| Concept | Implementation |
|---------|----------------|
| **Dynamic decisions** | Orchestrator chooses work streams based on goal context |
| **Structured output** | Use Pydantic to get validated work stream list |
| **Reasoning** | Orchestrator explains why it chose each work stream |

---

## Iteration 3: Workers Generate Task Lists

**Goal**: Spawn workers to generate markdown task lists for each work stream.

### Dispatching to Workers

```python
async def run_worker(goal: str, work_stream: str) -> str | None:
    """Spawn a worker to generate tasks for a specific work stream."""

    worker_map = {
        "technical": "technical-worker",
        "testing": "testing-worker",
        "documentation": "documentation-worker",
        "operations": "operations-worker"
    }

    worker_name = worker_map.get(work_stream)
    if not worker_name:
        return None

    result = None
    async for message in query(
        prompt=f"""Break down this goal into specific tasks for the {work_stream} work stream.

Goal: {goal}

Generate a clear, actionable task list in markdown format.""",
        options=ClaudeAgentOptions(
            allowed_tools=["Task"],
            agents=WORKER_AGENTS
        )
    ):
        if isinstance(message, ResultMessage):
            result = message.result

    return result
```

### Running Workers (Sequential)

```python
async def run_all_workers(goal: str, work_streams: list[str]) -> dict[str, str]:
    """Run workers for each work stream and collect results."""

    results = {}
    for stream in work_streams:
        print(f"[WORKER] Processing: {stream}")
        output = await run_worker(goal, stream)
        if output:
            results[stream] = output

    return results
```

### Key Concepts

| Concept | Implementation |
|---------|----------------|
| **Worker dispatch** | Map work stream names to worker agents |
| **Simple output** | Workers return markdown strings |
| **Collect results** | Gather all worker outputs for synthesis |

---

## Iteration 4: Orchestrator Synthesizes Plan

**Goal**: Combine worker outputs into a unified, cohesive plan.

### Synthesis Step

```python
async def synthesize_plan(goal: str, worker_results: dict[str, str]) -> str | None:
    """Orchestrator combines worker outputs into a unified plan."""

    # Format worker results for the prompt
    results_text = "\n\n".join([
        f"### {stream.title()} Work Stream\n{tasks}"
        for stream, tasks in worker_results.items()
    ])

    result = None
    async for message in query(
        prompt=f"""Synthesize these work stream task lists into a unified project plan.

Goal: {goal}

Work Stream Results:
{results_text}

Create a cohesive plan that:
1. Orders tasks logically (dependencies first)
2. Identifies any cross-stream dependencies
3. Provides a clear execution sequence

Output a clean markdown document with the unified plan.""",
        options=ClaudeAgentOptions()
    ):
        if isinstance(message, ResultMessage):
            result = message.result

    return result
```

### Complete Pipeline

```python
async def breakdown_goal(goal: str) -> dict:
    """Full orchestrator-workers pipeline."""

    print(f"\n[ORCHESTRATOR] Analyzing goal: {goal}")

    # Step 1: Identify work streams
    plan = await identify_work_streams(goal)
    if not plan:
        return {"success": False, "error": "Failed to identify work streams"}

    print(f"[ORCHESTRATOR] Work streams: {plan.work_streams}")
    print(f"[ORCHESTRATOR] Reasoning: {plan.reasoning}")

    # Step 2: Run workers
    print("\n[ORCHESTRATOR] Dispatching workers...")
    worker_results = await run_all_workers(goal, plan.work_streams)

    if not worker_results:
        return {"success": False, "error": "No worker results"}

    # Step 3: Synthesize
    print("\n[ORCHESTRATOR] Synthesizing plan...")
    final_plan = await synthesize_plan(goal, worker_results)

    if not final_plan:
        return {"success": False, "error": "Synthesis failed"}

    return {
        "success": True,
        "goal": goal,
        "work_streams": plan.work_streams,
        "plan": final_plan
    }
```

### Key Concepts

| Concept | Implementation |
|---------|----------------|
| **Synthesis** | Orchestrator combines all worker outputs |
| **Ordering** | Final plan has logical task sequence |
| **Dependencies** | Cross-stream dependencies identified |

---

## Iteration 5: CLI Interface

**Goal**: Add command-line interface for easy usage.

### CLI with argparse

```python
import argparse
import asyncio

def main():
    parser = argparse.ArgumentParser(
        description="Task Breakdown Agent - Break goals into actionable tasks"
    )
    parser.add_argument(
        "-g", "--goal",
        required=True,
        help="The goal to break down into tasks"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed orchestrator output"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save plan to file (markdown)"
    )

    args = parser.parse_args()

    result = asyncio.run(breakdown_goal(args.goal, verbose=args.verbose))

    if result["success"]:
        print("\n" + "=" * 50)
        print("TASK BREAKDOWN PLAN")
        print("=" * 50)
        print(result["plan"])

        if args.output:
            with open(args.output, "w") as f:
                f.write(result["plan"])
            print(f"\nPlan saved to: {args.output}")
    else:
        print(f"Failed: {result['error']}")

if __name__ == "__main__":
    main()
```

### Usage Examples

```bash
# Basic usage
python task_breakdown.py -g "Launch a user authentication feature"

# With verbose output
python task_breakdown.py -g "Migrate database to PostgreSQL" -v

# Save to file
python task_breakdown.py -g "Build REST API for orders" -o plan.md
```

---

## Pattern Summary

| Component | Role |
|-----------|------|
| **Orchestrator (Step 1)** | Analyzes goal, decides work streams |
| **Workers** | Generate markdown tasks for each stream |
| **Orchestrator (Step 2)** | Synthesizes unified plan |

## Key Differences from Prompt Chaining

| Prompt Chaining | Orchestrator-Workers |
|-----------------|---------------------|
| Fixed sequence of steps | Dynamic subtask determination |
| Same LLM handles all steps | Specialized workers for each subtask |
| Linear flow | Fan-out and fan-in pattern |
| Predictable steps | Context-dependent delegation |

## Worker Design Principles

1. **Single responsibility**: Each worker handles one work stream type
2. **Simple output**: Markdown strings, not complex structures
3. **Fast execution**: Use `haiku` model for quick generation
4. **No tools needed**: Workers just generate text
5. **Clear prompts**: Explicit output format in each worker's prompt
