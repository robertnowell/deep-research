#!/usr/bin/env python3
"""
Output validator for deep-research skill.

Checks structural compliance against quality gates and format rules.
Zero dependencies — stdlib only.

Usage:
    python validate.py output.md [--scope quick|standard|thorough] [--json]
    cat output.md | python validate.py - [--scope standard]
"""

import re
import sys
import json
import argparse

VALID_CONFIDENCE_LABELS = {
    "Established", "Likely", "Emerging", "Contested", "Speculative"
}

REQUIRED_SECTIONS = {
    "quick": ["Executive Summary", "Key Findings", "Sources"],
    "standard": ["Executive Summary", "Key Findings", "Detailed Analysis", "Sources", "Research Gaps"],
    "thorough": ["Executive Summary", "Key Findings", "Detailed Analysis", "Sources",
                 "Research Gaps", "Source Verification Results", "Methodology"],
}

ANSWER_STATUS_PATTERNS = [
    r"fully answered",
    r"partially answered",
    r"unanswerable",
]

SOURCE_QUALITY_CAVEAT = "relies primarily on community and secondary sources"


def parse_sections(text):
    """Split markdown into sections by ## headers. Returns dict of header -> content."""
    sections = {}
    current_header = None
    current_lines = []

    for line in text.split("\n"):
        match = re.match(r"^##\s+(.+)$", line)
        if match:
            if current_header is not None:
                sections[current_header] = "\n".join(current_lines)
            current_header = match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_header is not None:
        sections[current_header] = "\n".join(current_lines)

    return sections


def extract_sources(sections):
    """Extract sources from the Sources section. Returns list of (tier, url) tuples."""
    sources_content = sections.get("Sources", "")
    sources = []
    for line in sources_content.split("\n"):
        line = line.strip()
        if not line or not re.match(r"^\d+\.", line):
            continue
        tier_match = re.search(r"\[Tier\s*([1-4])\]", line)
        url_match = re.search(r"\((https?://[^\)]+)\)", line)
        tier = int(tier_match.group(1)) if tier_match else None
        url = url_match.group(1) if url_match else None
        sources.append({"tier": tier, "url": url, "line": line})
    return sources


def extract_findings(sections):
    """Extract Key Findings. Returns list of dicts with label and citation info."""
    findings_content = sections.get("Key Findings", "")
    findings = []
    current_finding = None

    for line in findings_content.split("\n"):
        line = line.strip()
        # Match numbered finding lines like "1. **Finding** — Confidence: Established"
        finding_match = re.match(r"^\d+\.\s+\*\*(.+?)\*\*", line)
        if finding_match:
            if current_finding:
                findings.append(current_finding)
            label_match = re.search(
                r"Confidence:\s*(Established|Likely|Emerging|Contested|Speculative)",
                line, re.IGNORECASE
            )
            # Check for source references like (Source: #1) or [1] or (#1)
            has_citation = bool(re.search(r"(?:Source|#\d|\[\d)", line))
            current_finding = {
                "name": finding_match.group(1),
                "label": label_match.group(1) if label_match else None,
                "has_citation": has_citation,
                "line": line,
            }
        elif current_finding and not current_finding["has_citation"]:
            # Check continuation lines for citations
            if re.search(r"(?:Source|#\d|\[\d)", line):
                current_finding["has_citation"] = True

    if current_finding:
        findings.append(current_finding)

    return findings


class CheckResult:
    def __init__(self, name, status, detail=""):
        self.name = name
        self.status = status  # "PASS", "FAIL", "SKIP"
        self.detail = detail

    def to_dict(self):
        d = {"name": self.name, "status": self.status}
        if self.detail:
            d["detail"] = self.detail
        return d

    def __str__(self):
        base = f"{self.status:<4}  {self.name}"
        if self.detail:
            base += f" — {self.detail}"
        return base


def check_sections_present(sections, scope):
    required = REQUIRED_SECTIONS.get(scope, REQUIRED_SECTIONS["standard"])
    missing = [s for s in required if s not in sections]
    if missing:
        return CheckResult("sections_present", "FAIL", f"Missing: {', '.join(missing)}")
    return CheckResult("sections_present", "PASS")


def check_tier_annotations(sources):
    if not sources:
        return CheckResult("tier_annotations", "FAIL", "No sources found in Sources section")
    missing = [s for s in sources if s["tier"] is None]
    if missing:
        examples = [s["line"][:60] + "..." for s in missing[:3]]
        return CheckResult("tier_annotations", "FAIL",
                           f"{len(missing)} source(s) missing [Tier N]: {examples}")
    return CheckResult("tier_annotations", "PASS")


