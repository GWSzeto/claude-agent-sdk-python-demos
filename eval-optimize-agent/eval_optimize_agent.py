from claude_agent_sdk import ResultMessage, query, ClaudeAgentOptions
from pydantic import BaseModel
from typing import Literal
import asyncio

class GenerateModel(BaseModel):
    thoughts: str
    result: str

class EvalModel(BaseModel):
    eval: Literal["PASS"] | Literal["FAIL"]
    feedback: str

async def generate(prompt: str, task: str, context: str = "") -> GenerateModel:
    full_prompt = f"{prompt}\n{context}\nTask: {task}" if context else f"{prompt}\nTask: {task}"
    result = None

    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": GenerateModel.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            result = GenerateModel.model_validate(message.structured_output)
            print(f"[GENERATE] thoughts: {result.thoughts}")
            print()
            print(f"[GENERATE] result: {result.result}")
    
    if not result:
        raise Exception("Failed to generate gen result")

    return result

async def evaluate(prompt: str, content: str, task: str) -> EvalModel:
    full_prompt = f"{prompt}\nOriginal task: {task}\nContent to evaluate: {content}"
    result = None

    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": EvalModel.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            result = EvalModel.model_validate(message.structured_output)
            print(f"[GENERATE] eval: {result.eval}")
            print()
            print(f"[GENERATE] feedback: {result.feedback}")

    if not result:
        raise Exception("Failed to generate eval result")

    return result


async def main(task: str, evaluator_prompt: str, generator_prompt: str):
    memory = []
    chain_of_thought = []
    context = ""
    eval = "FAIL"
    result = ""

    while eval == "FAIL":
        generate_result = await generate(generator_prompt, task, context)
        thoughts, result = generate_result.thoughts, generate_result.result

        memory.append(result)
        chain_of_thought.append({"thoughts": thoughts, "result": result})

        eval_result = await evaluate(evaluator_prompt, result, task)
        eval, feedback = eval_result.eval, eval_result.feedback

        context = "\n".join(
            ["Previous attempts:", *[f"- {m}" for m in memory], f"\nFeedback; {feedback}"]
        )

    return result, chain_of_thought


evaluator_prompt = """
Evaluate this following code implementation for:
1. code corerctness
2. time complexity
3. style and best practices

Based on your judgement of the code based on the criteria that was given, you are to give either a "PASS" or a "FAIL" as the evaluation
In the case of a "FAIL", you are to provide feedback on how to improve the code in order for it to be a "PASS"
"""

generator_prompt = """
Your goal is to complete the task based on <user input>. If there are feedback
from your previous generations, you should reflect on them to improve your solution

You are to provide the end result of the code as well as the thought process behind the creation of the code
"""

task = """
Implement a Stack with:
1. push(x)
2. pop()
3. getMin()
All operations should be O(1)
"""

asyncio.run(main(task, evaluator_prompt, generator_prompt))
