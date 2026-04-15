# Synthesis Patterns

How to consolidate multi-agent research findings into a coherent report.

## Grouping Rules

- Organize by **conceptual theme**, not by source or by agent
- Each theme section should cross-reference findings from multiple agents
- Never present "Agent 1 found X, Agent 2 found Y" — interleave findings by topic
- If two agents found the same fact independently, that's corroboration — note it
- If an agent found nothing useful for a theme, don't mention the agent

## Contradiction Resolution

When sources disagree, resolve in this priority order:

1. **Source tier**: Tier 1 wins over Tier 3 (see source-evaluation.md for tier definitions)
2. **Specificity**: Quantified claim with methodology wins over vague assertion
3. **Recency**: For technology and current-state questions, newer wins. For historical questions, contemporaneous sources win.
4. **Independence**: A claim supported by sources that don't cite each other is stronger than multiple sources tracing to one origin

If still contested after applying these rules:
- Present both positions with their respective tier annotations
- Label confidence as **Contested**
- Note what evidence would resolve the disagreement

Always report the resolution AND the disagreement. Don't silently drop the losing side.

## Confidence Labels

Apply to each Key Finding based on source evidence:

- **Established**: 2+ independent Tier 1/2 sources agree
- **Likely**: 1 Tier 1/2 source, or 2+ Tier 3 sources corroborate
- **Emerging**: Single Tier 2/3 source, no contradiction found
- **Contested**: Tier 1/2 sources disagree with each other
- **Speculative**: Only Tier 3/4 sources, or single uncorroborated claim

## Output Templates

### Quick Scope

```
## Executive Summary
[2-3 sentences directly answering the research question. State whether the question is fully answered, partially answered, or unanswerable with available evidence.]

## Key Findings
1. **[Finding]** — Confidence: [label]
   [1 sentence with source reference]
2. ...

## Sources
1. [Title](URL) — [Tier N] [what it contributed]
2. ...
```

### Standard Scope

```
## Executive Summary
[3-5 sentences directly answering the research question. State answer status.]

## Key Findings
1. **[Finding]** — Confidence: [label]
   [1-2 sentence supporting detail with source reference]
2. ...

## Detailed Analysis

### [Theme 1]
[Cross-reference multiple sources. Note where sources agree and disagree. Include tier annotations on claims.]

### [Theme 2]
...

## Sources
1. [Title](URL) — [Tier N] [what it contributed]
2. ...

## Research Gaps
- [What could not be determined, and why]
- [Suggested next steps or sources to check]
```

### Thorough Scope

Standard template, plus:

```
## Source Verification Results
| Claim | Source | Verdict | Key Quote |
|---|---|---|---|
| [claim] | [URL] | SUPPORTED/PARTIALLY/NOT_SUPPORTED/UNAVAILABLE | "..." |

## Methodology
- Research angles investigated: [list]
- Agents dispatched: [count] breadth, [count] depth, [count] verification
- Leads followed from breadth phase: [list]
- Angles that returned NO_USEFUL_FINDINGS: [list or "none"]
```