def check_confidence_labels(findings):
    if not findings:
        return CheckResult("confidence_labels", "FAIL", "No findings found in Key Findings section")
    missing = []
    invalid = []
    for i, f in enumerate(findings, 1):
        if f["label"] is None:
            missing.append(f"Finding #{i}")
        elif f["label"] not in VALID_CONFIDENCE_LABELS:
            invalid.append(f"Finding #{i} has '{f['label']}'")
    if missing or invalid:
        issues = missing + invalid
        return CheckResult("confidence_labels", "FAIL", "; ".join(issues))
    return CheckResult("confidence_labels", "PASS")


def check_citation_present(findings):
    if not findings:
        return CheckResult("citation_present", "FAIL", "No findings found")
    uncited = [f"Finding #{i}" for i, f in enumerate(findings, 1) if not f["has_citation"]]
    if uncited:
        return CheckResult("citation_present", "FAIL", f"No source citation: {', '.join(uncited)}")
    return CheckResult("citation_present", "PASS")


def check_no_orphan_urls():
    return CheckResult("no_orphan_urls", "SKIP", "Requires agent output to validate")


def check_answer_status(sections):
    summary = sections.get("Executive Summary", "")
    full_text = summary.lower()
    for pattern in ANSWER_STATUS_PATTERNS:
        if re.search(pattern, full_text):
            return CheckResult("answer_status", "PASS")
    return CheckResult("answer_status", "FAIL",
                       "Executive Summary missing answer status "
                       "(expected 'fully answered', 'partially answered', or 'unanswerable')")


def check_source_quality_caveat(text, sources):
    if not sources:
        return CheckResult("source_quality_caveat", "SKIP", "No sources to evaluate")
    sources_with_tier = [s for s in sources if s["tier"] is not None]
    if not sources_with_tier:
        return CheckResult("source_quality_caveat", "SKIP", "No tier-annotated sources")
    low_quality = sum(1 for s in sources_with_tier if s["tier"] >= 3)
    ratio = low_quality / len(sources_with_tier)
    if ratio > 0.5:
        if SOURCE_QUALITY_CAVEAT in text.lower():
            return CheckResult("source_quality_caveat", "PASS",
                               f"{low_quality}/{len(sources_with_tier)} sources are Tier 3/4, caveat present")
        return CheckResult("source_quality_caveat", "FAIL",
                           f"{low_quality}/{len(sources_with_tier)} sources are Tier 3/4 but caveat is missing")
    return CheckResult("source_quality_caveat", "PASS",
                       f"{low_quality}/{len(sources_with_tier)} sources are Tier 3/4 (below threshold)")


def check_failed_angles(sections):
    gaps = sections.get("Research Gaps", "")
    if "NO_USEFUL_FINDINGS" in gaps:
        return CheckResult("failed_angles_disclosed", "PASS", "Failed angles documented in Research Gaps")
    # We can't tell if there SHOULD be failed angles without agent output,
    # so if there's no mention, it's either fine or undetectable
    return CheckResult("failed_angles_disclosed", "SKIP", "No failure indicators found (may be correct)")


def validate(text, scope="standard"):
    sections = parse_sections(text)
    sources = extract_sources(sections)
    findings = extract_findings(sections)

    results = [
        check_sections_present(sections, scope),
        check_tier_annotations(sources),
        check_confidence_labels(findings),
        check_citation_present(findings),
        check_no_orphan_urls(),
        check_answer_status(sections),
        check_source_quality_caveat(text, sources),
        check_failed_angles(sections),
    ]

    return results


def main():
    parser = argparse.ArgumentParser(description="Validate deep-research output")
    parser.add_argument("file", help="Markdown file to validate (or - for stdin)")
    parser.add_argument("--scope", choices=["quick", "standard", "thorough"],
                        default="standard", help="Expected scope (default: standard)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
    else:
        with open(args.file) as f:
            text = f.read()

    results = validate(text, args.scope)

    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    skipped = sum(1 for r in results if r.status == "SKIP")

    if args.json:
        output = {
            "results": [r.to_dict() for r in results],
            "summary": {"passed": passed, "failed": failed, "skipped": skipped},
            "success": failed == 0,
        }
        print(json.dumps(output, indent=2))
    else:
        for r in results:
            print(r)
        print(f"\n{passed}/{len(results)} passed, {failed} failed, {skipped} skipped")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
