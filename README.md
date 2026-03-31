# Deep Research for Claude Code

Deep research skill with source quality gates — every claim cited, every source classified, no hallucinated URLs.

A [Claude Code custom skill](https://docs.anthropic.com/en/docs/claude-code/skills) that launches parallel research agents, classifies sources by tier, enforces hard quality gates, and synthesizes structured reports with confidence labels.

## Quick Start

```bash
# Clone and install
git clone https://github.com/robertnowell/deep-research.git
cp -r deep-research ~/.claude/skills/deep-research
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

| Scope | Breadth agents | Depth phase | Verification | Best for |
|---|---|---|---|---|
| `quick` | 2 | Skipped | Skipped | Fast orientation on a topic |
| `standard` | 3 | 1-2 agents | Skipped | Most research questions |
| `thorough` | 5 | 2-3 agents | Yes | High-stakes decisions, publishing |

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
- **Emerging** — Single Tier 2/3 source, no contradiction
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

| | Raw WebSearch | 199-bio skill | Imbad0202 academic | **This skill** |
|---|---|---|---|---|
| Parallel agents | No | Yes | Yes (13) | Yes (2-5) |
| Source classification | None | Opaque 0-100 score | Academic-focused | 4-tier transparent system |
| Quality gates | None | None enforced | PRISMA-style | 5 hard gates |
| Confidence labels | None | None | None | 5 levels |
| Scope scaling | N/A | One size | One size | quick / standard / thorough |
| Codebase-aware | No | No | No | Yes |
| Failed angle disclosure | N/A | No | No | Required |
| License | N/A | MIT | CC-BY-NC | MIT |

## Codebase-Aware Research

If your research question relates to your local project, the skill automatically spawns an Explore agent to search your codebase alongside the web research — connecting external findings to your actual code, config, and architecture.

## Example Output

See [examples/sample-output.md](examples/sample-output.md) for a full research report demonstrating source tiers, confidence labels, and quality gates in action.

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
    └── sample-output.md          # Example research output
```

## License

MIT — see [LICENSE](LICENSE).
