# Task Breakdown Agent

Takes a high-level goal and breaks it down into actionable tasks across multiple work streams.

## What It Does

- Analyze a goal and identify relevant work streams (technical, testing, docs, operations)
- Dispatch specialized workers to generate tasks for each stream
- Synthesize worker outputs into a unified, ordered plan
- Identify cross-stream dependencies

## Techniques Used

- **Orchestrator-Workers** - Central orchestrator dynamically delegates to specialized worker subagents
- **Subagents** - Worker agents defined with `AgentDefinition`, each focused on one work stream
- **Structured Outputs** - Pydantic schemas for orchestrator decisions
- **Dynamic Task Decomposition** - Work streams determined by context, not hardcoded
