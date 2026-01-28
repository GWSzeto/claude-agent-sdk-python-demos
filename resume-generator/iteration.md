# Resume Generator - Python Implementation Iterations

## TypeScript Demo Analysis

### Key Agentic Components

The TypeScript resume-generator demo demonstrates:

1. **WebSearch Tool** - Searches for a person's professional background (LinkedIn, GitHub, company pages)
2. **WebFetch Tool** - Fetches detailed page content
3. **Skill (docx)** - Comprehensive skill documentation for creating Word documents with docx-js
4. **Write Tool** - Writes JavaScript scripts to generate documents
5. **Bash Tool** - Executes scripts to produce .docx files

### Workflow

```
Person Name → WebSearch → Gather Info → Generate JS Script → Execute → .docx Resume
                ↓
         Search LinkedIn, GitHub,
         Company pages, News
```

### Original Tools Used
- `WebSearch` - Web search API
- `WebFetch` - Page content fetching
- `Skill` - docx skill for document creation
- `Write`, `Read`, `Bash`, `Glob`

---

## Python Implementation Approach

### Stubbed APIs (Mock Data)
Instead of real API calls, we'll create stubbed functions that return realistic mock data:
- `mock_web_search()` - Returns mock search results
- `mock_linkedin_profile()` - Returns structured profile data

### Custom MCP Tools
Using the `@tool` decorator to create MCP tools:

1. **web_search** - Stubbed web search tool
2. **get_linkedin_profile** - NEW: Structured LinkedIn profile data (stubbed)
3. **analyze_resume_data** - NEW: Aggregates data into resume-ready format
4. **generate_resume_docx** - Creates the .docx file using python-docx

### Python Libraries
- `python-docx` - For creating Word documents (replaces docx-js)
- `claude-agent-sdk` - Agent SDK with custom tools

---

## Iteration 1: Project Setup with Stubbed Web Search

**Goal**: Set up project structure and create a stubbed web search tool.

**Requirements**:
- Create `mock_data.py` with stubbed web search results
- Create a basic MCP tool using `@tool` decorator for web search
- Use `ClaudeSDKClient` with the custom tool
- Query the agent to search for a person

**Stubbed Data Structure** (`mock_data.py`):
```python
MOCK_SEARCH_RESULTS = {
    "John Smith": {
        "results": [
            {
                "title": "John Smith - Senior Software Engineer at TechCorp",
                "url": "https://linkedin.com/in/johnsmith",
                "snippet": "Senior Software Engineer with 8+ years of experience..."
            },
            {
                "title": "John Smith GitHub Profile",
                "url": "https://github.com/johnsmith",
                "snippet": "Open source contributor, 500+ contributions..."
            }
        ]
    }
}
```

**Tool Definition**:
```python
from claude_agent_sdk import tool

@tool("web_search", "Search the web for information about a person", {"query": str})
async def web_search(args: dict) -> dict:
    query = args["query"]
    # Return mock results
    return {"content": [{"type": "text", "text": json.dumps(results)}]}
```

**Expected Output**:
```
[TOOL] web_search called with: {"query": "John Smith professional background"}
[ASSISTANT] Based on my search, John Smith is a Senior Software Engineer...
```

**Key Concepts Tested**:
- MCP tool creation with `@tool` decorator
- `create_sdk_mcp_server()` for in-process tools
- Stubbed/mocked API responses
- `ClaudeSDKClient` with custom tools

---

## Iteration 2: LinkedIn Profile Tool (NEW)

**Goal**: Create a structured LinkedIn profile tool that returns detailed professional data.

**Requirements**:
- Add `mock_linkedin_profile()` to `mock_data.py`
- Create `get_linkedin_profile` MCP tool
- Returns structured data: name, headline, experience, education, skills
- Integrate with existing agent

**Stubbed Data Structure**:
```python
MOCK_LINKEDIN_PROFILES = {
    "John Smith": {
        "name": "John Smith",
        "headline": "Senior Software Engineer at TechCorp",
        "location": "San Francisco, CA",
        "summary": "Passionate software engineer with 8+ years...",
        "experience": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp",
                "duration": "2020 - Present",
                "description": "Led development of microservices architecture..."
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "duration": "2016 - 2020",
                "description": "Full-stack development using React and Node.js..."
            }
        ],
        "education": [
            {
                "degree": "B.S. Computer Science",
                "school": "Stanford University",
                "year": "2016"
            }
        ],
        "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"]
    }
}
```

