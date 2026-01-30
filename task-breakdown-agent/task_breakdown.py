"""
Task Breakdown Agent - Iteration 5
Demonstrates the Orchestrator-Workers pattern.

Pattern: Orchestrator dynamically decides work streams, workers generate tasks,
orchestrator synthesizes unified plan.
"""

import asyncio
import argparse
from claude_agent_sdk import AgentDefinition, ClaudeAgentOptions, ResultMessage, query
from pydantic import BaseModel

class WorkStreamPlan(BaseModel):
    goal: str
    work_streams: list[str]
    reasoning: str

WORKER_AGENTS = {
        "technical-worker": AgentDefinition(
        description="Technical implementation specialist. Use for development, architecture, and coding tasks.",
        prompt="""You are a technical task breakdown specialist.

        Given a goal and work stream context, output a markdown checklist of specific, actionable technical tasks.

        Format:
        ## Technical Tasks
        - [ ] Task description
        - [ ] Task description
        ...

        Keep tasks specific and actionable.""",
        tools=[],
        model="haiku",
    ),
    "testing-worker": AgentDefinition(
        description="Testing and QA specialist. Use for test planning, quality assurance, and validation tasks.",
        prompt="""You are a testing task breakdown specialist.

        Given a goal and work stream context, output a markdown checklist of specific testing tasks.

        Format:
        ## Testing Tasks
        - [ ] Task description
        - [ ] Task description
        ...

        Keep tasks specific and actionable.""",
        tools=[],
        model="haiku",
    ),
    "documentation-worker": AgentDefinition(
        description="Documentation specialist. Use for docs, guides and communication tasks.",
        prompt="""You are a documentation task breakdown specialist.

        Given a goal and work stream context, output a markdown checklist of documentation tasks.

        Format:
        ## Documentation Tasks
        - [ ] Task description
        - [ ] Task description
        ...

        Include user docs, API docs, and internal documentation.""",
        tools=[],
        model="haiku",
    ),
    "operations-worker": AgentDefinition(
        description="Operations and deployment specialist. Use for infrastructure, deployment, and monitoring tasks.",
        prompt="""You are an operations task breakdown specialist.

        Given a goal and work stream context, output a markdown checklist of operational tasks.

        Format:
        ## Operations Tasks
        - [ ] Task description
        - [ ] Task description
       
         Include deployment, monitoring, and infrastructure tasks.""",
        tools=[],
        model="haiku",
    )
}


WORK_STREAM_TO_WORKER = {
    "technical": "technical-worker",
    "testing": "testing-worker",
    "documentation": "documentation-worker",
    "operations": "operations-worker",
}

AVAILABLE_WORK_STREAMS = list(WORK_STREAM_TO_WORKER.keys())

