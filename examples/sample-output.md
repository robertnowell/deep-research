# Deep Research with Claude Code in 2026: Tools, Skills, and Approaches

> This is an example output from `/deep-research standard` demonstrating source tiers, confidence labels, and quality gates.

---

**Scope**: standard (3 breadth agents, 2 depth agents)

**Research angles**:
1. Claude Code's built-in research capabilities
2. Community skills and slash commands for deep research
3. MCP search servers and DIY approaches
4. (Depth) Decision framework by user profile
5. (Depth) MCP practical tradeoffs and subagent limitations

---

## Executive Summary

This question is **fully answered**. There are four distinct approaches to deep research with Claude Code — built-in tools, community skills, MCP search servers, and DIY pipelines — and the right choice depends on your use case, budget, and technical comfort. Claude Code's built-in `WebSearch` + `WebFetch` handle most daily research needs with zero setup. Community skills like academic-research-skills (1,654 stars) and claude-deep-research-skill (371 stars) add structured methodology and source verification on top of built-in tools. MCP search servers (Tavily, Perplexity, Exa) provide richer search results but have significant subagent compatibility bugs as of March 2026. DIY recursive pipelines offer maximum flexibility at the highest cost ($1–5 per deep query). For most users, a community skill using built-in web tools is the best starting point — it adds research rigor without API keys, billing, or setup friction.

## Key Findings

1. **Claude Code ships with capable research tools out of the box, but they have deliberate constraints.** — Confidence: **Established**
   WebSearch returns only titles and URLs (no page content); WebFetch retrieves pages through a Haiku intermediary with 100KB truncation and a 125-character quote cap. WebFetch can only access URLs already in the conversation — it cannot independently discover new pages. WebSearch costs $10 per 1,000 searches; WebFetch is free beyond token costs. These tools cover daily lookups but are insufficient for multi-source synthesis without additional orchestration. [Tier 1: Claude Code Tools Reference, Claude API Docs; Tier 2: Mikhail Shilkov analysis]

2. **The parallel subagent pattern is the foundation of every serious research approach.** — Confidence: **Established**
   Claude Code's `Agent` tool spawns multiple subagents simultaneously, each with its own context window. All community skills and DIY pipelines use this pattern — decompose a question into angles, research each in parallel, then synthesize. Subagents cannot spawn other subagents (one level deep only). Anthropic's official Agent SDK demo uses this exact orchestrator-worker architecture. [Tier 1: Claude Code Subagents Docs, Anthropic Agent SDK Demos]

3. **Community research skills are the fastest path from zero to structured research.** — Confidence: **Likely**
   Two skills dominate: Imbad0202/academic-research-skills (1,654 stars, CC-BY-NC, 13-agent team with PRISMA systematic review) for academic writing, and 199-biotechnologies/claude-deep-research-skill (371 stars, MIT, 8-phase pipeline with source credibility scoring) for general research. Both install with a single `git clone` and require no API keys. The Agent Skills open standard means these skills also work with Codex CLI, OpenCode, and Gemini CLI. [Tier 1: Primary GitHub repos; Tier 2: awesome-claude-code listing]

4. **Academic and general-purpose research are distinct niches with different leaders.** — Confidence: **Likely**
   Imbad0202's academic skill covers research-to-publication: literature search, PRISMA systematic reviews, predatory journal detection, LaTeX output (APA 7.0, IEEE, Chicago), and style calibration. A full pipeline run exceeds 200K input tokens (~$3+). For general-purpose research (competitive analysis, tech evaluation, market research), 199-biotechnologies offers four speed modes (Quick 2–5 min through UltraDeep 20–45 min) and multi-persona red teaming. Neither adequately serves the other's niche. [Tier 1: Primary repos with feature lists and version histories]

