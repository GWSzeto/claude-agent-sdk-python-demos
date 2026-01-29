"""
Content Pipeline Agent - Iteration 2
Demonstrates prompt chaining with structured outputs.
"""

import json
import re
import asyncio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
    tool,
    create_sdk_mcp_server,
)
from pydantic import BaseModel

from mock_data import get_content_by_id


# =============================================================================
# Pydantic Models (Structured Output Schemas)
# =============================================================================

class ExtractResult(BaseModel):
    extracted_content: str
    original_length: int
    extracted_length: int
    title: str


class GateResult(BaseModel):
    passed: bool
    reason: str
    checks: dict[str, bool]


# =============================================================================
# Helper Functions
# =============================================================================

def strip_html(html_content: str) -> str:
    """Remove HTML tags and clean up content."""
    text = html_content

    # Remove script, style, nav, footer elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<header[^>]*>.*?</header>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&copy;', '(c)')

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# =============================================================================
# MCP Tools
# =============================================================================

@tool("extract_content", "Extracts and cleans raw HTML/text content", {"content_id": str})
async def extract_content(args: dict) -> dict:
    """Fetch content from mock data and clean it."""
    content_id = args.get("content_id", "")

    # Fetch from mock data
    content_data = get_content_by_id(content_id)
    if not content_data:
        return {
            "content": [{
                "type": "text",
                "text": json.dumps({"error": f"Content not found: {content_id}"})
            }]
        }

    raw_content = content_data["content"]
    content_format = content_data["format"]

    # Extract based on format
    if content_format == "html":
        extracted = strip_html(raw_content)
    else:
        # For text/markdown, just normalize whitespace
        extracted = re.sub(r'\s+', ' ', raw_content).strip()

    result = {
        "extracted_content": extracted,
        "original_length": len(raw_content),
        "extracted_length": len(extracted),
        "title": content_data.get("title", "Untitled")
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(result)
        }]
    }


@tool("extraction_gate", "Validate extracted content meets quality criteria", {
    "extracted_content": str,
    "original_length": int,
    "extracted_length": int
})
async def extraction_gate(args: dict) -> dict:
    """Validate extraction quality."""
    extracted_content = args.get("extracted_content", "")
    original_length = args.get("original_length", 0)
    extracted_length = args.get("extracted_length", 0)

    checks = {}
    all_passed = True

    # Check 1: Minimum length > 100
    min_length_ok = extracted_length > 100
    checks["min_length"] = min_length_ok
    if not min_length_ok:
        all_passed = False

    # Check 2: No HTML tags remaining
    has_html = bool(re.search(r'<[a-zA-Z][^>]*>', extracted_content))
    checks["no_html_tags"] = not has_html
    if has_html:
        all_passed = False

    # Check 3: Not empty/whitespace only
    has_substance = bool(extracted_content.strip())
    checks["has_substance"] = has_substance
    if not has_substance:
        all_passed = False

    # Build reason
    if all_passed:
        reason = "All quality checks passed"
    else:
        failed = [k for k, v in checks.items() if not v]
        reason = f"Failed checks: {', '.join(failed)}"

    result = {
        "passed": all_passed,
        "reason": reason,
        "checks": checks
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(result)
        }]
    }


# =============================================================================
# MCP Server Setup
# =============================================================================

content_tools = create_sdk_mcp_server(
    name="content-pipeline",
    version="1.0.0",
    tools=[extract_content, extraction_gate]
)


# =============================================================================
# Pipeline Runner
# =============================================================================

async def main(content_id: str):
    """
    Run the extract + gate pipeline.

    Flow:
    1. query() with extract_content tool -> ExtractResult
    2. query() with extraction_gate tool -> GateResult
    """
    print(f"\n[PIPELINE] Starting for {content_id}")

    # =========================================
    # STEP 1: Extract content
    # =========================================
    print("[STEP 1] Extracting content...")

    step1_result = None
    async for message in query(
        prompt=f"Use the extract_content tool to extract content from content_id='{content_id}'",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": ExtractResult.model_json_schema()
            },
            allowed_tools=["mcp__content-pipeline__extract_content"],
            mcp_servers={"content-tools": content_tools}
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            step1_result = ExtractResult.model_validate(message.structured_output)

    if not step1_result:
        print("[STEP 1] FAILED - No result")
        return {"success": False, "error": "Extraction failed"}

    print(f"[STEP 1] SUCCESS - Extracted {step1_result.extracted_length} chars from {step1_result.original_length}")
    print(f"[STEP 1] Title: {step1_result.title}")

    # =========================================
    # STEP 2: Validate extraction (Gate)
    # =========================================
    print("\n[STEP 2] Validating extraction quality...")

    step2_result = None
    async for message in query(
        prompt=f"""Use the extraction_gate tool to validate the extracted content.

Parameters:
- extracted_content: "{step1_result.extracted_content[:500]}..."
- original_length: {step1_result.original_length}
- extracted_length: {step1_result.extracted_length}""",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": GateResult.model_json_schema()
            },
            allowed_tools=["mcp__content-pipeline__extraction_gate"],
            mcp_servers={"content-tools": content_tools}
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            step2_result = GateResult.model_validate(message.structured_output)

    if not step2_result:
        print("[STEP 2] FAILED - No result")
        return {"success": False, "error": "Gate validation failed"}

    print(f"[STEP 2] {'PASSED' if step2_result.passed else 'FAILED'}")
    print(f"[STEP 2] Reason: {step2_result.reason}")
    print(f"[STEP 2] Checks: {step2_result.checks}")

    # =========================================
    # Return final result
    # =========================================
    if step2_result.passed:
        print("\n[PIPELINE] SUCCESS")
        return {
            "success": True,
            "title": step1_result.title,
            "extracted": step1_result.extracted_content,
            "length": step1_result.extracted_length
        }
    else:
        print("\n[PIPELINE] FAILED at extraction_gate")
        return {
            "success": False,
            "failed_at": "extraction_gate",
            "reason": step2_result.reason
        }


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    import sys
    content_id = sys.argv[1] if len(sys.argv) > 1 else "article-001"
    result = asyncio.run(main(content_id))

    if result["success"]:
        print(f"\n--- EXTRACTED CONTENT (first 300 chars) ---")
        print(result["extracted"][:300] + "...")
