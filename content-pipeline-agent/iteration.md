# Content Pipeline Agent - Prompt Chaining Pattern

## Pattern Overview

**Prompt Chaining** decomposes tasks into sequential steps where each LLM call processes the output of the previous one. This pattern excels when:
- Tasks have fixed, predictable subtasks
- Breaking tasks into steps increases accuracy
- Quality gates between steps can catch errors early

```
Input → LLM₁ → Gate₁ → LLM₂ → Gate₂ → LLM₃ → Output
```

## Agent Concept

The **Content Pipeline Agent** transforms raw content through a multi-stage pipeline:

```
Raw Content → Extract → Summarize → Translate → Format → Quality Check → Final Output
```

### Pipeline Stages

| Stage | Input | Output | Purpose |
|-------|-------|--------|---------|
| **Extract** | Raw HTML/text | Clean text | Remove noise, extract main content |
| **Summarize** | Clean text | Summary | Condense to key points |
| **Translate** | Summary | Translated text | Convert to target language |
| **Format** | Translated text | Formatted output | Apply output format (markdown, JSON, etc.) |
| **Quality Check** | Formatted output | Validated output | Verify quality criteria met |

### Quality Gates

Between each stage, a gate checks if output meets criteria before proceeding:
- Extract gate: Content length > 0, no HTML tags remaining
- Summarize gate: Summary length within bounds, key points preserved
- Translate gate: Target language detected, no source language remnants
- Format gate: Valid structure, required fields present

---

## Iteration 1: Project Setup with Mock Data

**Goal**: Set up project structure with sample content data for pipeline processing.

**Requirements**:
- Create `mock_data.py` with sample content in various formats:
  - Raw HTML articles
  - Plain text documents
  - News articles with metadata
- Create helper functions to retrieve sample content
- Basic project structure

**Mock Data Scenarios**:
```python
SAMPLE_ARTICLES = [
    {
        "id": "article-001",
        "title": "Introduction to Machine Learning",
        "format": "html",
        "content": "<html>...</html>",
        "source_language": "en",
        "metadata": {"author": "...", "date": "..."}
    },
    # More articles in different formats...
]

SAMPLE_DOCUMENTS = [
    {
        "id": "doc-001",
        "title": "Quarterly Report Q4 2024",
        "format": "text",
        "content": "...",
        "metadata": {...}
    },
]
```

**Helper Functions**:
```python
def get_article_by_id(article_id: str) -> dict | None:
    """Get a sample article by ID."""
    pass

def get_articles_by_format(format: str) -> list[dict]:
    """Get articles filtered by format (html, text, markdown)."""
    pass

def list_available_content() -> list[dict]:
    """List all available sample content with metadata."""
    pass
```

**Expected Structure**:
```
content-pipeline-agent/
├── mock_data.py      # Sample content and helpers
├── iteration.md      # This file
└── .claude/
    └── skills/       # Will hold pipeline skills
```

**Key Concepts Tested**:
- Data modeling for content processing
- Sample data generation
- Project organization

---

## Iteration 2: Single-Stage Pipeline (Extract)

**Goal**: Create the first pipeline stage - content extraction with a quality gate.

**Requirements**:
- Create `extract_content` tool that cleans raw HTML/text
- Implement extraction gate that validates output
- Basic pipeline runner that executes one stage

**Tool Definition**:
```python
@tool("extract_content", "Extract clean text from raw content", {
    "content": str,
    "format": str  # "html", "text", "markdown"
})
async def extract_content(args: dict) -> dict:
    """
    Extract clean text from raw content.
    - Remove HTML tags if format is html
    - Normalize whitespace
    - Extract main content body
    """
    pass
```

**Gate Implementation**:
```python
def extraction_gate(extracted_content: str) -> tuple[bool, str]:
    """
    Validate extracted content meets criteria.
    Returns (passed, reason).

    Criteria:
    - Content length > 100 characters
    - No HTML tags remaining
    - Not empty/whitespace only
    """
    pass
```

**Pipeline Runner**:
```python
async def run_pipeline_stage(stage_name: str, input_data: dict) -> dict:
    """Run a single pipeline stage and check its gate."""
    pass
```

**Test Prompts**:
```
"Extract the main content from article-001"
"Clean up this HTML and give me just the text"
```

**Key Concepts Tested**:
- Single MCP tool for content transformation
- Quality gate pattern
- Stage validation

---

## Iteration 3: Two-Stage Chaining (Extract → Summarize)

