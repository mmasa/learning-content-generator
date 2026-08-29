"""Validate that the PR body contains the required sections and declarations.

Checks (failing unless present):
- Related Issue with an issue reference (#N)
- Test Evidence, Security Impact, Data and Copyright Review sections filled in
- AI Usage declaration (AI Used: Yes / No)
- AI Token Summary with numbers or an explicit not-provided/unknown/estimated
- Estimated and Actual Person-Hours filled in
- Reviewer named in Reviewer Approval

Usage: PR_BODY="$(...)" python3 check_pr_body.py
"""

import os
import re
import sys

REQUIRED_SECTIONS = [
    "Related Issue",
    "Summary",
    "Changes",
    "Test Evidence",
    "Security Impact",
    "Data and Copyright Review",
    "AI Usage",
    "AI Token Summary",
    "Estimated Person-Hours",
    "Actual Person-Hours",
    "Review Checklist",
    "Rollback Plan",
    "Reviewer Approval",
]

TOKEN_MARKERS = ("not-provided", "unknown", "estimated")


def split_sections(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for line in body.splitlines():
        heading = re.match(r"^##\s+(.*)$", line)
        if heading:
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current = heading.group(1).strip()
            lines = []
        else:
            lines.append(line)
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return sections


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    errors: list[str] = []
    sections = split_sections(body)

    for name in REQUIRED_SECTIONS:
        if name not in sections:
            errors.append(f"missing section: ## {name}")
            continue
        if not strip_comments(sections[name]):
            errors.append(f"section is empty: ## {name}")

    related = strip_comments(sections.get("Related Issue", ""))
    if related and not re.search(r"#\d+", related):
        errors.append("Related Issue must reference an issue number (#N)")

    ai_usage = strip_comments(sections.get("AI Usage", ""))
    if ai_usage and not re.search(r"AI Used:\s*(Yes|No)", ai_usage, re.IGNORECASE):
        errors.append("AI Usage must declare 'AI Used: Yes' or 'AI Used: No'")

    tokens = strip_comments(sections.get("AI Token Summary", ""))
    ai_used = bool(re.search(r"AI Used:\s*Yes", ai_usage, re.IGNORECASE))
    if ai_used and tokens:
        has_numbers = bool(re.search(r"\d", tokens))
        has_marker = any(marker in tokens.lower() for marker in TOKEN_MARKERS)
        if not (has_numbers or has_marker):
            errors.append(
                "AI Token Summary must contain token counts or an explicit "
                "not-provided / unknown / estimated"
            )

    reviewer = strip_comments(sections.get("Reviewer Approval", ""))
    if reviewer and not re.search(r"Reviewer:\s*\S", reviewer):
        errors.append("Reviewer Approval must name a reviewer (Reviewer: <name>)")

    for name in ("Estimated Person-Hours", "Actual Person-Hours"):
        value = strip_comments(sections.get(name, ""))
        if value and not re.search(r"\d", value):
            errors.append(f"{name} must contain a number of person-hours")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"\nPR body validation failed with {len(errors)} error(s).", file=sys.stderr)
        print("Fill in .github/PULL_REQUEST_TEMPLATE.md completely.", file=sys.stderr)
        return 1
    print("PR body OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
