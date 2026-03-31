# Source Evaluation Framework

This reference defines how to classify, evaluate, and cross-reference sources during research.

## Source Tiers

### Tier 1 — Primary Sources
Direct, authoritative origins of information. Highest credibility.

Examples:
- Official documentation and specifications
- Peer-reviewed papers and journals
- Government and regulatory filings (SEC, patents, court records)
- Direct announcements from the entity being discussed
- Author's own repository, blog, or talk about their own project
- Raw data sets from authoritative institutions
- Standards body publications (W3C, IETF, ISO)

### Tier 2 — Curated Secondary Sources
Professionally edited, fact-checked, or peer-reviewed analysis of primary material.

Examples:
- Major publications: NYT, WSJ, Ars Technica, The Verge, Nature, Science, IEEE
- Established reference sites: MDN Web Docs, Wikipedia (with inline citations)
- Conference proceedings (peer-reviewed)
- Published books by domain experts
- Investigative journalism with named sources
- Analyst reports from recognized firms (Gartner, Forrester — note potential bias)

### Tier 3 — Community Sources
Unvetted but often valuable. Good for signals, bad as sole evidence.

Examples:
- Personal blog posts and tutorials
- Stack Overflow answers
- Forum discussions (Reddit, HN, Discord)
- Conference talks and podcasts (non-peer-reviewed)
- Newsletters and substacks
- Non-peer-reviewed preprints (arXiv without publication)
- YouTube explainers

### Tier 4 — Unverifiable Sources
Cannot be traced to a credible origin. Do not use as evidence for findings.

Examples:
- Anonymous social media posts
- AI-generated content without human editorial review
- SEO listicles ("Top 10 Best X in 2026")
- Content farms and syndicated filler
- Press releases with no independent verification
- Undated or unattributed pages
- Scraped/aggregated sites that repackage others' content

## Red Flags

Watch for these signals that a source may be unreliable:

- **Circular citations**: A cites B, B cites A, neither has primary evidence
- **Evergreen SEO farming**: "Updated for [current year]" with no changelog or diff
- **Vague authority**: Claims without specifics — no numbers, dates, names, or methodology
- **Consensus manufacturing**: Single-source claims presented as "experts agree" or "it's well known"
- **AI echo chamber**: AI-generated research citing other AI-generated research with no primary anchor
- **Survivorship bias**: Only successful cases cited, failures omitted
- **Conflict of interest**: Vendor research about their own product category (flag, don't discard)

## Cross-Referencing Rules

These rules determine confidence labels based on source tier and corroboration:

| Scenario | Confidence Label |
|---|---|
| 2+ independent Tier 1/2 sources agree | **Established** |
| 1 Tier 1/2 source, or 2+ Tier 3 sources corroborate | **Likely** |
| Single Tier 2/3 source, no contradiction | **Emerging** |
| Tier 1/2 sources disagree with each other | **Contested** |
| Only Tier 3/4 sources, or single uncorroborated claim | **Speculative** |

Key principles:
- "Independent" means sources that don't cite each other as their basis
- A Tier 3 source that cites a Tier 1 source inherits Tier 1 for that specific claim (but verify the citation is accurate)
- Quantity of Tier 3 sources does not override a single Tier 1 source
- Tier 4 sources should not appear in Key Findings — note them in Research Gaps if they're the only evidence available

## Condensed Tier Summary (for agent prompts)

Use this condensed version when including tier definitions in research agent prompts:

```
Source tiers — classify every source:
- [Tier 1] Primary: official docs, specs, peer-reviewed papers, direct announcements, author's own repo/blog
- [Tier 2] Curated secondary: major publications, established reference sites (MDN, Wikipedia w/ citations), published analysis
- [Tier 3] Community: blog posts, Stack Overflow, forums, tutorials, podcasts, newsletters
- [Tier 4] Unverifiable: social media, AI-generated content, SEO listicles, content farms, undated/unattributed pages
Red flags: circular citations, "updated for [year]" with no changelog, claims without specifics, AI citing AI
```
