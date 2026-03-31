# Inventive and Unexpected Uses of Deep Research with Claude Code

> This is an example output from `/deep-research standard` demonstrating source tiers, confidence labels, and quality gates on a creative, open-ended topic.

---

**Scope**: standard (3 breadth agents, 1 depth agent)

**Research angles**:
1. Business and professional applications (due diligence, competitive intelligence, finance)
2. Developer workflow integrations (debugging, architecture decisions, security, migrations)
3. Content creation and creative applications (journalism, OSINT, science, personal)
4. (Depth) Chained workflows where research feeds directly into automated action

---

*Note: This research relies primarily on community and secondary sources. Key claims should be independently verified.*

## Executive Summary

This question is **fully answered**. Deep research tools with Claude Code are being used far beyond "research a topic and get a report." The most inventive applications treat research as a **pipeline stage** — the output feeds directly into code generation, dashboard deployment, content publishing, financial models, or knowledge graphs. Documented workflows span M&A due diligence (compressing 6-week timelines to 2 weeks), investigative journalism (replicating published investigations in under an hour), security vulnerability research (500+ previously undetected bugs in production codebases), OSINT investigations with chain-of-custody evidence, genealogy with chromosome-level DNA mapping, and self-improvement systems that analyze your own journal entries against your Git commits. The common thread: the research output is *consumed by another process*, not just read by a human.

## Key Findings

