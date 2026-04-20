---
name: deep-research
description: "Deep multi-source research with source quality evaluation and hard quality gates. Launches parallel research agents, classifies sources by tier, cross-references findings, and synthesizes structured reports. Use when asked to research, investigate, or deeply analyze any topic requiring multi-source evidence."
argument-hint: "[quick|standard|thorough|angles] <research question or topic>"
---

# Deep Research

You are conducting deep research on a topic. Your goal is a well-sourced, structured report that answers the user's question thoroughly, with every claim grounded in classified sources.

Research question: $ARGUMENTS

---

## Phase 1: Analyze

Before launching any agents, reason through the following:

1. **Parse scope**: If the first word of the arguments is "quick", "thorough", or "angles", treat it as a scope modifier. Otherwise, default to "standard" scope.
   - **quick**: 2 breadth agents, skip depth phase, skip verification
   - **standard**: 3 breadth agents, 1-2 depth agents, skip verification
   - **thorough**: 5 breadth agents, 2-3 depth agents, source verification phase
   - **angles**: 4 breadth agents (each exploring a distinct facet — surprising facts, counterintuitive claims, unresolved debates, real-world anchors), skip depth, skip verification. Output is a candidate-angles list, NOT a question-answered report. Use this mode when the caller wants angle-surfacing for a piece of content, not a definitive answer. See "Angles mode" section below.

2. **Codebase relevance**: Does this question reference the local project, its tech stack, or its architecture? If yes, include a codebase exploration agent (subagent_type: Explore) in the breadth phase.

3. **Research angles**: Break the question into 3-5 distinct angles worth investigating. Each angle should target a different facet of the question — e.g., current state, historical context, competing approaches, practical implementation, known pitfalls.

4. **Show the user your research plan** before proceeding: list the scope, angles, and how many agents you intend to launch.

---

## Phase 2: Breadth Search

Launch parallel Sonnet agents (count based on scope). Each agent gets one research angle. Send all Agent tool calls in a single message to maximize parallelism.

Use this EXACT prompt for each research agent, filling in {angle} and {question}:

```
You are a research agent investigating one specific angle of a broader research question.

YOUR ANGLE: {angle}
BROADER QUESTION: {question}

## Source Classification

Classify every source you use by tier:
- [Tier 1] Primary: official docs, specs, peer-reviewed papers, direct announcements, author's own repo/blog
- [Tier 2] Curated secondary: major publications, established reference sites (MDN, Wikipedia w/ citations), published analysis
- [Tier 3] Community: blog posts, Stack Overflow, forums, tutorials, podcasts, newsletters
- [Tier 4] Unverifiable: social media, AI-generated content, SEO listicles, content farms, undated/unattributed pages
Red flags: circular citations, "updated for [year]" with no changelog, claims without specifics, AI citing AI

## Instructions

1. Use WebSearch with at least 2 different search queries to find 3-5 relevant sources.
   Vary query phrasing, synonyms, and specificity across queries.
   Prefer Tier 1/2 sources over Tier 3/4.
   If a search query returns nothing useful, reformulate and try again (up to 3 attempts per query).
2. Use WebFetch to read the top 2-3 most promising sources thoroughly. Extract specific facts, data points, and direct quotes.
3. If any source references another important source, follow that lead with WebFetch.
4. Do NOT fabricate or assume information. If a source does not clearly state something, say so.

## Failure Protocol

If after 3 query reformulations you cannot find any Tier 1/2 sources:
- Return NO_USEFUL_FINDINGS
- List all queries you attempted
- Note what you expected to find vs. what was available
- Do NOT pad findings with Tier 4 sources to appear successful

## Return Format

Return your findings in this EXACT format:

## Angle: [your angle]

### Sources Consulted
1. [Title](URL) — [Tier N] one-line description of what it contributed
2. ...

### Key Findings
1. **[Finding]** — [Details with specifics: numbers, dates, names]. (Source: #N)
   > "Direct quote from source if available"
2. ...

### Contradictions or Uncertainties
- [anything where sources disagree or are ambiguous]

### Leads Worth Following
- [URLs or topics discovered but not yet explored]

### Confidence: [Established/Likely/Emerging/Contested/Speculative] — [brief justification referencing source tiers]

Confidence label definitions:
- Established: 2+ independent Tier 1/2 sources agree
- Likely: 1 Tier 1/2 source, or 2+ Tier 3 sources corroborate
- Emerging: Single Tier 2/3 source, no contradiction found
- Contested: Tier 1/2 sources disagree with each other
- Speculative: Only Tier 3/4 sources, or single uncorroborated claim
```