**Goal**: Chain two stages together with gates between them.

**Requirements**:
- Add `summarize_content` tool
- Implement summary gate
- Chain extraction output to summarization input
- Handle gate failures gracefully

**Tool Definition**:
```python
@tool("summarize_content", "Summarize extracted content to key points", {
    "content": str,
    "max_length": int,  # Target summary length
    "style": str        # "bullets", "paragraph", "executive"
})
async def summarize_content(args: dict) -> dict:
    """
    Summarize content to key points.
    - Identify main themes
    - Extract key facts
    - Preserve important details
    """
    pass
```

**Summary Gate**:
```python
def summary_gate(summary: str, original_length: int) -> tuple[bool, str]:
    """
    Validate summary meets criteria.

    Criteria:
    - Summary length < 30% of original
    - Contains at least 3 key points
    - No critical information loss (heuristic)
    """
    pass
```

**Chaining Logic**:
```python
async def run_chain(content: str, stages: list[str]) -> dict:
    """
    Run multiple pipeline stages in sequence.
    Stop if any gate fails.

    Returns:
    {
        "success": bool,
        "stages_completed": ["extract", "summarize"],
        "failed_stage": None or "stage_name",
        "output": "final output",
        "intermediate": {"extract": "...", "summarize": "..."}
    }
    """
    pass
```

**Test Prompts**:
```
"Extract and summarize article-001 in bullet points"
"Give me an executive summary of doc-001"
```

**Key Concepts Tested**:
- Multi-stage chaining
- Output-to-input passing
- Gate failure handling
- Intermediate result tracking

---

## Iteration 4: Full Pipeline (Extract → Summarize → Translate → Format)

**Goal**: Implement the complete content transformation pipeline.

**Requirements**:
- Add `translate_content` tool
- Add `format_output` tool
- Implement gates for each stage
- Full pipeline execution with all stages

**Tool Definitions**:
```python
@tool("translate_content", "Translate content to target language", {
    "content": str,
    "source_language": str,
    "target_language": str
})
async def translate_content(args: dict) -> dict:
    """Translate content between languages."""
    pass

@tool("format_output", "Format content into specified structure", {
    "content": str,
    "output_format": str,  # "markdown", "json", "html", "plain"
    "template": str        # Optional template name
})
async def format_output(args: dict) -> dict:
    """Format content into specified output structure."""
    pass
```

**Pipeline Configuration**:
```python
PIPELINE_CONFIG = {
    "stages": [
        {"name": "extract", "tool": "extract_content", "gate": extraction_gate},
        {"name": "summarize", "tool": "summarize_content", "gate": summary_gate},
        {"name": "translate", "tool": "translate_content", "gate": translation_gate},
        {"name": "format", "tool": "format_output", "gate": format_gate},
    ],
    "stop_on_gate_failure": True,
    "collect_intermediate": True,
}
```

**Test Prompts**:
```
"Process article-001: extract, summarize to 3 bullets, translate to Spanish, format as JSON"
"Run the full pipeline on doc-001 with French output"
```

**Key Concepts Tested**:
- Complete prompt chaining pipeline
- Configurable stage ordering
- Multiple gate validations
- End-to-end transformation

---

## Iteration 5: Pipeline Skills and Quality Checks

**Goal**: Add Skills for pipeline best practices and a final quality check stage.

**Requirements**:
- Create `content-pipeline` Skill with transformation best practices
- Add `quality_check` tool as final validation stage
- Configure `setting_sources` for Skill discovery

**Skill Content** (`.claude/skills/content-pipeline/SKILL.md`):
```yaml
---
name: content-pipeline
description: "Best practices for content transformation pipelines. Use when processing, summarizing, translating, or formatting content."
---

# Content Pipeline Skill

## Extraction Best Practices
- Preserve semantic structure (paragraphs, lists)
- Remove boilerplate (navigation, ads, footers)
- Keep metadata when relevant

## Summarization Guidelines
- Executive summary: 3-5 sentences, key decisions/actions
- Bullet points: 5-10 items, one concept per bullet
- Paragraph: 100-200 words, narrative flow

## Translation Quality
- Preserve tone and style
- Maintain technical terminology
- Adapt idioms appropriately

## Output Formatting
- Markdown: Use headers, lists, code blocks
- JSON: Include metadata fields
- Plain: Clean paragraphs, no markup
```

