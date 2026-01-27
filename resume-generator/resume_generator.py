#!/usr/bin/env python3
"""Resume Generator - Creates professional resumes using Claude Agent SDK with custom MCP tools."""

import sys
from pathlib import Path
import json
from typing import Any

# Add shared module to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeSDKClient,
    ClaudeAgentOptions,
    HookContext,
    HookMatcher,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    tool,
    create_sdk_mcp_server,
)
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

from shared.cli import AgentCLI, CLIArgument, run_agent_cli
from mock_data import get_search_results, get_linkedin_profile as _get_linkedin_profile


# =============================================================================
# MCP Tool Definitions
# =============================================================================

@tool("web_search", "Search the web for information about a person", {"query": str})
async def web_search(args: dict) -> dict:
    """Search the web for information about a person."""
    query = args["query"]
    results = get_search_results(query)
    return {
        "content": [{"type": "text", "text": json.dumps(results, indent=2)}]
    }


@tool("get_linkedin_profile", "Fetch a person's LinkedIn profile", {"name": str})
async def get_linkedin_profile(args: dict) -> dict:
    """Fetch a person's LinkedIn profile data."""
    name = args["name"]
    profile = _get_linkedin_profile(name)
    return {
        "content": [{"type": "text", "text": json.dumps(profile, indent=2)}]
    }


@tool(
    "analyze_resume_data",
    "Analyze profile data and structure it for resume generation",
    {"name": str, "profile_json": str}
)
async def analyze_resume_data(args: dict) -> dict:
    """Analyze and structure profile data for resume generation."""
    name, profile_json = args["name"], args["profile_json"]
    profile = json.loads(profile_json)

    resume_data = {
        "header": {
            "name": profile.get("name", name),
            "headline": profile.get("headline", ""),
            "email": profile.get("email", ""),
            "phone": profile.get("phone", ""),
            "location": profile.get("location", ""),
            "linkedin": profile.get("linkedin_url", "")
        },
        "summary": profile.get("summary", ""),
        "experience": profile.get("experience", [])[:3],
        "education": profile.get("education", []),
        "skills": profile.get("skills", [])[:10]
    }

    return {
        "content": [{"type": "text", "text": json.dumps(resume_data, indent=2)}]
    }


@tool(
    "generate_resume_docx",
    "Generate a professional resume as a Word document",
    {"resume_json": str, "output_path": str}
)
async def generate_resume_docx(args: dict) -> dict:
    """Generate a resume document using python-docx."""
    resume_json, output_path = args["resume_json"], args["output_path"]
    resume = json.loads(resume_json)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    doc = Document()

    # Set margins (0.5 inches)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Header - Name
    header = resume.get("header", {})
    name_para = doc.add_paragraph()
    name_run = name_para.add_run(header.get("name", ""))
    name_run.bold = True
    name_run.font.size = Pt(24)
    name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Contact info
    contact = f"{header.get('email', '')} | {header.get('phone', '')} | {header.get('location', '')}"
    contact_para = doc.add_paragraph(contact)
    contact_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Summary
    doc.add_heading("Summary", level=1)
    doc.add_paragraph(resume.get("summary", ""))

    # Experience
    doc.add_heading("Experience", level=1)
    for job in resume.get("experience", []):
        job_para = doc.add_paragraph()
        title_run = job_para.add_run(f"{job.get('title', '')} - {job.get('company', '')}")
        title_run.bold = True
        doc.add_paragraph(job.get("duration", ""), style="Normal")
        for bullet in job.get("description", []):
            doc.add_paragraph(bullet, style="List Bullet")

    # Education
    doc.add_heading("Education", level=1)
    for edu in resume.get("education", []):
        doc.add_paragraph(f"{edu.get('degree', '')} - {edu.get('school', '')} ({edu.get('year', '')})")

    # Skills
    doc.add_heading("Skills", level=1)
    skills = ", ".join(resume.get("skills", []))
    doc.add_paragraph(skills)

    doc.save(output_path)

    return {
        "content": [{"type": "text", "text": f"Resume successfully saved to {output_path}"}]
    }


# =============================================================================
# Hook Definition
# =============================================================================

async def log_tool_use(
    input_data: dict[str, Any],
    tool_use_id: str | None,
    context: HookContext
) -> dict[str, Any]:
    """Log all tool usage before execution."""
    tool_name = input_data.get('tool_name', 'unknown')
    print(f"[HOOK] Executing: {tool_name}")
    return {}


# =============================================================================
# MCP Server Setup
# =============================================================================

resume_tools = create_sdk_mcp_server(
    name="resume_tools",
    version="1.0.0",
    tools=[web_search, get_linkedin_profile, analyze_resume_data, generate_resume_docx],
)


# =============================================================================
# Agent Runner
# =============================================================================

async def run_agent(args) -> None:
    """Run the resume generator agent."""
    output_path = args.output or f"{args.name.replace(' ', '_')}_Resume.docx"

    options = ClaudeAgentOptions(
        mcp_servers={"resume": resume_tools},
        allowed_tools=[
            "mcp__resume__web_search",
            "mcp__resume__get_linkedin_profile",
            "mcp__resume__analyze_resume_data",
            "mcp__resume__generate_resume_docx"
        ],
        hooks={
            'PreToolUse': [HookMatcher(hooks=[log_tool_use])]
        }
    )

    prompt = (
        f"Research {args.name} by searching the web and fetching their LinkedIn profile. "
        f"Then analyze the data and generate a professional resume document. "
        f"Save the resume to: {output_path}"
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)

        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        if args.verbose:
                            print(f"[ASSISTANT] {block.text}")
                    if isinstance(block, ToolUseBlock):
                        if args.verbose:
                            print(f"[TOOL] {block.name}: {block.input}")

            if isinstance(message, ResultMessage):
                if args.verbose:
                    print(f"[RESULT] {message.result}")

    print(f"\nResume saved to: {output_path}")


# =============================================================================
# CLI Configuration
# =============================================================================

cli = AgentCLI(
    name="Resume Generator",
    description="Generate professional resumes using Claude Agent SDK with custom MCP tools",
    arguments=[
        CLIArgument(
            name="name",
            help="Name of the person to generate resume for"
        ),
        CLIArgument(
            name="--output",
            short="-o",
            help="Output file path (default: {name}_Resume.docx)"
        ),
        CLIArgument(
            name="--verbose",
            short="-v",
            help="Show detailed output including assistant messages",
            action="store_true"
        ),
    ],
    epilog="""
Examples:
  python resume_generator.py "John Smith"
  python resume_generator.py "Jane Doe" -o ./output/jane_resume.docx
  python resume_generator.py "John Smith" --verbose

Available mock profiles: John Smith, Jane Doe, Alex Johnson
"""
)


if __name__ == "__main__":
    exit_code = run_agent_cli(cli, run_agent)
    sys.exit(exit_code)