5. **MCP search servers provide richer results than built-in WebSearch but have serious subagent compatibility bugs.** — Confidence: **Established**
   Tavily (4 tools: search, extract, map, crawl; 1,000 free credits/month), Perplexity (4 tools including deep-research mode; $5/1K requests), and Exa (neural/semantic search; free tier) all exceed WebSearch capabilities. However, multiple open GitHub issues (#7296, #13898, #14496) confirm MCP tools do not reliably work inside Claude Code subagents. Custom subagents hallucinate results instead of erroring. Background/async subagents cannot access MCP tools at all. [Tier 1: Official Tavily/Perplexity/Exa docs, Claude Code GitHub issue tracker]

6. **MCP tool definitions consume significant context tokens — from 385 to 17,000+ per server.** — Confidence: **Likely**
   The commonly cited "5–10K tokens per MCP server" masks enormous variance. Measured data: SQLite MCP at 385 tokens (6 tools), Playwright at 3,442 tokens (22 tools), Jira at 17,000+. A 5-server configuration consumed 55,000 tokens — over a quarter of a 200K context window before any user message. Claude Code's Tool Search (auto-enabled at 10% context usage) reduces this by deferring schema loading. [Tier 3: Developer benchmarks using `/context` command, corroborated across 2 independent sources]

7. **DIY recursive spawning is the most flexible but most expensive approach.** — Confidence: **Likely**
   Using `--allowedTools "Bash(claude:*)"` lets an orchestrator spawn parallel Claude instances in ~20 lines of shell. Costs range from $0.20–$0.60 per standard query to $1–$5 for deep recursive research. No progress visibility, no cross-session persistence. The Cranot/deep-research tool extends this with multi-model ensembling across 7 LLM providers. Anthropic's official Agent SDK provides a structured version with typed tool use and observability hooks. [Tier 1: Anthropic Agent SDK demos; Tier 3: paddo.dev cost analysis]

8. **Anthropic frames MCP and Skills as complementary: "MCP = access, Skills = expertise."** — Confidence: **Established**
   The official Anthropic blog explicitly distinguishes: skills encode methodology (how to research), MCP servers provide data access (search APIs, databases). A skill can orchestrate MCP servers; an MCP server can support many skills. The best setup combines a skill (methodology) with MCP servers (enhanced search) — though subagent MCP bugs currently limit this in practice. [Tier 1: Anthropic blog "Extending Claude's Capabilities with Skills and MCP Servers"]

## Detailed Analysis

### What Ships Out of the Box

Claude Code includes 29 built-in tools, with `WebSearch` and `WebFetch` providing web research capabilities. The design is intentionally split: WebSearch finds pages (titles and URLs only), while WebFetch reads them (through a summarization intermediary with content limits). This conservative architecture limits prompt injection risk and keeps token costs low, but a single research question requires multiple tool calls — search, selectively fetch, then potentially search again.

The `Agent` tool enables parallel research by spawning multiple subagents simultaneously, each with its own context window. The Explore subagent (Haiku model, read-only) handles fast codebase investigation, while the general-purpose subagent inherits all tools including web search. Subagents are one level deep — they cannot spawn their own subagents.

Key limitations: WebSearch and WebFetch are unavailable on AWS Bedrock and Google Vertex. WebFetch cannot render JavaScript-heavy pages. The 125-character quote cap limits direct citations. WebFetch can only access URLs already in conversation context, constraining open-ended research chains.

### The Community Skill Landscape

The ecosystem has bifurcated into domain-specific collections and general research tools. K-Dense-AI/claude-scientific-skills (16,776 stars) and Orchestra-Research/AI-research-SKILLs (5,868 stars) are the largest by stars but serve narrow domains — scientific computation and AI/ML research engineering.

For general deep research, 199-biotechnologies/claude-deep-research-skill (371 stars, MIT) provides an 8-phase pipeline: a critique loop-back that re-triggers retrieval if gaps are found, multi-persona red teaming, and optional Python validation scripts. Four modes scale from Quick (2–5 min) to UltraDeep (20–45 min). The skill claims to "outperform OpenAI, Gemini, and Claude Desktop" but provides no benchmarks.

For academic research, Imbad0202/academic-research-skills (1,654 stars, CC-BY-NC) achieved remarkable traction in one month with a 13-agent team including specialized roles (Bibliography Agent, Devil's Advocate, Ethics Review, Risk of Bias) and 7 research modes including PRISMA systematic reviews and Socratic guided dialogue. The self-disclosure that 21/68 issues were missed by 3 integrity check rounds is notable transparency.

Weizhena/Deep-Research-skills (258 stars) takes a different approach: a simpler 2-phase workflow (outline, then fill) with explicit human checkpoints between phases and cross-platform support (Claude Code, OpenCode, Codex).

### MCP Search Servers: Enhanced Search with Caveats

The four major providers each have distinct strengths:

- **Tavily**: Most feature-complete (search, extract, map, crawl). 1,000 free credits/month. Best for technical documentation and structured extraction.
- **Perplexity**: Returns synthesized answers with citations. Deep-research mode uses sonar-deep-research. $5/1K requests. Best for complex questions requiring reasoning.
- **Exa**: Neural/semantic search — finds conceptually similar content rather than keyword matches. Free tier available. Best for exploratory research.
- **mcp-omnisearch**: Meta-server aggregating 7 providers with auto-routing. Maximum flexibility, but requires managing multiple API keys.

The critical caveat: **MCP tools do not reliably work inside Claude Code subagents** as of March 2026. Multiple open issues (#7296, #13898, #14496) confirm this. Custom subagents hallucinate results instead of erroring — a dangerous failure mode for research. Background/async subagents cannot access MCP tools at all. The workaround (user-scope MCP + built-in subagent types only) is partial. Any research skill spawning parallel agents cannot reliably use MCP search.

### DIY Approaches

Three tiers:

1. **Recursive spawning** (~20 lines of shell): Lowest barrier, highest per-query cost ($1–$5). No persistence. Quality depends on prompt engineering.
2. **Agent SDK pipelines** (days of engineering): Anthropic's official pattern with typed tool use and observability hooks. Production-grade.
3. **Multi-model ensembling** (Cranot/deep-research): Knowledge graphs with epistemic state tracking across 7 LLM providers. "Cheap models ensemble well" — Haiku + Gemini Flash as leaf agents.

### What Should You Choose

| Your Profile | Best Approach | Setup | Cost/Query |
|---|---|---|---|
| Developer, quick answers | Built-in WebSearch + WebFetch | 0 min | ~$0.01 |
| Product manager, competitive research | Community skill (general-purpose) | 2 min | $0.10–$0.50 |
| Academic writing papers | Imbad0202 academic-research-skills | 2 min | ~$3+ |
| Startup founder, market research | Community skill + optional Perplexity MCP | 2–10 min | $0.50–$5 |
| Enterprise due diligence | DIY Agent SDK pipeline or UltraDeep skill mode | Hours (DIY) / 2 min (skill) | $1–$5 |
| AI/ML researcher | Orchestra-Research or K-Dense-AI | 5 min | Varies |

**General principle**: Start with built-in tools + a community skill. Add MCP servers when you hit search quality limits. Build custom only when you need domain-specific logic or production infrastructure.

## Sources

1. [Claude Code Tools Reference](https://code.claude.com/docs/en/tools-reference) — [Tier 1] Complete list of 29 built-in tools
2. [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents) — [Tier 1] Subagent types, parallel execution, one-level-deep constraint
3. [WebSearch Tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) — [Tier 1] Pricing, domain filtering, dynamic filtering
4. [WebFetch Tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool) — [Tier 1] URL restriction, caching, PDF support
5. [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) — [Tier 1] 8-phase pipeline, 371 stars
6. [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) — [Tier 1] 13-agent team, 1,654 stars, CC-BY-NC
7. [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) — [Tier 1] Human-in-the-loop, 258 stars
8. [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — [Tier 1] 16,776 stars, 136 scientific skills
9. [Orchestra-Research/AI-research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs) — [Tier 1] 5,868 stars, 87 AI/ML skills
10. [Tavily MCP Server Docs](https://docs.tavily.com/documentation/mcp) — [Tier 1] 4 tools, free tier
11. [Perplexity MCP Server Docs](https://docs.perplexity.ai/guides/mcp-server) — [Tier 1] Deep-research mode, $5/1K requests
12. [Exa MCP Docs](https://exa.ai/docs/reference/exa-mcp) — [Tier 1] Neural search, free tier
13. [mcp-omnisearch](https://github.com/spences10/mcp-omnisearch) — [Tier 1] 7-provider meta-MCP
14. [Anthropic Agent SDK Demos — research-agent](https://github.com/anthropics/claude-agent-sdk-demos/tree/main/research-agent) — [Tier 1] Official orchestrator-worker pattern
15. [Extending Claude's Capabilities — Anthropic Blog](https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers) — [Tier 1] "MCP = access, Skills = expertise"
16. [GitHub Issue #7296](https://github.com/anthropics/claude-code/issues/7296) — [Tier 1] Subagent MCP inheritance bug, OPEN
17. [GitHub Issue #13898](https://github.com/anthropics/claude-code/issues/13898) — [Tier 1] Custom subagent MCP hallucination, OPEN
18. [GitHub Issue #21318](https://github.com/anthropics/claude-code/issues/21318) — [Tier 1] Plugin agent web tool access, NOT_PLANNED
19. [Inside Claude Code's Web Tools — Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-web-tools/) — [Tier 2] Architecture details, Haiku intermediary
20. [Three Ways to Build Deep Research — paddo.dev](https://paddo.dev/blog/three-ways-deep-research-claude/) — [Tier 3] Cost analysis
21. [MCP Server Token Costs — jdhodges.com](https://www.jdhodges.com/blog/claude-code-mcp-server-token-costs/) — [Tier 3] Per-server token measurements
22. [Claude Code's Hidden MCP Flag — paddo.dev](https://paddo.dev/blog/claude-code-hidden-mcp-flag/) — [Tier 3] Deferred loading benchmark
23. [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — [Tier 2] Skill discovery hub, 34,585 stars
24. [Cranot/deep-research](https://github.com/Cranot/deep-research) — [Tier 1] Multi-model ensembling
25. [MCP Search Comparison — intuitionlabs.ai](https://intuitionlabs.ai/articles/mcp-servers-claude-code-internet-search) — [Tier 3] Provider setup details

## Research Gaps

- **No independent benchmarks exist** comparing research output quality across approaches. All quality claims are self-reported or Tier 3.
- **Token cost for community skills is poorly documented.** Only Imbad0202 states requirements (200K+ input for full pipeline).
- **Subagent MCP bug resolution timeline is unknown.** Multiple issues are open with no visible Anthropic response.
- **No research angle failed.** All 3 breadth agents and 2 depth agents returned substantive findings.

---

*Research conducted using the [deep-research](https://github.com/robertnowell/deep-research) skill for Claude Code — 3 breadth agents, 2 depth agents, standard scope. Sources: 17 Tier 1, 3 Tier 2, 5 Tier 3, 0 Tier 4.*