**Tool Definition**:
```python
@tool("get_linkedin_profile", "Get structured LinkedIn profile data for a person", {"name": str})
async def get_linkedin_profile(args: dict) -> dict:
    name = args["name"]
    profile = MOCK_LINKEDIN_PROFILES.get(name, DEFAULT_PROFILE)
    return {"content": [{"type": "text", "text": json.dumps(profile, indent=2)}]}
```

**Expected Output**:
```
[TOOL] get_linkedin_profile called with: {"name": "John Smith"}
[ASSISTANT] I found John Smith's LinkedIn profile. He is a Senior Software Engineer...
```

**Key Concepts Tested**:
- Multiple MCP tools in one server
- Structured data responses
- Default fallback data

---

## Iteration 3: Resume Data Analyzer Tool (NEW)

**Goal**: Create a tool that aggregates and structures data into a resume-ready format.

**Requirements**:
- Create `analyze_resume_data` MCP tool
- Takes raw data (search results + profile) and outputs structured resume sections
- Validates and formats data for resume generation

**Tool Definition**:
```python
@tool(
    "analyze_resume_data",
    "Analyze and structure profile data into resume-ready format",
    {
        "name": str,
        "profile_data": str,  # JSON string of profile data
        "additional_info": str  # JSON string of search results
    }
)
async def analyze_resume_data(args: dict) -> dict:
    # Parse and structure data
    # Return formatted resume sections
    resume_data = {
        "header": {...},
        "summary": "...",
        "experience": [...],
        "education": [...],
        "skills": [...]
    }
    return {"content": [{"type": "text", "text": json.dumps(resume_data, indent=2)}]}
```

**Expected Output**:
```
[TOOL] analyze_resume_data called with: {"name": "John Smith", ...}
[ASSISTANT] I've analyzed the data and structured it for the resume...
```

**Key Concepts Tested**:
- Complex tool with multiple parameters
- Data transformation and validation
- Preparing structured output for document generation

---

## Iteration 4: Resume Document Generation

**Goal**: Create the actual .docx resume using python-docx.

**Requirements**:
- Create `generate_resume_docx` MCP tool
- Use `python-docx` library to create professional resume
- Follow formatting guidelines: 0.5" margins, proper fonts, 1-page fit
- Save to `agent/custom_scripts/resume.docx`

**Tool Definition**:
```python
@tool(
    "generate_resume_docx",
    "Generate a professional resume as a .docx file",
    {
        "resume_data": str,  # JSON string of structured resume data
        "output_path": str   # Path to save the .docx file
    }
)
async def generate_resume_docx(args: dict) -> dict:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    data = json.loads(args["resume_data"])
    output_path = args["output_path"]

    doc = Document()
    # Set margins, add sections, format text...
    doc.save(output_path)

    return {"content": [{"type": "text", "text": f"Resume saved to {output_path}"}]}
```

**Resume Format Specs**:
- Margins: 0.5 inches all sides
- Name: 24pt, bold, centered
- Section Headers: 12pt, bold, uppercase
- Body Text: 10pt
- Max 3 job roles, 2-3 bullets each (~80-100 chars)

**Expected Output**:
```
[TOOL] generate_resume_docx called with: {"resume_data": "...", "output_path": "..."}
[ASSISTANT] I've generated the resume and saved it to agent/custom_scripts/resume.docx
```

**Key Concepts Tested**:
- python-docx library usage
- Document formatting and styling
- File I/O within MCP tools

---

## Iteration 5: Full Feature with CLI and Hooks (Final)

**Goal**: Production-ready implementation with CLI, hooks, and error handling.

**Requirements**:
- Command-line arguments:
  - `name` (positional) - Person's name
  - `--output` / `-o` - Output path (default: agent/custom_scripts/resume.docx)
  - `--verbose` / `-v` - Show all tool calls and responses
- PreToolUse hook for logging
- Error handling for missing data, file errors
- Clean code organization

