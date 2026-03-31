[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/robertnowell/deep-research)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude_Code-Skill-blueviolet)](https://docs.anthropic.com/en/docs/claude-code/skills)

# Deep Research for Claude Code

Deep research with source quality gates — every claim cited, every source classified, no hallucinated URLs.

> Built for engineers and decision-makers, not academia. Optimized for speed and source transparency over exhaustive rigor. Get a trustworthy answer in minutes, not a 50-page paper.

## Quick Start

```bash
git clone https://github.com/robertnowell/deep-research.git ~/.claude/skills/deep-research
```

Then in Claude Code:

```
/deep-research what are the tradeoffs between SQLite and PostgreSQL for new web apps?
```

## What It Does

A 5-phase research pipeline that runs in your Claude Code session:

| Phase | What happens | Agents |
|---|---|---|
| **Analyze** | Breaks topic into 3-5 research angles | Main context |
| **Breadth** | Parallel web research per angle | 2-5 Sonnet agents |
| **Depth** | Fills gaps, verifies contradictions | 1-3 Sonnet agents |
| **Verify** | Fact-checks single-source claims | Haiku agents (thorough only) |
| **Synthesize** | Confidence-labeled structured report | Main context |

### Scope Modes

Control depth vs. speed with a single keyword:

| Scope | Breadth agents | Depth phase | Verification | Typical duration | Best for |
|---|---|---|---|---|---|
| `quick` | 2 | Skipped | Skipped | ~2 min | Fast orientation on a topic |
| `standard` | 3 | 1-2 agents | Skipped | ~5 min | Most research questions |
| `thorough` | 5 | 2-3 agents | Yes | ~10 min | High-stakes decisions, publishing |

```
/deep-research quick what is WebTransport?
/deep-research thorough should we migrate from Redis to Valkey?
```

## Source Quality System

Every source is classified into four tiers. Every finding must cite at least one.

| Tier | Label | Examples |
|---|---|---|
| **Tier 1** | Primary | Official docs, specs, peer-reviewed papers, author's own repo |
| **Tier 2** | Curated secondary | Major publications, MDN, Wikipedia (w/ citations), analyst reports |
| **Tier 3** | Community | Blog posts, Stack Overflow, forums, tutorials, newsletters |
| **Tier 4** | Unverifiable | Social media, AI-generated content, SEO listicles, content farms |

### Confidence Labels

Each key finding gets a confidence label based on source evidence:

- **Established** — 2+ independent Tier 1/2 sources agree
- **Likely** — 1 Tier 1/2 source, or 2+ Tier 3 sources corroborate
- **Emerging** — Single Tier 2/3 source, no contradiction found
- **Contested** — Tier 1/2 sources disagree with each other
- **Speculative** — Only Tier 3/4 sources, or single uncorroborated claim

### Hard Quality Gates

Five enforced gates that must pass before the report is shown:

1. **Citation requirement** — Every finding must cite ≥1 source with a tier annotation
2. **No fabricated URLs** — Every URL must trace back to an agent's actual output
3. **Question answered** — Executive summary must state whether the question is fully answered, partially answered, or unanswerable
4. **Source quality caveat** — Auto-prepended if >50% of sources are Tier 3/4
5. **Failed angles disclosed** — No silently dropped research angles

## How It Compares

| | Raw WebSearch | [199-bio](https://github.com/199-biotechnologies/claude-deep-research-skill) | [Imbad0202](https://github.com/Imbad0202/academic-research-skills) | **This skill** |
|---|---|---|---|---|
| Parallel agents | No | Yes | Yes (13) | Yes (2-5) |
| Source classification | None | Opaque 0-100 score | Academic-focused | 4-tier transparent system |
| Quality gates | None | None enforced | PRISMA-style | 5 hard gates |
| Confidence labels | None | None | None | 5 levels |
| Scope scaling | N/A | 4 modes | 7 modes | 3 scopes (quick/standard/thorough) |
| Codebase-aware | No | No | No | Yes |
| Failed angle disclosure | N/A | No | No | Required |
| Target audience | — | General | Academic | Engineers and decision-makers |
| License | N/A | MIT | CC-BY-NC | MIT |

## Codebase-Aware Research

If your research question relates to your local project, the skill automatically spawns an Explore agent to search your codebase alongside the web research — connecting external findings to your actual code, config, and architecture.

## Example Output

<details>
<summary>Sample report: Deep research tools in Claude Code (standard scope)</summary>

See [examples/sample-output.md](examples/sample-output.md) for the full report demonstrating source tiers, confidence labels, research gaps, and quality gates in action.

**Preview of key findings:**

| Finding | Confidence | Sources |
|---|---|---|
| Claude Code ships with capable research tools but has deliberate constraints | Established | Tier 1, Tier 2 |
| The parallel subagent pattern is the foundation of every serious research approach | Established | Tier 1 |
| Community research skills are the fastest path from zero to structured research | Likely | Tier 1, Tier 2 |
| MCP search servers have serious subagent compatibility bugs | Established | Tier 1 |
| MCP tool definitions consume 385 to 17,000+ context tokens per server | Likely | Tier 3 |
| Anthropic frames MCP and Skills as complementary: "MCP = access, Skills = expertise" | Established | Tier 1 |

</details>

<details>
<summary>Sample report: Inventive uses of deep research (standard scope)</summary>

See [examples/inventive-uses.md](examples/inventive-uses.md) for a report on creative, unexpected applications — M&A due diligence, investigative journalism, OSINT, security research, and research-to-action pipelines.

**Preview of key findings:**

| Finding | Confidence | Sources |
|---|---|---|
| The most inventive pattern is research → automated action, not research → report | Likely | Tier 2, Tier 3 |
| M&A due diligence compresses 6-week timelines to 2 weeks | Established | Tier 1, Tier 2 |
| Claude Code Security found 500+ undetected vulnerabilities via reasoning-based research | Established | Tier 1, Tier 2 |
| Investigative journalism workflows replicate published investigations in under an hour | Likely | Tier 3 |
| Scientific research: genome study compressed from months to 20 minutes | Established | Tier 1 |
| Self-improvement systems cross-reference journal entries with Git commits | Emerging | Tier 2 |

</details>

## File Structure

```
deep-research/
├── SKILL.md                      # Skill definition (the pipeline)
├── README.md                     # This file
├── LICENSE                       # MIT
├── references/
│   ├── source-evaluation.md      # Source tier definitions and red flags
│   └── synthesis-patterns.md     # Report templates and synthesis rules
└── examples/
    ├── sample-output.md          # Example: deep research tools comparison
    └── inventive-uses.md         # Example: creative and unexpected applications
```

## License

MIT — see [LICENSE](LICENSE).
