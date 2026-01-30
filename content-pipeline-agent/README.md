# Content Pipeline Agent

Transforms raw content through a multi-stage pipeline that extracts, validates, and summarizes information.

## What It Does

- Extract main content from documents (removes ads, navigation, footers)
- Validate extraction quality with gates
- Summarize content into key points
- Support different summary styles (bullets, executive)

## Techniques Used

- **Prompt Chaining** - Sequential `query()` calls where each step processes the output of the previous one
- **Structured Outputs** - Pydantic schemas with `output_format` for validated JSON responses
- **Gates** - Quality checks between pipeline stages that can halt processing on failure
- **Skills** - Best practices for content extraction and summarization