**If an agent returns NO_USEFUL_FINDINGS**, reformulate that angle into a more specific or broader question and dispatch one replacement agent before moving on. If the replacement also fails, accept the gap and note it.

---

## Phase 3: Depth Search

**Skip this phase entirely if scope is "quick".**

Review all breadth results. Identify:
- **(a)** Claims that appear in only one source (unverified)
- **(b)** Contradictions between agents' findings
- **(c)** "Leads Worth Following" that look promising
- **(d)** Areas where all agents were shallow or vague

Launch 1-3 targeted Sonnet agents (model: sonnet) to address the most important gaps. Use the same agent prompt template from Phase 2, but replace {angle} with a specific gap-filling directive like "Verify whether [claim] is accurate by finding primary sources" or "Investigate the opposing viewpoint on [topic]".

**Codebase integration** (only if relevant): Launch one additional agent with subagent_type "Explore" to search the local codebase for code, patterns, or configuration related to the research question. Ask it to return specific file paths and code snippets that connect to the web findings.

---

## Phase 4: Source Verification

**Skip this phase unless scope is "thorough".**

For each high-importance claim that came from a single source, launch a verification agent with `model: haiku`:

```
You are a fact-checking agent. Your ONLY job is to verify whether a specific claim is supported by a specific source.

CLAIM: {claim}
SOURCE URL: {url}

Use WebFetch to read the source. Then answer:
1. Does the source support this claim? (YES / PARTIALLY / NO / SOURCE UNAVAILABLE)
2. If not YES, what does the source actually say?
3. Most relevant direct quote from the source.

Do not add interpretation. Do not search for other sources. Only evaluate this one source against this one claim.
```

Collect all verification results for the report.

---

## Phase 5: Synthesize & Report

Synthesis happens in the main conversation context (not a separate agent) to preserve full access to the user's question and conversation history.

**Before synthesizing**, read `${CLAUDE_SKILL_DIR}/references/synthesis-patterns.md` for methodology on grouping, contradiction resolution, and output templates. Also consult `${CLAUDE_SKILL_DIR}/references/source-evaluation.md` for detailed red flag detection and cross-referencing rules when evaluating source quality.

**Apply these confidence labels** to each Key Finding based on source evidence:
- **Established**: 2+ independent Tier 1/2 sources agree
- **Likely**: 1 Tier 1/2 source, or 2+ Tier 3 sources corroborate
- **Emerging**: Single Tier 2/3 source, no contradiction found
- **Contested**: Tier 1/2 sources disagree with each other
- **Speculative**: Only Tier 3/4 sources, or single uncorroborated claim

**Use the output template** matching the scope (quick/standard/thorough) from synthesis-patterns.md.

---

## Hard Quality Gates

Enforce ALL of these BEFORE presenting the report to the user. These are not suggestions — the report must pass every gate.

1. **Citation requirement**: Every Key Finding must cite ≥1 source with a [Tier N] annotation. Any finding without a source → move to a separate "Unverified Observations" section at the end.

2. **No fabricated URLs**: Every URL in the Sources section must appear in at least one agent's output. Any URL not traceable to an agent → remove it.

3. **Question answered**: The Executive Summary must explicitly state whether the research question is **fully answered**, **partially answered**, or **unanswerable with available evidence**. If this is missing, add it before presenting.

4. **Source quality caveat**: If >50% of cited sources are Tier 3 or Tier 4, prepend this caveat to the report: *"Note: This research relies primarily on community and secondary sources. Key claims should be independently verified."*

5. **Failed angles disclosed**: If any agent returned `NO_USEFUL_FINDINGS`, the failed angle and attempted queries must appear in the Research Gaps section. Do not silently drop failed angles.

---

## Phase 6: Persist Report

**Write the report to disk before ending the turn.** Reports must survive the conversation — a report that only exists in chat context is useless the moment the session compacts or closes.

1. **Pick a contextual slug** — 2-5 words that identify the *topic*, not the raw question. Examples:
   - "What are the tradeoffs between SQLite and PostgreSQL for new web apps?" → `sqlite-vs-postgres`
   - "Should we migrate from Redis to Valkey?" → `redis-to-valkey-migration`
   - "What is WebTransport?" → `webtransport-overview`
   - Kebab-case, lowercase, alphanumerics and hyphens only, ~40 chars max. No filler words ("what-is", "should-we", "how-to").

