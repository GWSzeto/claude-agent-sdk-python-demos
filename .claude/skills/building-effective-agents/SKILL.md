---
name: building-effective-agents
description: Patterns and best practices for building effective AI agents from Anthropic's research. Use when designing agent architectures, choosing between workflows, implementing tool interfaces, or deciding complexity levels.
---

# Building Effective Agents

Reference guide based on Anthropic's research on building effective AI agents.

## Core Philosophy

**Start Simple**: Find the simplest solution possible. Only increase complexity when demonstrably improving outcomes. Agentic systems trade latency and cost for improved task performance—this tradeoff must be justified.

**When to Use Agents**: Agents suit open-ended problems where you cannot predict required steps or hardcode fixed paths. For many applications, optimizing single LLM calls with retrieval and in-context examples suffices.

## The Augmented LLM Foundation

The foundation of any agent combines an LLM with three capabilities:

```
┌─────────────────────────────────────┐
│           Augmented LLM             │
│  ┌─────────┐ ┌───────┐ ┌────────┐  │
│  │Retrieval│ │ Tools │ │ Memory │  │
│  └─────────┘ └───────┘ └────────┘  │
└─────────────────────────────────────┘
```

- **Retrieval**: Search queries, document lookup
- **Tools**: External actions, API calls
- **Memory**: Context retention across interactions

## Five Key Workflow Patterns

### 1. Prompt Chaining

Decompose tasks into sequential steps where each LLM call processes prior output.

```
Input → LLM₁ → Check → LLM₂ → Check → LLM₃ → Output
```

**When to use**: Fixed subtasks where breaking them up increases accuracy.

**Example**: Document translation → Grammar check → Format verification

### 2. Routing

Classify inputs and direct them to specialized handlers.

```
         ┌→ Handler A (specialized prompt)
Input → Router
         └→ Handler B (specialized prompt)
```

**When to use**: Different input types require different handling. Prevents one category from degrading performance on others.

**Example**: Customer query → Technical support OR Billing OR General inquiry

### 3. Parallelization

Run LLM calls simultaneously for speed or confidence.

**Sectioning**: Independent subtasks run in parallel
```
        ┌→ Subtask A ─┐
Input ──┼→ Subtask B ─┼→ Combine → Output
        └→ Subtask C ─┘
```

**Voting**: Multiple attempts at same task for higher confidence
```
        ┌→ Attempt 1 ─┐
Input ──┼→ Attempt 2 ─┼→ Vote → Output
        └→ Attempt 3 ─┘
```

**When to use**: Need speed improvements or higher confidence through diverse perspectives.

### 4. Orchestrator-Workers

Central LLM dynamically breaks down tasks, delegates to workers, synthesizes results.

```
                    ┌→ Worker A ─┐
Input → Orchestrator┼→ Worker B ─┼→ Orchestrator → Output
                    └→ Worker C ─┘
```

**When to use**: Complex tasks where subtasks aren't predefined but determined by context. Ideal for coding agents handling unpredictable changes.

**Key difference from parallelization**: Subtasks are dynamically determined, not predefined.

### 5. Evaluator-Optimizer

Loop between generation and evaluation for iterative refinement.

```
Input → Generator → Evaluator → (feedback) → Generator → ... → Output
```

**When to use**: Clear evaluation criteria exist and measurable refinement adds value.

**Example**: Code generation → Test execution → Fix based on errors → Re-test

## Autonomous Agents

Agents operate in a loop: receive command → take actions → get feedback → continue.

```python
while not task_complete:
    action = llm.decide_action(context, feedback)
    result = execute_tool(action)
    feedback = evaluate_result(result)
    context = update_context(context, result, feedback)
```

**Implementation is often straightforward**: Just LLMs using tools in a loop based on environmental feedback.

**Risks**: Higher costs and error compounding. Requires extensive sandboxed testing and guardrails.

## Tool Design Principles (ACI)

Invest in Agent-Computer Interface (ACI) design as thoroughly as human-computer interface design. Tool design deserves equal attention to overall prompts.

### Format Selection
- Choose formats close to natural internet text
- Avoid unnecessary overhead (tracking line counts, string escaping)
- Give models space to "think" before committing to output

### Poka-Yoke Design (Error-Proofing)
Make mistakes harder through argument design:
- **Good**: Require absolute filepaths instead of relative ones
- **Good**: Use structured parameters instead of free-form strings
- **Good**: Validate inputs before execution

### Documentation
For each tool, include:
- Usage examples
- Edge cases
- Input format requirements
- Clear boundaries between tools

## Three Core Principles

| Principle | Application |
|-----------|-------------|
| **Simplicity** | Design agents with minimal complexity. Add only what's needed. |
| **Transparency** | Explicitly show planning steps. Make agent reasoning visible. |
| **Documentation & Testing** | Thoroughly craft and test the agent-computer interface. |

## Complexity Decision Framework

Ask these questions before adding complexity:

1. **Can a single LLM call with good prompting solve this?**
   → If yes, don't add agents.

2. **Are the steps predictable and fixed?**
   → If yes, use Prompt Chaining.

3. **Do different inputs need different handling?**
   → If yes, use Routing.

4. **Can subtasks run independently?**
   → If yes, use Parallelization.

5. **Are subtasks unpredictable and context-dependent?**
   → If yes, use Orchestrator-Workers.

6. **Does output need iterative refinement with clear criteria?**
   → If yes, use Evaluator-Optimizer.

7. **Is the problem truly open-ended with unpredictable paths?**
   → Only then use Autonomous Agents.

## When Agents Excel

Agents work best when:
- Solutions are verifiable (automated tests, clear criteria)
- Agents can iterate using feedback
- Problem space is well-defined
- Output quality is objectively measurable

**Example**: Coding agents shine because code can be tested, errors provide feedback, and results are verifiable.

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Over-engineering | Start simple, add complexity only when proven needed |
| Poor tool design | Invest as much in ACI as in prompts |
| Hidden reasoning | Make planning steps explicit and visible |
| No guardrails | Sandbox testing, human checkpoints for critical actions |
| Ignoring costs | Measure latency/cost vs. performance tradeoffs |

## Measurement Mindset

Success means building the right system for your needs, not the most sophisticated one. Always:
- Measure performance
- Iterate relentlessly
- Justify every added complexity