**Expected Usage**:
```bash
# Basic usage
python resume_generator.py "John Smith"

# Custom output path
python resume_generator.py "Jane Doe" -o ./output/jane_resume.docx

# Verbose mode
python resume_generator.py "John Smith" --verbose
```

**Code Structure**:
```python
#!/usr/bin/env python3
"""Resume Generator using Claude Agent SDK with custom MCP tools."""

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookMatcher,
    HookContext,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
)

from mock_data import MOCK_SEARCH_RESULTS, MOCK_LINKEDIN_PROFILES

# Tool definitions...

async def log_tool_use(input_data: dict, tool_use_id: str | None, context: HookContext) -> dict:
    """Log all tool usage."""
    ...

async def generate_resume(name: str, output_path: str, verbose: bool) -> None:
    """Main function to generate a resume."""
    ...

def main():
    parser = argparse.ArgumentParser(description="Generate professional resumes")
    parser.add_argument("name", help="Name of the person")
    parser.add_argument("-o", "--output", default="agent/custom_scripts/resume.docx")
    parser.add_argument("-v", "--verbose", action="store_true")
    ...
```

**Key Concepts Tested**:
- Full MCP tool integration
- Multiple tools working together
- Hooks with ClaudeSDKClient
- Production code quality

---

## Iteration 6: Resume Quality Evaluator (Evaluator-Optimizer Pattern)

**Goal**: Implement iterative resume refinement using the evaluator-optimizer pattern from Anthropic's building effective agents research.

**Background**: The evaluator-optimizer pattern loops between one LLM generating content and another providing iterative feedback. This is ideal for resume generation where quality can be objectively measured.

**Pattern Flow**:
```
Generate Resume → Evaluate Quality → (if score < threshold) → Improve Sections → Re-evaluate
      ↑                                                              │
      └──────────────────────────────────────────────────────────────┘
```

**Requirements**:
- Create `evaluate_resume_quality` MCP tool
- Create `improve_resume_section` MCP tool
- Implement quality scoring with specific criteria
- Add iteration loop until quality threshold is met
- Maximum 3 refinement iterations to prevent infinite loops

**New Tool 1: evaluate_resume_quality**:
```python
@tool(
    "evaluate_resume_quality",
    "Evaluate a resume against quality criteria and return a score with feedback",
    {
        "resume_json": str,  # JSON string of the resume data
    }
)
async def evaluate_resume_quality(args: dict) -> dict:
    """
    Quality Criteria (each scored 0-25, total 100):
    1. Completeness: All sections present (header, summary, experience, education, skills)
    2. Conciseness: Summary < 3 sentences, bullets < 100 chars each
    3. Specificity: Contains quantified achievements (numbers, percentages)
    4. Formatting: Proper structure, no empty sections
    """
    resume = json.loads(args["resume_json"])

    score = 0
    issues = []
    suggestions = []

    # Completeness check (25 points)
    required_sections = ["header", "summary", "experience", "education", "skills"]
    missing = [s for s in required_sections if s not in resume or not resume[s]]
    completeness_score = 25 - (5 * len(missing))
    if missing:
        issues.append(f"Missing sections: {', '.join(missing)}")
    score += max(0, completeness_score)

    # Conciseness check (25 points)
    # ... check summary length, bullet lengths

    # Specificity check (25 points)
    # ... check for numbers, percentages, metrics

    # Formatting check (25 points)
    # ... check structure consistency

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "score": score,
                "passing": score >= 75,
                "issues": issues,
                "suggestions": suggestions
            }, indent=2)
        }]
    }
```

**New Tool 2: improve_resume_section**:
```python
@tool(
    "improve_resume_section",
    "Improve a specific section of the resume based on feedback",
    {
        "section": str,           # Section to improve: "summary", "experience", "skills"
        "current_content": str,   # Current content of the section (JSON)
        "improvement_type": str,  # Type: "add_metrics", "shorten", "add_detail", "restructure"
        "feedback": str           # Specific feedback to address
    }
)
async def improve_resume_section(args: dict) -> dict:
    """
    Improvement types:
    - add_metrics: Add quantified achievements (numbers, percentages)
    - shorten: Reduce length while preserving key information
    - add_detail: Expand with more specific information
    - restructure: Reorganize for better flow
    """
    section = args["section"]
    current = json.loads(args["current_content"])
    improvement_type = args["improvement_type"]
    feedback = args["feedback"]

    # Return improved section based on type
    # (In practice, the LLM will use this tool and provide the improved content)

    return {
        "content": [{
            "type": "text",
            "text": json.dumps({
                "section": section,
                "improved": True,
                "message": f"Section '{section}' improved with {improvement_type}"
            })
        }]
    }
```