2. **Build the path**: `~/Documents/deep-research/YYYY-MM-DD-<slug>.md`. Expand `~` to the absolute home path. Create `~/Documents/deep-research/` if it doesn't exist.

3. **Write the full report** using the Write tool — the same content you're about to display inline (Executive Summary, Key Findings with sources, Research Gaps, confidence labels, quality gate disclosures). Include a frontmatter block at the top:
   ```yaml
   ---
   question: <original user question>
   scope: <quick|standard|thorough|angles>
   date: YYYY-MM-DD
   ---
   ```

4. **Display the COMPLETE report inline.** Not a summary. Not a highlight reel. The full report — Executive Summary, all Key Findings with citations, Detailed Analysis, Source Verification table (thorough scope), Sources, Research Gaps, Methodology. The chat transcript is the primary delivery; the file is an archive for post-session access. Claude Code's TUI renders markdown (headers, tables, code blocks, bold) — use that.

   The file and the inline output are the same content. Do not save one and truncate the other.

5. **After displaying the report**, print a single final line with the re-view command — ready to copy-paste into the terminal:
   ```
   glow /Users/<you>/Documents/deep-research/2026-04-14-sqlite-vs-postgres.md
   ```
   (`glow` is a terminal-native markdown renderer — `brew install glow` if not present. Any markdown viewer works: `bat`, `mdcat`, `code`, etc. The point is the path is prefixed with a ready command rather than bare text.)

If a file with that path already exists (same day, same slug), append `-2`, `-3`, etc. before the extension — don't overwrite prior reports.

This applies to every scope including `angles`.

---

## Angles mode (scope: angles)

When scope is "angles", the goal is different from quick/standard/thorough. You are not answering a question; you are surfacing a pool of candidate angles for a piece of content (typically a video essay, blog post, or talk) to choose from. The caller will pick 2–4 angles to develop further; your job is to give them enough to choose from and to ground each candidate angle in real sources.

**Skip the normal Phase 1 step 3** ("break into 3-5 angles"). Instead, use these four fixed facets as the breadth agents:

1. **Surprising facts** — what do insiders know that most people don't? What numbers or mechanisms in this space are counterintuitive? Look for specific named facts (with sources) that would make a viewer say "wait, what?"
2. **Counterintuitive claims / overreach** — where is the public narrative wrong or oversimplified? Where is the industry overreaching (claiming more than the evidence supports)? Who's the most credible critic, and what do they say?
3. **Unresolved debates** — what are the open questions experts are actively disagreeing about? Where are there competing explanations with different adherents? Name the sides and the best source for each.
4. **Real-world anchors** — specific companies, incidents, dates, case studies, court filings, primary-source documents, named people. These are the hooks the final script will lean on. List specific anchors with URLs.

Each facet agent runs with the same tier classification rules and output format from Phase 2 (Key Findings with sources).

**Skip Phase 3 (depth) and Phase 4 (verification)** entirely in angles mode. The caller is doing a shallow pass to pick angles; the winning angle will get a thorough pass later.

**Phase 5 synthesis format for angles mode:**

Instead of the normal report template, return:

```
# Candidate Angles — [topic]

## Executive summary
Two sentences on what this topic actually looks like once you've surveyed it. Not a thesis; a lay of the land.

## Candidate Angles

### Angle 1 — [short punchy name]
- **Thesis in one sentence**: [concrete claim with at least one number or proper noun]
- **Why it might click**: [one sentence on the hook]
- **Research anchors**: [2-4 bullet points, each a specific source/fact/quote with tier annotation]

### Angle 2 — [name]
(same structure)

### Angle 3 — [name]
(same structure)

### Angle 4 — [name]
(same structure)

### Angle 5 — [name] (optional)
(same structure)

## Sources consulted
All sources used across the four facets, tier-classified.

## Notes
Anything the caller should know about the research pool — contested topics, sources that disagreed, gaps.
```

**Quality gate for angles mode**: every candidate angle must be grounded in at least one Tier 1 or Tier 2 source. If you can't anchor an angle in real material, drop it. Better to return 3 grounded angles than 6 speculative ones.
