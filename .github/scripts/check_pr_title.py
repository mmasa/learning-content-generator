"""Validate that the PR title follows Conventional Commits.

Usage: PR_TITLE="feat(takken): add schema" python3 check_pr_title.py
"""

import os
import re
import sys

PATTERN = re.compile(
    r"^(feat|fix|docs|data|security|chore|refactor|test|ci|build|perf|style|revert)"
    r"(\([\w./-]+\))?!?: .+"
)


def main() -> int:
    title = os.environ.get("PR_TITLE", "")
    if PATTERN.match(title):
        print(f"OK: {title!r}")
        return 0
    print(f"error: PR title {title!r} does not follow Conventional Commits", file=sys.stderr)
    print("expected e.g.: feat(takken): add question schema (#123)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
