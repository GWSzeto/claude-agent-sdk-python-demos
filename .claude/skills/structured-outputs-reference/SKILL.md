---
name: structured-outputs-reference
description: "Reference for getting structured JSON output from Claude Agent SDK. Use when you need typed, validated JSON responses from query() calls instead of free-form text."
---

# Structured Outputs Reference

Get validated JSON from agent workflows using JSON Schema or Pydantic. The SDK guarantees output matches your schema.

## Why Use Structured Outputs

- **Reliable parsing**: No regex or text parsing needed
- **Validated data**: SDK ensures output matches schema
- **Type safety**: Use Pydantic for typed Python objects
- **Works with tools**: Agent can use tools, still returns structured output

## Basic Usage

Pass `output_format` to `ClaudeAgentOptions`:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "count": {"type": "number"}
    },
    "required": ["name", "count"]
}

async for message in query(
    prompt="Count the files in this directory",
    options=ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "schema": schema
        }
    )
):
    if isinstance(message, ResultMessage) and message.structured_output:
        print(message.structured_output)
        # {'name': 'src', 'count': 42}
```

## With Pydantic (Recommended)

Use Pydantic for type safety and validation:

```python
from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

class ExtractionResult(BaseModel):
    content: str
    word_count: int
    format: str

async for message in query(
    prompt="Extract the main content from article-001",
    options=ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "schema": ExtractionResult.model_json_schema()
        }
    )
):
    if isinstance(message, ResultMessage) and message.structured_output:
        # Validate and get typed object
        result = ExtractionResult.model_validate(message.structured_output)
        print(result.content)  # Type-safe access
```

## Key Points

1. **Schema goes in options, not the prompt**
   ```python
   options=ClaudeAgentOptions(
       output_format={"type": "json_schema", "schema": schema}
   )
   ```

2. **Result is in `message.structured_output`**
   ```python
   if isinstance(message, ResultMessage) and message.structured_output:
       data = message.structured_output  # Already validated dict
   ```

3. **Works with tools**: Agent can use any tools, structured output is the final response

4. **Use `model_json_schema()`** for Pydantic models:
   ```python
   schema=MyModel.model_json_schema()
   ```

## Error Handling

Check `subtype` for errors:

```python
if isinstance(message, ResultMessage):
    if message.subtype == "success" and message.structured_output:
        # Use the output
        pass
    elif message.subtype == "error_max_structured_output_retries":
        # Schema too complex or task ambiguous
        pass
```

## Schema Tips

- Keep schemas focused and simple
- Make fields optional if data might not exist
- Use clear prompts that match what schema expects
- Start simple, add complexity as needed

## Common Patterns

### Validation/Gate Pattern
```python
class GateResult(BaseModel):
    passed: bool
    reason: str
    checks: dict[str, bool]
```

### Extraction Pattern
```python
class ExtractedContent(BaseModel):
    content: str
    metadata: dict
    source_format: str
```

### Multi-Step Pipeline
Each step uses its own schema:
```python
# Step 1: Extract
class ExtractResult(BaseModel): ...

# Step 2: Validate
class GateResult(BaseModel): ...

# Step 3: Transform
class TransformResult(BaseModel): ...
```
