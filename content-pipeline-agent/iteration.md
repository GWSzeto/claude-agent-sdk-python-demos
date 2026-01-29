# Content Pipeline Agent - Prompt Chaining Pattern

## Pattern Overview

**Prompt Chaining** decomposes tasks into sequential steps where each LLM call processes the output of the previous one. This pattern excels when:
- Tasks have fixed, predictable subtasks
- Breaking tasks into steps increases accuracy
- Quality gates between steps can catch errors early

```
Python Control Flow
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   query()    │     │   query()    │     │   query()    │
│      +       │ ──► │      +       │ ──► │      +       │
│   schema 1   │     │   schema 2   │     │   schema 3   │
└──────────────┘     └──────────────┘     └──────────────┘
     Extract            Gate               Summarize
```

**Key Technique**: Use `output_format` with JSON Schema (via Pydantic) to get validated, structured responses from each `query()` call. No manual JSON parsing needed.

## Core Technique: Structured Outputs

Instead of parsing JSON from text responses (brittle), use `output_format` to get validated structured data:

```python
from pydantic import BaseModel
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

class MyResult(BaseModel):
    content: str
    score: int

async for message in query(
    prompt="Your prompt here",
    options=ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "schema": MyResult.model_json_schema()
        }
    )
):
    if isinstance(message, ResultMessage) and message.structured_output:
        result = MyResult.model_validate(message.structured_output)
        # result.content and result.score are typed and validated
```

---

## Agent Concept

The **Content Pipeline Agent** transforms raw content through a multi-stage pipeline:

```
Raw Content → Extract → Gate → Summarize → Gate → Translate → Gate → Format → Final Output
```

Each stage is a `query()` call with its own Pydantic schema.

---

## Iteration 1: Project Setup with Mock Data

**Goal**: Set up project structure with sample content data for pipeline processing.

**Requirements**:
- Create `mock_data.py` with sample content in various formats
- Create helper functions to retrieve sample content
- Basic project structure

**Expected Structure**:
```
content-pipeline-agent/
├── mock_data.py      # Sample content and helpers
├── content_pipeline.py  # Main pipeline
├── iteration.md      # This file
└── pyproject.toml    # Dependencies (pydantic)
```

**Key Concepts**: Data modeling, project organization

---

## Iteration 2: Single-Stage Pipeline (Extract + Gate)

**Goal**: Create the first pipeline stage with structured outputs for reliable JSON responses.

### Pydantic Models

Define the output schemas:

```python
from pydantic import BaseModel

class ExtractResult(BaseModel):
    """Output from extraction step."""
    extracted_content: str
    original_length: int
    extracted_length: int
    title: str

class GateResult(BaseModel):
    """Output from gate validation step."""
    passed: bool
    reason: str
    checks: dict[str, bool]
```

### Pipeline Runner

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage
from mock_data import get_content_by_id

