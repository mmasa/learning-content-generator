"""Validate all JSON Schemas and check example/sample data against them.

Run from the repository root: uv run python .github/scripts/validate_schemas.py
"""

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]

SCHEMA_GLOBS = ["schemas/*.schema.json", "contents/*/schemas/*.schema.json"]

# (schema, data file, validate-each-item)
DATA_CHECKS = [
    ("schemas/ai-usage-log.schema.json", "examples/ai-usage/2026-07.yaml", False),
    ("schemas/work-log.schema.json", "examples/effort/2026-07.yaml", False),
    ("schemas/issue-estimate.schema.json", "examples/effort/estimates.yaml", False),
    (
        "contents/takken/schemas/question.schema.json",
        "contents/takken/normalized/samples/sample-questions.yaml",
        True,
    ),
    (
        "contents/takken/schemas/source-record.schema.json",
        "contents/takken/metadata/sources.yaml",
        True,
    ),
]


def json_safe(data: Any) -> Any:
    return json.loads(json.dumps(data, default=str))


def main() -> int:
    errors: list[str] = []

    validators: dict[str, Draft202012Validator] = {}
    for pattern in SCHEMA_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            rel = str(path.relative_to(ROOT))
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                validators[rel] = Draft202012Validator(schema)
                print(f"schema OK: {rel}")
            except Exception as exc:  # report every schema problem, keep checking the rest
                errors.append(f"{rel}: invalid schema: {exc}")

    for schema_rel, data_rel, each_item in DATA_CHECKS:
        validator = validators.get(schema_rel)
        data_path = ROOT / data_rel
        if validator is None:
            errors.append(f"{schema_rel}: schema missing for data check")
            continue
        if not data_path.is_file():
            errors.append(f"{data_rel}: data file missing")
            continue
        data = json_safe(yaml.safe_load(data_path.read_text(encoding="utf-8")))
        items = data if each_item else [data]
        for index, item in enumerate(items):
            for error in validator.iter_errors(item):
                errors.append(f"{data_rel} [{index}]: {error.message}")
        print(f"data OK: {data_rel} (against {schema_rel})")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("all schemas and data valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
