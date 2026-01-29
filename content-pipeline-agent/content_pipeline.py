"""
Content Pipeline Agent - Iteration 5
Demonstrates two-stage prompt chaining: Extract → Summarize with gates.

Pattern: Python handles data, LLM returns structured responses.
Skills integration for best practices guidance.
CLI interface with error handling.
"""

import re
import asyncio
import argparse
from pathlib import Path
from typing import TypeVar, Type
from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
)
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

from mock_data import get_content_by_id

# Project directory for skill loading
PROJECT_DIR = str(Path(__file__).parent.resolve())


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
# Generic Stage Runner with Error Handling
# =============================================================================

async def run_stage_safe(
    prompt: str,
    schema_class: Type[T],
    stage_name: str,
    verbose: bool = False
) -> tuple[T | None, str | None]:
    """Run a pipeline stage with error handling.

    Returns:
        Tuple of (result, error). If successful, error is None.
        If failed, result is None and error contains the message.
    """
    try:
        if verbose:
            print(f"[{stage_name}] Starting...")

        result = None
        error = None

        # Must consume full iterator to avoid async generator cleanup issues
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=PROJECT_DIR,
                setting_sources=["user", "project"],
                allowed_tools=["Skill"],
                output_format={
                    "type": "json_schema",
                    "schema": schema_class.model_json_schema()
                }
            )
        ):
            if isinstance(message, ResultMessage):
                if message.structured_output:
                    result = schema_class.model_validate(message.structured_output)
                    if verbose:
                        print(f"[{stage_name}] Success")
                elif message.subtype == "error_max_structured_output_retries":
                    error = f"{stage_name}: Could not produce valid output after retries"

        # Return after loop completes
        if error:
            return None, error
        if result:
            return result, None
        return None, f"{stage_name}: No result received"

    except Exception as e:
        return None, f"{stage_name}: {str(e)}"


# =============================================================================
# Pipeline Step Functions (LLM calls with structured outputs)
# =============================================================================

async def run_extract(content_id: str, verbose: bool = False) -> tuple[ExtractResult | None, str | None]:
    """
    Step 1: Extract content.
    - Python fetches and cleans the data
    - LLM confirms/returns the structured result

    Returns:
        Tuple of (ExtractResult, error). If successful, error is None.
    """
    # Python does the data work
    data = fetch_and_clean_content(content_id)
    if not data:
        return None, f"Content not found: {content_id}"

    prompt = f"""I have extracted content from a document. Please return it in the structured format.

Title: {data['title']}
Original length: {data['original_length']} characters
Extracted length: {data['extracted_length']} characters
Extracted content:
{data['extracted_content'][:3000]}"""

    return await run_stage_safe(prompt, ExtractResult, "EXTRACT", verbose)


async def run_summarize(
    content: str,
    style: str = "bullets",
    max_points: int = 5,
    verbose: bool = False
) -> tuple[SummarizeResult | None, str | None]:
    """
    Step 3: Summarize content.
    - LLM does the summarization and returns structured result

    Returns:
        Tuple of (SummarizeResult, error). If successful, error is None.
    """
    prompt = f"""Summarize the following content into key points.

Style: {style}
Maximum key points: {max_points}

Content to summarize:
{content[:3000]}

Provide a concise summary and extract the key points."""

    return await run_stage_safe(prompt, SummarizeResult, "SUMMARIZE", verbose)


# =============================================================================
# Pipeline Runner
# =============================================================================

async def run_pipeline(
    content_id: str,
    style: str = "bullets",
    max_points: int = 5,
    verbose: bool = False
) -> dict:
    """
    Run the two-stage pipeline: Extract → Summarize with gates.

    Args:
        content_id: ID of content to process
        style: Summary style (bullets, executive)
        max_points: Maximum number of key points
        verbose: Show detailed output

    Flow:
    1. Python fetches/cleans data, LLM returns ExtractResult
    2. Python validates extraction (gate)
    3. LLM summarizes, returns SummarizeResult
    4. Python validates summary (gate)
    """
    if verbose:
        print(f"\n[PIPELINE] Starting for {content_id}")

    # =========================================
    # STEP 1: Extract content
    # =========================================
    step1_result, error = await run_extract(content_id, verbose)

    if error:
        if verbose:
            print(f"[EXTRACT] FAILED - {error}")
        return {"success": False, "error": error}

    if verbose:
        print(f"[EXTRACT] SUCCESS - Extracted {step1_result.extracted_length} chars from {step1_result.original_length}")
        print(f"[EXTRACT] Title: {step1_result.title}")

    # =========================================
    # STEP 2: Validate extraction (Gate - Python)
    # =========================================
    step2_result = validate_extraction(
        step1_result.extracted_content,
        step1_result.original_length,
        step1_result.extracted_length
    )

    if verbose:
        print(f"\n[GATE] Extraction: {'PASSED' if step2_result.passed else 'FAILED'}")
        print(f"[GATE] Reason: {step2_result.reason}")
        print(f"[GATE] Checks: {step2_result.checks}")

    if not step2_result.passed:
        return {"success": False, "failed_at": "extraction_gate", "reason": step2_result.reason}

    # =========================================
    # STEP 3: Summarize content (LLM)
    # =========================================
    step3_result, error = await run_summarize(
        step1_result.extracted_content,
        style=style,
        max_points=max_points,
        verbose=verbose
    )

    if error:
        if verbose:
            print(f"[SUMMARIZE] FAILED - {error}")
        return {"success": False, "error": error}

    if verbose:
        print(f"[SUMMARIZE] SUCCESS - {step3_result.summary_length} chars, {len(step3_result.key_points)} key points")

    # =========================================
    # STEP 4: Validate summary (Gate - Python)
    # =========================================
    step4_result = validate_summary(
        step3_result.summary,
        step3_result.key_points,
        step3_result.original_length,
        step3_result.summary_length
    )

    if verbose:
        print(f"\n[GATE] Summary: {'PASSED' if step4_result.passed else 'FAILED'}")
        print(f"[GATE] Reason: {step4_result.reason}")
        print(f"[GATE] Checks: {step4_result.checks}")

    # =========================================
    # Return final result
    # =========================================
    if step4_result.passed:
        if verbose:
            print("\n[PIPELINE] SUCCESS")
        return {
            "success": True,
            "title": step1_result.title,
            "summary": step3_result.summary,
            "key_points": step3_result.key_points
        }
    else:
        return {
            "success": False,
            "failed_at": "summary_gate",
            "reason": step4_result.reason
        }


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """CLI entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Content Pipeline Agent - Extract and summarize content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python content_pipeline.py -i article-001
  python content_pipeline.py -i article-002 --style executive --max-points 3
  python content_pipeline.py -i article-001 -v
        """
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Content ID to process (e.g., article-001)"
    )
    parser.add_argument(
        "--style",
        default="bullets",
        choices=["bullets", "executive"],
        help="Summary style (default: bullets)"
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=5,
        help="Maximum number of key points (default: 5)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed pipeline output"
    )

    args = parser.parse_args()

    result = asyncio.run(run_pipeline(
        args.input,
        style=args.style,
        max_points=args.max_points,
        verbose=args.verbose
    ))

    if result["success"]:
        print(f"\n--- {result['title']} ---")
        print(result["summary"])
        print("\nKey Points:")
        for i, point in enumerate(result["key_points"], 1):
            print(f"  {i}. {point}")
    else:
        error = result.get("error") or result.get("reason")
        failed_at = result.get("failed_at", "unknown")
        print(f"\nPipeline failed at: {failed_at}")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
