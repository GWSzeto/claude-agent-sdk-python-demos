from claude_agent_sdk import AgentDefinition
from pydantic import BaseModel
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition, ResultMessage, query

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

import asyncio


async def run_orchestrator(goal: str, verbose: bool = True):
    """Test the orchestrator's work stream identification."""
    print("\n" + "=" * 50)
    print("TASK BREAKDOWN AGENT - Iteration 2")
    print("=" * 50)

    plan = await identify_work_streams(goal, verbose=verbose)

    if plan:
        print(f"\n[RESULT] Goal: {plan.goal}")
        print(f"[RESULT] Work streams: {plan.work_streams}")
        print(f"[RESULT] Reasoning: {plan.reasoning}")
        return plan
    else:
        print("[ERROR] Failed to identify work streams")
        return None


def main():
    import sys
    goal = sys.argv[1] if len(sys.argv) > 1 else "Build a REST API for user management"
    asyncio.run(run_orchestrator(goal))


if __name__ == "__main__":
    main()