**Quality Check Tool**:
```python
@tool("quality_check", "Final quality validation of pipeline output", {
    "content": str,
    "original_content": str,
    "pipeline_config": dict
})
async def quality_check(args: dict) -> dict:
    """
    Final quality validation.

    Checks:
    - Information preservation (key facts retained)
    - Format compliance
    - Language correctness
    - Length appropriateness

    Returns score 0-100 and issues list.
    """
    pass
```

**Test Prompts**:
```
"Process article-001 following content pipeline best practices"
"Run quality check on the processed output"
```

**Key Concepts Tested**:
- Skill integration with pipeline
- Final quality validation
- Best practices encoding

---

## Iteration 6: CLI, Hooks, and Deterministic Pipeline

**Goal**: Add CLI interface, hooks for monitoring, and deterministic pipeline execution.

**Requirements**:
- CLI using shared `AgentCLI` module
- PreToolUse hooks to log pipeline progress
- Deterministic pipeline execution (Python controls the flow, not LLM)
- Progress reporting between stages

**Hook Implementation**:
```python
async def log_pipeline_stage(input_data, tool_use_id, context):
    """Log pipeline stage execution."""
    tool_name = input_data.get('tool_name', '')
    if tool_name.startswith('mcp__pipeline__'):
        stage = tool_name.replace('mcp__pipeline__', '')
        print(f"[PIPELINE] Stage: {stage}")
    return {}
```

**Deterministic Pipeline Runner**:
```python
async def run_deterministic_pipeline(
    content: str,
    stages: list[str],
    options: dict
) -> dict:
    """
    Run pipeline with Python controlling the flow.

    - Calls each tool directly (not via LLM orchestration)
    - Checks gates deterministically
    - Reports progress at each stage
    - Handles failures with retry or skip options
    """
    results = {"stages": [], "success": True}

    current_input = content
    for stage in stages:
        print(f"[STAGE] Running: {stage}")

        # Call tool directly
        output = await TOOLS[stage]({"content": current_input, **options})

        # Check gate
        passed, reason = GATES[stage](output)
        if not passed:
            results["success"] = False
            results["failed_at"] = stage
            results["reason"] = reason
            break

        results["stages"].append({"name": stage, "output": output})
        current_input = output

    return results
```

**CLI Configuration**:
```python
cli = AgentCLI(
    name="Content Pipeline Agent",
    description="Transform content through a multi-stage pipeline",
    arguments=[
        CLIArgument(name="--input", short="-i", help="Input content or article ID"),
        CLIArgument(name="--stages", help="Comma-separated stages to run"),
        CLIArgument(name="--target-lang", help="Target language for translation"),
        CLIArgument(name="--output-format", help="Output format (markdown, json, plain)"),
        CLIArgument(name="--deterministic", short="-d", help="Use deterministic pipeline", action="store_true"),
        CLIArgument(name="--verbose", short="-v", help="Show stage progress", action="store_true"),
    ]
)
```

**Usage Examples**:
```bash
# LLM-orchestrated pipeline
python content_pipeline.py -i article-001 --stages extract,summarize,translate --target-lang es

# Deterministic pipeline with progress
python content_pipeline.py -i article-001 -d -v --stages extract,summarize,format

# Full pipeline to JSON
python content_pipeline.py -i doc-001 --output-format json --target-lang fr
```

**Key Concepts Tested**:
- Prompt chaining with deterministic control
- LLM-orchestrated vs Python-controlled pipelines
- Progress monitoring
- CLI for pipeline configuration

---

## Pattern Summary

| Aspect | Implementation |
|--------|----------------|
| **Chaining** | Sequential tool calls with output→input passing |
| **Gates** | Validation functions between stages |
| **Deterministic Option** | Python controls flow, not LLM |
| **Failure Handling** | Stop, retry, or skip on gate failure |
| **Monitoring** | Hooks log each stage execution |

## Tools Summary

| Tool | Stage | Purpose |
|------|-------|---------|
| `extract_content` | 1 | Clean raw content |
| `summarize_content` | 2 | Condense to key points |
| `translate_content` | 3 | Convert to target language |
| `format_output` | 4 | Apply output format |
| `quality_check` | 5 | Final validation |

## Comparison: LLM-Orchestrated vs Deterministic

| Aspect | LLM-Orchestrated | Deterministic |
|--------|------------------|---------------|
| Flow control | LLM decides next step | Python loop |
| Flexibility | Can adapt to content | Fixed stage order |
| Reliability | May skip stages | Guaranteed execution |
| Debugging | Harder to trace | Clear step-by-step |
| Use case | Complex content | Consistent processing |