async def run_extract(content_id: str) -> ExtractResult | None:
    """Step 1: Extract content using structured output."""

    content_data = get_content_by_id(content_id)
    if not content_data:
        return None

    async for message in query(
        prompt=f"""Extract the main content from this document. Remove HTML tags,
navigation, footers, and ads. Keep only the main article text.

Document:
{content_data['content'][:2000]}

Return the cleaned content.""",
        options=ClaudeAgentOptions(
            model="sonnet",
            output_format={
                "type": "json_schema",
                "schema": ExtractResult.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            return ExtractResult.model_validate(message.structured_output)

    return None


async def run_extraction_gate(extract_result: ExtractResult) -> GateResult | None:
    """Step 2: Validate extraction quality using structured output."""

    async for message in query(
        prompt=f"""Validate this extracted content meets quality criteria:

Content (first 500 chars): {extract_result.extracted_content[:500]}...
Original length: {extract_result.original_length}
Extracted length: {extract_result.extracted_length}

Check:
1. min_length: Content > 100 characters
2. has_substance: Content is meaningful, not just boilerplate
3. coherent: Content reads as proper sentences/paragraphs

Return whether it passes all checks.""",
        options=ClaudeAgentOptions(
            model="sonnet",
            output_format={
                "type": "json_schema",
                "schema": GateResult.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            return GateResult.model_validate(message.structured_output)

    return None


async def run_pipeline(content_id: str) -> dict:
    """Run the extract + gate pipeline."""

    print(f"[PIPELINE] Starting for {content_id}")

    # Step 1: Extract
    print("[STEP 1] Extracting...")
    extract_result = await run_extract(content_id)

    if not extract_result:
        return {"success": False, "error": "Extraction failed"}

    print(f"[STEP 1] Extracted {extract_result.extracted_length} chars")

    # Step 2: Gate
    print("[STEP 2] Validating...")
    gate_result = await run_extraction_gate(extract_result)

    if not gate_result:
        return {"success": False, "error": "Gate validation failed"}

    print(f"[STEP 2] Gate: {'PASSED' if gate_result.passed else 'FAILED'}")
    print(f"[STEP 2] Reason: {gate_result.reason}")

    # Return result
    if gate_result.passed:
        return {
            "success": True,
            "extracted": extract_result.extracted_content,
            "title": extract_result.title
        }
    else:
        return {
            "success": False,
            "failed_at": "extraction_gate",
            "reason": gate_result.reason
        }
```

### Main Entry Point

```python
async def main():
    result = await run_pipeline("article-001")

    if result["success"]:
        print(f"\n--- SUCCESS ---")
        print(f"Title: {result['title']}")
        print(f"Content: {result['extracted'][:300]}...")
    else:
        print(f"\n--- FAILED ---")
        print(f"Reason: {result.get('reason', result.get('error'))}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Key Concepts

| Concept | Implementation |
|---------|----------------|
| **Structured output** | `output_format={"type": "json_schema", "schema": Model.model_json_schema()}` |
| **Type safety** | Pydantic models with `model_validate()` |
| **Prompt chaining** | Sequential `query()` calls, output feeds into next prompt |
| **Gate pattern** | Second query validates first query's output |

---

## Iteration 3: Two-Stage Chaining (Extract → Summarize)

**Goal**: Chain extraction and summarization with gates between them.

### Additional Models

```python
class SummarizeResult(BaseModel):
    """Output from summarization step."""
    summary: str
    key_points: list[str]
    original_length: int
    summary_length: int

class SummaryGateResult(BaseModel):
    """Output from summary validation."""
    passed: bool
    reason: str
    checks: dict[str, bool]
```

### Summarize Step

```python
async def run_summarize(content: str, style: str = "bullets") -> SummarizeResult | None:
    """Step 3: Summarize content."""

    async for message in query(
        prompt=f"""Summarize this content into key points.

Style: {style}
Content:
{content[:3000]}

Extract the main themes and important facts.""",
        options=ClaudeAgentOptions(
            model="sonnet",
            output_format={
                "type": "json_schema",
                "schema": SummarizeResult.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            return SummarizeResult.model_validate(message.structured_output)

    return None
```

### Chained Pipeline

```python
async def run_two_stage_pipeline(content_id: str, style: str = "bullets") -> dict:
    """Extract → Gate → Summarize → Gate"""

    # Step 1: Extract
    extract_result = await run_extract(content_id)
    if not extract_result:
        return {"success": False, "error": "Extraction failed"}

    # Step 2: Extraction Gate
    gate1 = await run_extraction_gate(extract_result)
    if not gate1 or not gate1.passed:
        return {"success": False, "failed_at": "extraction_gate", "reason": gate1.reason if gate1 else "Unknown"}

    # Step 3: Summarize (uses extraction output)
    summary_result = await run_summarize(extract_result.extracted_content, style)
    if not summary_result:
        return {"success": False, "error": "Summarization failed"}

    # Step 4: Summary Gate
    gate2 = await run_summary_gate(summary_result, extract_result.extracted_content)
    if not gate2 or not gate2.passed:
        return {"success": False, "failed_at": "summary_gate", "reason": gate2.reason if gate2 else "Unknown"}

    return {
        "success": True,
        "summary": summary_result.summary,
        "key_points": summary_result.key_points
    }
```

---

## Iteration 4: Full Pipeline (Extract → Summarize → Translate → Format)

**Goal**: Complete pipeline with all transformation stages.

### Additional Models

```python
class TranslateResult(BaseModel):
    translated_content: str
    source_language: str
    target_language: str

class FormatResult(BaseModel):
    formatted_content: str
    format_type: str  # "markdown", "json", "plain"
```

### Generic Stage Runner

```python
from typing import TypeVar, Type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

async def run_stage(prompt: str, schema_class: Type[T]) -> T | None:
    """Generic stage runner with structured output."""

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            model="sonnet",
            output_format={
                "type": "json_schema",
                "schema": schema_class.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            return schema_class.model_validate(message.structured_output)

    return None
```

### Full Pipeline

```python
async def run_full_pipeline(
    content_id: str,
    target_language: str = "es",
    output_format: str = "markdown"
) -> dict:
    """Extract → Summarize → Translate → Format with gates."""

    stages = []

    # Extract
    extract = await run_stage(
        f"Extract main content from: {get_content_by_id(content_id)['content'][:2000]}",
        ExtractResult
    )
    if not extract:
        return {"success": False, "failed_at": "extract"}
    stages.append(("extract", extract))

    # Extract Gate
    gate1 = await run_stage(
        f"Validate extraction: {extract.extracted_content[:500]}...",
        GateResult
    )
    if not gate1 or not gate1.passed:
        return {"success": False, "failed_at": "extract_gate"}

    # Summarize
    summary = await run_stage(
        f"Summarize: {extract.extracted_content[:2000]}",
        SummarizeResult
    )
    if not summary:
        return {"success": False, "failed_at": "summarize"}
    stages.append(("summarize", summary))

    # Summary Gate
    gate2 = await run_stage(
        f"Validate summary preserves key info. Original: {extract.extracted_content[:500]}... Summary: {summary.summary}",
        GateResult
    )
    if not gate2 or not gate2.passed:
        return {"success": False, "failed_at": "summary_gate"}

    # Translate
    translate = await run_stage(
        f"Translate to {target_language}: {summary.summary}",
        TranslateResult
    )
    if not translate:
        return {"success": False, "failed_at": "translate"}
    stages.append(("translate", translate))

    # Format
    formatted = await run_stage(
        f"Format as {output_format}: {translate.translated_content}",
        FormatResult
    )
    if not formatted:
        return {"success": False, "failed_at": "format"}
    stages.append(("format", formatted))

    return {
        "success": True,
        "output": formatted.formatted_content,
        "stages": [(name, s.model_dump()) for name, s in stages]
    }
```

---

## Iteration 5: Skills Integration

**Goal**: Add content-pipeline skill for best practices.

Create `.claude/skills/content-pipeline/SKILL.md`:

```yaml
---
name: content-pipeline
description: "Best practices for content transformation. Use when extracting, summarizing, translating, or formatting content."
---

# Content Pipeline Best Practices

## Extraction
- Remove navigation, ads, footers
- Preserve semantic structure
- Keep metadata when relevant

## Summarization
- Bullets: 5-10 items, one concept each
- Executive: 3-5 sentences, key decisions
- Preserve critical facts

## Translation
- Maintain tone and style
- Adapt idioms appropriately
- Keep technical terms consistent
```

Enable skills in options:

```python
options = ClaudeAgentOptions(
    model="sonnet",
    cwd="/path/to/content-pipeline-agent",
    setting_sources=["user", "project"],  # Required for skills
    output_format={"type": "json_schema", "schema": schema}
)
```

---

## Iteration 6: CLI and Error Handling

**Goal**: Add CLI interface and robust error handling.

### Error Handling

```python
async def run_stage_safe(prompt: str, schema_class: Type[T], stage_name: str) -> tuple[T | None, str | None]:
    """Run stage with error handling."""

    try:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                model="sonnet",
                output_format={
                    "type": "json_schema",
                    "schema": schema_class.model_json_schema()
                }
            )
        ):
            if isinstance(message, ResultMessage):
                if message.subtype == "success" and message.structured_output:
                    return schema_class.model_validate(message.structured_output), None
                elif message.subtype == "error_max_structured_output_retries":
                    return None, f"{stage_name}: Could not produce valid output"

        return None, f"{stage_name}: No result received"

    except Exception as e:
        return None, f"{stage_name}: {str(e)}"
```

### CLI

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Content Pipeline Agent")
    parser.add_argument("-i", "--input", required=True, help="Content ID")
    parser.add_argument("--target-lang", default="es", help="Target language")
    parser.add_argument("--format", default="markdown", help="Output format")
    args = parser.parse_args()

    result = asyncio.run(run_full_pipeline(
        args.input,
        target_language=args.target_lang,
        output_format=args.format
    ))

    if result["success"]:
        print(result["output"])
    else:
        print(f"Failed at: {result['failed_at']}")

if __name__ == "__main__":
    main()
```

---

## Pattern Summary

| Aspect | Implementation |
|--------|----------------|
| **Structured output** | `output_format` with Pydantic schemas |
| **Type safety** | `model_validate()` for typed objects |
| **Flow control** | Python controls sequence of `query()` calls |
| **Data passing** | Output from step N feeds into prompt for step N+1 |
| **Gates** | Separate `query()` with `GateResult` schema |

## Benefits of Structured Outputs

| Before (Manual Parsing) | After (Structured Outputs) |
|------------------------|---------------------------|
| Parse JSON from text with regex | Direct access to `structured_output` |
| Handle malformed JSON | SDK validates against schema |
| No type safety | Pydantic provides typed objects |
| Brittle extraction | Guaranteed schema compliance |

## Models Reference

```python
# Core models for the pipeline
class ExtractResult(BaseModel):
    extracted_content: str
    original_length: int
    extracted_length: int
    title: str

class GateResult(BaseModel):
    passed: bool
    reason: str
    checks: dict[str, bool]

class SummarizeResult(BaseModel):
    summary: str
    key_points: list[str]
    original_length: int
    summary_length: int

class TranslateResult(BaseModel):
    translated_content: str
    source_language: str
    target_language: str

class FormatResult(BaseModel):
    formatted_content: str
    format_type: str
```
