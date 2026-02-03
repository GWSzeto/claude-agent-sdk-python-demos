from claude_agent_sdk import ResultMessage, query, ClaudeAgentOptions
from typing import List
from pydantic import BaseModel
import asyncio
from pprint import pprint

class Tasks(BaseModel):
    task_agent: str
    description: str

class OrchestratorOutput(BaseModel):
    analysis: str
    tasks: List[Tasks]

class WorkerOutput(BaseModel):
    style: str
    task: str
    response: str

orchestrator_prompt = """
Analyze this task and break it down into 2-3 distinct approaches:

Task {task}

For each approach, provide the:
- analysis: An explanation of your understanding of the task and which variations would be valuable. Focus on how each approach serves different aspects of the task.

The tasks can be the following

**formal**
type: formal
description: Write a precise, technical version that emphasizes specifications

**conversational**
type: conversational
description: Write an engaging, friendly version that connects with readers
"""

worker_prompt = """
Generate content based on:
Task: {task}
Style: {task_agent}
Guidelines: {description}
"""


async def process_worker(task: str, task_info: Tasks) -> WorkerOutput:
    worker_input = worker_prompt.format(task=task, task_agent=task_info.task_agent, description=task_info.description)
    worker_response = None

    async for message in query(
        prompt=worker_input,
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": WorkerOutput.model_json_schema()}
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            worker_response = WorkerOutput.model_validate(message.structured_output)

    if not worker_response:
        raise Exception("Worker response is empty")

    return worker_response


async def process(task: str, context: dict | None = None) -> dict:
    context = context or {}

    orchestator_input = orchestrator_prompt.format(task=task, **context)
    orchestrator_response = None

    async for message in query(
        prompt=orchestator_input,
        options=ClaudeAgentOptions(
            output_format={"type": "json_schema", "schema": OrchestratorOutput.model_json_schema()}
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            orchestrator_response = OrchestratorOutput.model_validate(message.structured_output)

    analysis, tasks = orchestrator_response.analysis, orchestrator_response.tasks
    for i, task_info in enumerate(tasks):
        print(f"{i}. {task_info.task_agent.upper()}")
        print(f"{task_info.description}")

    worker_futures = [process_worker(task, task_info) for task_info in tasks]
    worker_results = await asyncio.gather(*worker_futures)

    map(lambda task: {
        "type": task.style,
        "description": task.task,
        "result": task.response,
    }, worker_results)

    pprint(worker_results)

    return {
        "analysis": analysis,
        "worker_results": worker_results,
    }

asyncio.run(process(
    task="Write a product description for a new eco-friendly water bottle",
    context={
        "target_audience": "environmentally concious millenials",
        "key_features": ["plastic-free", "insulated", "lifetime warranty"],
    },
))
