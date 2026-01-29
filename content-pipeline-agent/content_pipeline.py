"""
Content Pipeline Agent - Iteration 3
Demonstrates two-stage prompt chaining: Extract → Summarize with gates.

Pattern: Python handles data, LLM returns structured responses.
No MCP tools needed - just structured outputs.
"""

import re
import asyncio
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
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


class SummarizeResult(BaseModel):
    summary: str
    key_points: list[str]
    original_length: int
    summary_length: int


# =============================================================================
# Helper Functions (Python does the data work)
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


def fetch_and_clean_content(content_id: str) -> dict | None:
    """Fetch content from mock data and clean it (Python function, not LLM)."""
    content_data = get_content_by_id(content_id)
    if not content_data:
        return None

    raw_content = content_data["content"]
    content_format = content_data["format"]

    # Extract based on format
    if content_format == "html":
        extracted = strip_html(raw_content)
    else:
        extracted = re.sub(r'\s+', ' ', raw_content).strip()

    return {
        "extracted_content": extracted,
        "original_length": len(raw_content),
        "extracted_length": len(extracted),
        "title": content_data.get("title", "Untitled"),
        "format": content_format
    }


def validate_extraction(extracted_content: str, original_length: int, extracted_length: int) -> GateResult:
    """Validate extraction quality (Python function, not LLM)."""
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

    if all_passed:
        reason = "All quality checks passed"
    else:
        failed = [k for k, v in checks.items() if not v]
        reason = f"Failed checks: {', '.join(failed)}"

    return GateResult(passed=all_passed, reason=reason, checks=checks)


def validate_summary(summary: str, key_points: list[str], original_length: int, summary_length: int) -> GateResult:
    """Validate summary quality (Python function, not LLM)."""
    checks = {}
    all_passed = True

    # Check 1: Has enough key points (at least 3)
    has_points = len(key_points) >= 3
    checks["has_key_points"] = has_points
    if not has_points:
        all_passed = False

    # Check 2: Reasonable compression (summary < 40% of original)
    if original_length > 0:
        ratio = summary_length / original_length
        good_compression = ratio < 0.4
        checks["good_compression"] = good_compression
        if not good_compression:
            all_passed = False

    # Check 3: Summary has substance (> 50 chars)
    has_content = len(summary.strip()) > 50
    checks["has_content"] = has_content
    if not has_content:
        all_passed = False

    if all_passed:
        reason = "All summary checks passed"
    else:
        failed = [k for k, v in checks.items() if not v]
        reason = f"Failed checks: {', '.join(failed)}"

    return GateResult(passed=all_passed, reason=reason, checks=checks)


# =============================================================================
# Pipeline Step Functions (LLM calls with structured outputs)
# =============================================================================

async def run_extract(content_id: str) -> ExtractResult | None:
    """
    Step 1: Extract content.
    - Python fetches and cleans the data
    - LLM confirms/returns the structured result
    """
    # Python does the data work
    data = fetch_and_clean_content(content_id)
    if not data:
        return None

    # LLM returns structured response - consume full iterator
    result = None
    async for message in query(
        prompt=f"""I have extracted content from a document. Please return it in the structured format.

Title: {data['title']}
Original length: {data['original_length']} characters
Extracted length: {data['extracted_length']} characters
Extracted content:
{data['extracted_content'][:3000]}""",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": ExtractResult.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            result = ExtractResult.model_validate(message.structured_output)
    return result


async def run_summarize(content: str, style: str = "bullets", max_points: int = 5) -> SummarizeResult | None:
    """
    Step 3: Summarize content.
    - LLM does the summarization and returns structured result
    """
    # Consume full iterator to avoid early exit issues
    result = None
    async for message in query(
        prompt=f"""Summarize the following content into key points.

Style: {style}
Maximum key points: {max_points}

Content to summarize:
{content[:3000]}

Provide a concise summary and extract the key points.""",
        options=ClaudeAgentOptions(
            output_format={
                "type": "json_schema",
                "schema": SummarizeResult.model_json_schema()
            }
        )
    ):
        if isinstance(message, ResultMessage) and message.structured_output:
            result = SummarizeResult.model_validate(message.structured_output)
    return result


# =============================================================================
# Pipeline Runner
# =============================================================================

async def main(content_id: str):
    """
    Run the two-stage pipeline: Extract → Summarize with gates.

    Flow:
    1. Python fetches/cleans data, LLM returns ExtractResult
    2. Python validates extraction (gate)
    3. LLM summarizes, returns SummarizeResult
    4. Python validates summary (gate)
    """
    print(f"\n[PIPELINE] Starting for {content_id}")

    # =========================================
    # STEP 1: Extract content
    # =========================================
    print("[STEP 1] Extracting content...")
    step1_result = await run_extract(content_id)

    if not step1_result:
        print("[STEP 1] FAILED - No result")
        return {"success": False, "error": "Extraction failed"}

    print(f"[STEP 1] SUCCESS - Extracted {step1_result.extracted_length} chars from {step1_result.original_length}")
    print(f"[STEP 1] Title: {step1_result.title}")

    # =========================================
    # STEP 2: Validate extraction (Gate - Python)
    # =========================================
    print("\n[STEP 2] Validating extraction quality...")
    step2_result = validate_extraction(
        step1_result.extracted_content,
        step1_result.original_length,
        step1_result.extracted_length
    )

    print(f"[STEP 2] {'PASSED' if step2_result.passed else 'FAILED'}")
    print(f"[STEP 2] Reason: {step2_result.reason}")
    print(f"[STEP 2] Checks: {step2_result.checks}")

    if not step2_result.passed:
        print("\n[PIPELINE] FAILED at extraction_gate")
        return {"success": False, "failed_at": "extraction_gate", "reason": step2_result.reason}

    # =========================================
    # STEP 3: Summarize content (LLM)
    # =========================================
    print("\n[STEP 3] Summarizing content...")
    step3_result = await run_summarize(step1_result.extracted_content)

    if not step3_result:
        print("[STEP 3] FAILED - No result")
        return {"success": False, "error": "Summarization failed"}

    print(f"[STEP 3] SUCCESS - Summary: {step3_result.summary_length} chars, {len(step3_result.key_points)} key points")

    # =========================================
    # STEP 4: Validate summary (Gate - Python)
    # =========================================
    print("\n[STEP 4] Validating summary quality...")
    step4_result = validate_summary(
        step3_result.summary,
        step3_result.key_points,
        step3_result.original_length,
        step3_result.summary_length
    )

    print(f"[STEP 4] {'PASSED' if step4_result.passed else 'FAILED'}")
    print(f"[STEP 4] Reason: {step4_result.reason}")
    print(f"[STEP 4] Checks: {step4_result.checks}")

    # =========================================
    # Return final result
    # =========================================
    if step4_result.passed:
        print("\n[PIPELINE] SUCCESS")
        return {
            "success": True,
            "title": step1_result.title,
            "summary": step3_result.summary,
            "key_points": step3_result.key_points
        }
    else:
        print("\n[PIPELINE] FAILED at summary_gate")
        return {
            "success": False,
            "failed_at": "summary_gate",
            "reason": step4_result.reason
        }


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    import sys
    content_id = sys.argv[1] if len(sys.argv) > 1 else "article-001"
    result = asyncio.run(main(content_id))

    if result["success"]:
        print(f"\n--- SUMMARY ---")
        print(result["summary"])
        print(f"\n--- KEY POINTS ---")
        for i, point in enumerate(result["key_points"], 1):
            print(f"{i}. {point}")