1. **The most inventive pattern is research → automated action, not research → report.** — Confidence: **Likely**
   Multiple independent practitioners document workflows where deep research feeds directly into downstream automation: competitor ad analysis → branded PDF for creative teams, backlink research → 3-month content calendar (20 minutes), Google Ads data → Slack-delivered Monday morning reports, stock research → structured JSON for programmatic consumption, and multi-platform ad data → auto-deployed React dashboard that Claude itself wrote. [Tier 2: Lenny's Newsletter; Tier 3: Stormy AI, AI Automators, paddo.dev — corroborated across 4+ independent sources]

2. **M&A due diligence is the highest-stakes documented application.** — Confidence: **Established**
   Tribe AI's VDR copilot processes 30–50 GB of mixed files (PDFs, Excel models, board decks, vendor databases with 50K+ entries) in a single pipeline, compressing diligence from 6 weeks to 2 weeks and reducing manual review by 80%. Separately, an outside-in diligence tool compressed public signal aggregation from 7–10 days to under 1 day with 30% more signal coverage. Deloitte's 2025 study found 86% of M&A organizations have integrated GenAI, with 83% investing $1M+. Anthropic launched six finance-specific agent skills with live data connectors for LSEG, Moody's, and Aiera, with named customers including RBC, Citi, and Bridgewater. [Tier 1: Anthropic finance announcement; Tier 2: Tribe AI, Deloitte study, Third Bridge]

3. **Claude Code Security found 500+ previously undetected vulnerabilities by treating security as a research problem.** — Confidence: **Established**
   Launched February 2026, Claude Code Security applies reasoning-based analysis (not pattern matching) to trace data flows across entire codebases. Anthropic's team found bugs undetected for decades despite expert review. Multi-stage self-verification (Claude tries to disprove its own findings) filters false positives. Companion Trail of Bits skills orchestrate CodeQL analysis and YARA malware pattern authoring end-to-end. CSIS independently noted "hallucinations and incorrect findings" remain a challenge. [Tier 1: Anthropic announcement; Tier 2: CSIS analysis, Snyk documentation]

4. **Investigative journalism workflows replicate published investigations in under an hour.** — Confidence: **Likely**
   Nick Hagar replicated a full MuckRock/WHRO investigation into Virginia police decertifications using Claude Code skills in under an hour (~20 minutes of manual spot-checking). Washington Post data journalist Kevin Schaul used Claude Code to consolidate scattered federal AI use case inventories across agency websites. A journalism skill suite automates FOIA request drafting with state-specific guidance, source verification using the SIFT method, and pre-publish hooks enforcing source diversity checks. [Tier 3: Multiple independent practitioner accounts; Tier 2: established journalism publication]

5. **OSINT investigations with graph export and evidence chain-of-custody.** — Confidence: **Emerging**
   A Claude Code template (Claude-OSINT-Investigator) structures investigations with 8 autonomous agents handling evidence processing, entity profiling, correlation analysis, timeline building, network mapping, and SpiderFoot reconnaissance. Evidence items receive SHA-256 verification and chain-of-custody documentation. Graphs export to Mermaid and GEXF for programmatic analysis. [Tier 3: Single GitHub repo, detailed and internally consistent]

6. **Research → personal knowledge graph (Obsidian integration) turns reports into evergreen notes.** — Confidence: **Emerging**
   A Claude Code skill researches a topic, extracts concepts into atomic markdown notes prefixed `[PN-...]`, links them under Maps of Content (MOCs), and checks the existing Obsidian vault to avoid duplicates. This creates a self-building knowledge graph rather than a disposable report. Featured as a Show HN post. [Tier 3: HN Show post with community engagement]

7. **Full newsroom workflow chain: morning digest → interview prep → article → multi-platform publication.** — Confidence: **Emerging**
   One journalist documented a complete chain: `/daily-digest` aggregates RSS + Twitter + research repos into 8–10 contextualized items (saving ~25 min/day), feeding interview prep, then a publication package generator producing push notifications, Twitter threads, LinkedIn posts, and Facebook posts — all from a single article draft. [Tier 3: Single practitioner Substack with specific technical detail]

8. **ADR-driven development: research → architecture decision record → implementation.** — Confidence: **Likely**
   PubNub documents a three-stage pipeline: `pm-spec` writes a working spec → `architect-review` validates design and produces an ADR → `implementer` builds against the ADR. A team of 10+ engineers maintains ~10–15 ADRs symlinked from a shared repo, automatically loaded as context. [Tier 1: Claude Code docs; Tier 3: PubNub blog, GitHub issue with real team context]

9. **Scientific research acceleration: genome study compressed from months to 20 minutes.** — Confidence: **Established**
   Stanford's Biomni lab compressed a GWAS from months to 20 minutes and analyzed 450+ wearable data files in 35 minutes vs. three weeks. MIT's Cheeseman Lab uses Claude for CRISPR experiments, "consistently catching things" researchers missed — including novel transcription factors in embryonic tissue data. [Tier 1: Anthropic announcement with named institutions and benchmarks]

10. **Self-improvement systems that research your own behavior.** — Confidence: **Emerging**
    A practitioner created a weekly slash command that reads journal entries and analyzes Git commit history, identifies gaps between stated goals and actual activity, then generates concrete system-level improvements. Separately, customer call transcripts validate or invalidate product assumptions, with findings written to Notion/Linear as tracked hypotheses. [Tier 2: Lenny's Newsletter]

## Detailed Analysis

### Research as a Pipeline Stage (Not a Destination)

The most surprising finding is that inventive uses of deep research *don't end with a report*. The pattern: research provides structured intelligence, then a downstream process consumes it programmatically.

- **Research → Code**: Stock analysis → structured JSON for downstream systems. Competitor backlinks → code generates a content calendar. Multi-platform ad data → Claude writes and deploys a React dashboard to Vercel.
- **Research → Publication**: Perplexity deep research → Claude outline → draft → Data for SEO keyword injection → Flux image generation → WordPress auto-publish → platform-specific social posts — all automated.
- **Research → Knowledge Graph**: Topic research → Obsidian atomic notes with MOC linking → self-building vault that avoids duplicates.
- **Research → Decision Artifact**: Call transcript research → Notion/Linear hypothesis tracking. Journal + Git analysis → behavioral change recommendations.

This inverts the traditional mental model. Deep research isn't a tool you *use* — it's a stage in a pipeline you *build*.

### High-Stakes Professional Applications

Financial due diligence has the most mature implementations. The progression from "chat with documents" to "ingest an entire data room and produce structured outputs" is a qualitative leap. Tribe AI's VDR copilot processes 30–50 GB of mixed file types with traceability to specific pages and paragraphs. Third Bridge grounds research in 100,000+ proprietary expert transcripts to prevent hallucination in regulated environments.

Anthropic's launch of finance-specific skills (comparable company analysis, DCF models, earnings analysis) with live data connectors signals that "research agent" is becoming a product category, not just a prompt pattern.

### Security: Research as Offensive and Defensive Tool

Claude Code Security reframes vulnerability scanning from pattern matching to reasoning-based research. Finding 500+ previously undetected bugs — surviving decades of expert review — is a striking result. The companion ecosystem (Trail of Bits CodeQL orchestration, YARA rule authoring, OWASP skill with 20-language coverage) creates a full security research toolkit.

The recursive irony: Check Point Research used similar techniques to find CVEs *in Claude Code itself* (CVE-2025-59536, CVE-2026-21852) — security researchers using AI agents to research vulnerabilities in AI agents.

### Journalism and OSINT: Research Meets Accountability

The journalism applications chain research with verification and accountability tools. FOIA automation with state-specific guidance, source verification via the SIFT method, and pre-publish hooks enforcing source diversity checks embed research in professional editorial standards.

The OSINT investigator's chain-of-custody documentation and SHA-256 evidence verification show tools designed for contexts where research must be defensible — not just informative.

### The Weird and Wonderful

The genealogy framework with chromosome-level DNA mapping across 105+ interconnected markdown documents. The self-improvement system cross-referencing journal entries with Git commits. Voice memos recorded on walks → organized into research themes → published as LinkedIn posts. A hobby project planner that researches materials science before generating a bill of materials. These personal applications are less documented but represent the frontier — where deep research tools stop being "work tools" and become extensions of how people think.

## Sources

1. [Anthropic: Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services) — [Tier 1] Finance skills, data connectors, named customers
2. [Anthropic: Claude Code Security](https://www.anthropic.com/news/claude-code-security) — [Tier 1] 500+ vulnerabilities, reasoning-based analysis
3. [Anthropic: How Scientists Are Using Claude](https://www.anthropic.com/news/accelerating-scientific-research) — [Tier 1] Stanford GWAS, MIT CRISPR benchmarks
4. [Anthropic Engineering: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system) — [Tier 1] Internal architecture
5. [Claude Code Subagents Documentation](https://code.claude.com/docs/en/sub-agents) — [Tier 1] Debug isolation, parallel investigation, worktree isolation
6. [Tribe AI: Due Diligence Copilot](https://www.tribe.ai/applied-ai/launching-our-claude-powered-due-diligence-copilot) — [Tier 2] 30–50 GB VDR processing, 80% manual reduction
7. [Tribe AI: Outside-In Due Diligence](https://www.tribe.ai/case-studies/accelerating-outside-in-due-diligence-with-ai-insights-for-a-global-consulting-firm) — [Tier 2] 7–10 days → under 1 day
8. [Deloitte: 2025 M&A Generative AI Study](https://www.deloitte.com/us/en/what-we-do/capabilities/mergers-acquisitions-restructuring/articles/m-and-a-generative-ai-study.html) — [Tier 2] 86% adoption, $1M+ investment
9. [CSIS: AI-Driven Code Analysis](https://www.csis.org/blogs/strategic-technologies-blog/ai-driven-code-analysis-what-claude-code-security-can-and-cant-do) — [Tier 2] Independent analysis, hallucination caveat
10. [Snyk: Top Claude Skills for Cybersecurity](https://snyk.io/articles/top-claude-skills-cybersecurity-hacking-vulnerability-scanning/) — [Tier 2] Trail of Bits CodeQL, YARA, OWASP skills
11. [Lenny's Newsletter: Everyone Should Be Using Claude Code](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) — [Tier 2] Journal+Git analysis, voice notes pipeline
12. [Third Bridge: PE Due Diligence with AI](https://www.thirdbridge.com/en-us/about-us/media/perspectives/ai-due-diligence-private-equity) — [Tier 2] Expert transcript grounding
13. [Kevin Schaul: AI Data Journalism](https://kschaul.com/post/2026/02/09/2026-02-09-ai-data-journalism/) — [Tier 3] Federal AI inventory consolidation
14. [Nick Hagar: Coding Agents for Investigative Journalism](https://generative-ai-newsroom.com/coding-agents-for-investigative-journalism-8b65bc30f9ea) — [Tier 3] Investigation replication in under 1 hour
15. [jamditis/claude-skills-journalism](https://github.com/jamditis/claude-skills-journalism) — [Tier 3] FOIA automation, source verification
16. [danielrosehill/Claude-OSINT-Investigator](https://github.com/danielrosehill/Claude-OSINT-Investigator) — [Tier 3] 8-agent OSINT, SHA-256 evidence
17. [mattprusak/autoresearch-genealogy](https://github.com/mattprusak/autoresearch-genealogy) — [Tier 3] Chromosome mapping, 105+ document vault
18. [Show HN: Deep Research for Claude Code and Obsidian](https://news.ycombinator.com/item?id=47246516) — [Tier 3] Research → Obsidian atomic notes
19. [Stormy AI: Claude Code for Ad Strategy](https://stormy.ai/blog/claude-code-advertising-automation-guide) — [Tier 3] Competitor scrape → PDF, Ads → Slack
20. [Stormy AI: Growth Marketing Automation](https://stormy.ai/blog/claude-code-growth-marketing-automation-2026) — [Tier 3] Backlink research → content calendar
21. [The AI Automators: Expert-Level Blog Posts](https://www.theaiautomators.com/ai-system-for-expert-level-blog-posts/) — [Tier 3] Full publication pipeline
22. [AI Engineer: Stock Analysis Agent](https://medium.com/aingineer/building-deep-research-ai-agents-with-claude-3-7-a-working-implementation-part-2-9b629ac94506) — [Tier 3] Research → structured JSON
23. [fdaudens: AI as a Reporting Assistant](https://fdaudens.substack.com/p/how-to-use-ai-as-a-reporting-assistant) — [Tier 3] Full newsroom chain
24. [PubNub: Claude Code Subagents Best Practices](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) — [Tier 3] Three-stage ADR pipeline
25. [GitHub Issue #13853: ADR Support](https://github.com/anthropics/claude-code/issues/13853) — [Tier 2] Real team ADR workflow

## Research Gaps

- **No quantified quality comparison** exists between research-then-act pipelines and single-pass prompting. All productivity claims are self-reported.
- **Ethical guardrails for research → action chains** are undocumented. When does automated research-to-action cross ethical lines?
- **Long-term reliability** of chained workflows is unknown. One journalist noted his initial one-shot approach failed — the multi-step chain was a workaround.
- **No research angle failed.** All 3 breadth agents and the depth agent returned substantive findings.

---

*Research conducted using the [deep-research](https://github.com/robertnowell/deep-research) skill for Claude Code — 3 breadth agents, 1 depth agent, standard scope. Sources: 5 Tier 1, 7 Tier 2, 13 Tier 3, 0 Tier 4.*
