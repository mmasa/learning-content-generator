"""Validate all JSON Schemas and check example/sample data against them.

Run from the repository root: uv run python .github/scripts/validate_schemas.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]

SCHEMA_GLOBS = ["schemas/*.schema.json", "contents/*/schemas/*.schema.json"]

# (schema, data file, validate-each-item)
# Content under contents/*/normalized/ is discovered dynamically (see
# _validate_normalized_content) so newly added reading-script / audio-metadata
# files are checked without editing this list.
DATA_CHECKS = [
    ("schemas/ai-usage-log.schema.json", "examples/ai-usage/2026-07.yaml", False),
    ("schemas/work-log.schema.json", "examples/effort/2026-07.yaml", False),
    ("schemas/issue-estimate.schema.json", "examples/effort/estimates.yaml", False),
    (
        "contents/takken/schemas/source-record.schema.json",
        "contents/takken/metadata/sources.yaml",
        True,
    ),
]


def json_safe(data: Any) -> Any:
    return json.loads(json.dumps(data, default=str))


def _category_schema_map(category_dir: Path) -> dict[str, Path]:
    """schema key -> resolved schema path, from contents/<category>/config/content.yaml."""
    config_path = category_dir / "config" / "content.yaml"
    if not config_path.is_file():
        return {}
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    schemas = config.get("schemas", {})
    return {key: (category_dir / rel).resolve() for key, rel in schemas.items()}


def _validate_normalized_content(validators: dict[str, Draft202012Validator]) -> list[str]:
    """Validate every file under contents/*/normalized/ against the schema whose
    ``id`` pattern matches each entry, so new content kinds are covered without
    hardcoding individual data files here."""
    errors: list[str] = []
    for category_dir in sorted((ROOT / "contents").glob("*")):
        if not category_dir.is_dir():
            continue
        id_patterns: list[tuple[re.Pattern[str], Draft202012Validator]] = []
        for schema_path in _category_schema_map(category_dir).values():
            rel = str(schema_path.relative_to(ROOT))
            validator = validators.get(rel)
            if validator is None:
                continue
            pattern = validator.schema.get("properties", {}).get("id", {}).get("pattern")
            if pattern:
                id_patterns.append((re.compile(pattern), validator))

        normalized_dir = category_dir / "normalized"
        if not normalized_dir.is_dir():
            continue
        for data_path in sorted(normalized_dir.rglob("*.yaml")):
            rel_data = str(data_path.relative_to(ROOT))
            data = json_safe(yaml.safe_load(data_path.read_text(encoding="utf-8")) or [])
            items = data if isinstance(data, list) else [data]
            for index, item in enumerate(items):
                item_id = item.get("id") if isinstance(item, dict) else None
                match = next(
                    (
                        v
                        for pat, v in id_patterns
                        if isinstance(item_id, str) and pat.match(item_id)
                    ),
                    None,
                )
                if match is None:
                    errors.append(f"{rel_data} [{index}]: no schema matches id {item_id!r}")
                    continue
                for error in match.iter_errors(item):
                    errors.append(f"{rel_data} [{index}]: {error.message}")
            print(f"data OK: {rel_data}")
    return errors


def main() -> int:
    errors: list[str] = []

    validators: dict[str, Draft202012Validator] = {}
    for pattern in SCHEMA_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            rel = str(path.relative_to(ROOT))
            try:
                schema = json.loads(path.read_text(encoding="utf-8"))
                Draft202012Validator.check_schema(schema)
                validators[rel] = Draft202012Validator(schema, format_checker=FormatChecker())
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

    errors.extend(_validate_normalized_content(validators))

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("all schemas and data valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