**Evaluator-Optimizer Loop Implementation**:
```python
QUALITY_THRESHOLD = 75
MAX_ITERATIONS = 3

async def generate_resume_with_quality_loop(name: str, output_path: str) -> None:
    """Generate resume with iterative quality improvement."""

    prompt = f"""Generate a professional resume for {name}.

After generating the initial resume:
1. Use evaluate_resume_quality to score it
2. If score < {QUALITY_THRESHOLD}, use improve_resume_section to fix issues
3. Re-evaluate after improvements
4. Repeat until score >= {QUALITY_THRESHOLD} or {MAX_ITERATIONS} iterations reached
5. Finally, generate the .docx file

Quality criteria:
- Completeness: All sections present
- Conciseness: Bullets under 100 characters
- Specificity: Include quantified achievements
- Formatting: Consistent structure
"""

    # Run agent with quality tools
    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        # ... handle response
```

**Test Prompts**:
```
"Generate a resume for John Smith and ensure it passes quality checks"
"Create a resume for Jane Doe, iterate until the quality score is above 80"
```

**Expected Output**:
```
[TOOL] web_search called with: {"query": "John Smith professional"}
[TOOL] get_linkedin_profile called with: {"name": "John Smith"}
[TOOL] analyze_resume_data called with: {...}
[TOOL] evaluate_resume_quality called with: {...}
[ASSISTANT] Initial resume scored 65/100. Issues: Summary too long, missing metrics.
[TOOL] improve_resume_section called with: {"section": "summary", "improvement_type": "shorten", ...}
[TOOL] improve_resume_section called with: {"section": "experience", "improvement_type": "add_metrics", ...}
[TOOL] evaluate_resume_quality called with: {...}
[ASSISTANT] Improved resume scored 82/100. Generating final document.
[TOOL] generate_resume_docx called with: {...}
[ASSISTANT] Resume saved to output/john_smith_resume.docx with quality score 82/100.
```

**Key Concepts Tested**:
- Evaluator-Optimizer pattern from building effective agents
- Iterative refinement with quality thresholds
- Multi-step tool orchestration
- Measurable quality criteria

---

## Comparison Checklist

| Feature | TypeScript Demo | Python Implementation |
|---------|-----------------|----------------------|
| Web Search | `WebSearch` built-in tool | Custom `web_search` MCP tool (stubbed) |
| LinkedIn Data | Via WebSearch/WebFetch | Custom `get_linkedin_profile` tool (NEW) |
| Data Analysis | Agent reasoning | Custom `analyze_resume_data` tool (NEW) |
| Document Creation | docx-js via Skill | `generate_resume_docx` tool with python-docx |
| Skill System | `.claude/skills/docx/` | MCP tools with `@tool` decorator |
| CLI | `process.argv` | `argparse` module |

## Tools Summary

| Tool | Purpose | New/Existing |
|------|---------|--------------|
| `web_search` | Search for person's background | Replaces WebSearch (stubbed) |
| `get_linkedin_profile` | Get structured profile data | **NEW** (stubbed) |
| `analyze_resume_data` | Structure data for resume | **NEW** |
| `generate_resume_docx` | Create .docx document | Replaces Skill+Write+Bash |
| `evaluate_resume_quality` | Score resume against criteria | **NEW** (Iteration 6) |
| `improve_resume_section` | Refine specific sections | **NEW** (Iteration 6) |

## Patterns Used

| Pattern | Iteration | Description |
|---------|-----------|-------------|
| Prompt Chaining | 1-4 | Sequential tool calls with implicit verification |
| Evaluator-Optimizer | 6 | Iterative refinement with quality scoring |

## Mock Data Files

Create `mock_data.py` with realistic stubbed data for:
- Multiple people (John Smith, Jane Doe, etc.)
- Varied professional backgrounds
- Different industries and experience levels