async def identify_work_streams(goal: str, verbose: bool = False) -> WorkStreamPlan | None:
    if verbose:
        print(f"[ORCHESTRATOR] Analyzing goal: {goal}")

    streams_description = "\n".join([
        f"- {stream}: {WORKER_AGENTS[worker].description}"
        for stream, worker in WORK_STREAM_TO_WORKER.items()
    ])

    result = None
    async for message in query(
        prompt=f"""Analyze this goal and identify which work streams are needed to accomplish it.

Goal: {goal}

Available work streams:
{streams_description}

Choose ONLY the work streams that are relevant to this specific goal.
Not every goal needs all work streams - be selective based on what the goal actually requires.
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

    if verbose and result:
        print(f"[ORCHESTRATOR] Selected work streams: {result.work_streams}")
        print(f"[ORCHESTRATOR] Reasoning: {result.reasoning}")

    return result


async def run_worker(goal: str, work_stream: str, verbose: bool = False) -> str | None:
    worker_name = WORK_STREAM_TO_WORKER[work_stream]
    if not worker_name:
        if verbose:
            print(f"[WORKER] Unknown work stream: {work_stream}")
        return None

    if verbose:
        print(f"[WORKER] Running {worker_name} for '{work_stream}' stream...")

    result = None
    async for message in query(
        prompt=f"""Break down this goal into specific, actionable tasks for the {work_stream} work stream.

Goal: {goal}

Generate a clear markdown checklist. Be specific and practical.""",
        options=ClaudeAgentOptions(
            allowed_tools=["Task"],
            agents={worker_name: WORKER_AGENTS[worker_name]},
        )
    ):
        if isinstance(message, ResultMessage):
            result = message.result

    return result


async def run_all_workers(goal: str, work_streams: list[str], verbose: bool = False) -> dict[str, str]:
    if verbose:
        print(f"\n[ORCHESTRATOR] Dispatching {len(work_streams)} workers...")

    results = {}
    for stream in work_streams:
        output = await run_worker(goal, stream, verbose)
        if output:
            results[stream] = output
            if verbose:
                print(f"[WORKER] {stream}: Generated tasks")

        else:
            if verbose:
                print(f"[WORKER] {stream}: No output")

    return results


async def synthesize_plan(goal: str, worker_results: dict[str, str], verbose: bool = False) -> str | None:
    """
    Orchestrator Step 2: Combine worker outputs into a unified plan.

    Takes the markdown outputs from all workers and synthesizes them into
    a cohesive, ordered plan.
    """
    if verbose:
        print("\n[ORCHESTRATOR] Synthesizing unified plan...")

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
3. Groups related tasks together
4. Provides a clear execution sequence

Output a clean markdown document with the unified plan. Use checkboxes for tasks.""",
        options=ClaudeAgentOptions()
    ):
        if isinstance(message, ResultMessage):
            result = message.result

    return result


async def run_orchestrator(goal: str, verbose: bool = True) -> dict | None:
    """
    Full orchestrator-workers pipeline:
    1. Orchestrator identifies work streams
    2. Workers generate task lists
    3. Orchestrator synthesizes unified plan
    """
    if verbose:
        print("\n" + "=" * 50)
        print("TASK BREAKDOWN AGENT")
        print("=" * 50)

    # Step 1: Identify work streams
    plan = await identify_work_streams(goal, verbose=verbose)

    if not plan:
        if verbose:
            print("[ERROR] Failed to identify work streams")
        return {"success": False, "error": "Failed to identify work streams"}

    if verbose:
        print(f"\n[RESULT] Work streams: {plan.work_streams}")

    # Step 2: Run workers for each stream
    worker_results = await run_all_workers(goal, plan.work_streams, verbose=verbose)

    if not worker_results:
        if verbose:
            print("[ERROR] No worker results")
        return {"success": False, "error": "No worker results"}

    # Step 3: Synthesize unified plan
    final_plan = await synthesize_plan(goal, worker_results, verbose=verbose)

    if not final_plan:
        if verbose:
            print("[ERROR] Synthesis failed")
        return {"success": False, "error": "Synthesis failed"}

    # Display final plan
    print("\n" + "=" * 50)
    print(f"TASK BREAKDOWN: {goal}")
    print("=" * 50)
    print(final_plan)

    return {
        "success": True,
        "goal": goal,
        "work_streams": plan.work_streams,
        "plan": final_plan
    }


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Task Breakdown Agent - Break goals into actionable tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python task_breakdown.py -g "Build a REST API for user management"
  python task_breakdown.py -g "Migrate database to PostgreSQL" -v
  python task_breakdown.py -g "Create onboarding guide" -o plan.md
        """
    )
    parser.add_argument(
        "-g", "--goal",
        required=True,
        help="The goal to break down into tasks"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed orchestrator and worker output"
    )
    parser.add_argument(
        "-o", "--output",
        help="Save the plan to a markdown file"
    )

    args = parser.parse_args()

    result = asyncio.run(run_orchestrator(args.goal, verbose=args.verbose))

    if result and result.get("success"):
        if args.output:
            with open(args.output, "w") as f:
                f.write(f"# Task Breakdown: {result['goal']}\n\n")
                f.write(result["plan"])
            print(f"\nPlan saved to: {args.output}")
    else:
        error = result.get("error", "Unknown error") if result else "Pipeline failed"
        print(f"\nFailed: {error}")


if __name__ == "__main__":
    main()
