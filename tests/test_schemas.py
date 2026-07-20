"""Validate example data against the JSON Schemas (external contract).

The Pydantic models are the canonical definition; these tests keep the
JSON Schemas in sync with them by checking both accept the same examples.
"""

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator


def load_schema(repo_root: Path, relative: str) -> Draft202012Validator:
    schema = json.loads((repo_root / relative).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class TestLogSchemas:
    def test_ai_usage_example_matches_schema(self, repo_root: Path) -> None:
        validator = load_schema(repo_root, "schemas/ai-usage-log.schema.json")
        data = load_yaml(repo_root / "examples/ai-usage/2026-07.yaml")
        # YAML may parse datetimes as objects; serialize to JSON types first
        normalized = json.loads(json.dumps(data, default=str))
        errors = list(validator.iter_errors(normalized))
        assert errors == [], [e.message for e in errors]

    def test_work_log_example_matches_schema(self, repo_root: Path) -> None:
        validator = load_schema(repo_root, "schemas/work-log.schema.json")
        data = json.loads(
            json.dumps(load_yaml(repo_root / "examples/effort/2026-07.yaml"), default=str)
        )
        errors = list(validator.iter_errors(data))
        assert errors == [], [e.message for e in errors]

    def test_estimates_example_matches_schema(self, repo_root: Path) -> None:
        validator = load_schema(repo_root, "schemas/issue-estimate.schema.json")
        data = load_yaml(repo_root / "examples/effort/estimates.yaml")
        errors = list(validator.iter_errors(data))
        assert errors == [], [e.message for e in errors]


class TestTakkenSchemas:
    @pytest.mark.parametrize(
        "schema_file",
        [
            "contents/takken/schemas/question.schema.json",
            "contents/takken/schemas/reading-script.schema.json",
            "contents/takken/schemas/audio-metadata.schema.json",
            "contents/takken/schemas/source-record.schema.json",
        ],
    )
    def test_schemas_are_valid(self, repo_root: Path, schema_file: str) -> None:
        load_schema(repo_root, schema_file)

    def test_sample_questions_match_schema(self, repo_root: Path) -> None:
        validator = load_schema(repo_root, "contents/takken/schemas/question.schema.json")
        data = load_yaml(repo_root / "contents/takken/normalized/samples/sample-questions.yaml")
        normalized = json.loads(json.dumps(data, default=str))
        errors = [e for item in normalized for e in validator.iter_errors(item)]
        assert errors == [], [e.message for e in errors]

    def test_sample_questions_are_fictional(self, repo_root: Path) -> None:
        data = load_yaml(repo_root / "contents/takken/normalized/samples/sample-questions.yaml")
        for question in data:
            assert question["source"]["type"] == "fictional"
