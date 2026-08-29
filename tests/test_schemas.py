"""Validate example data against the JSON Schemas (external contract).

The Pydantic models are the canonical definition; these tests keep the
JSON Schemas in sync with them by checking both accept the same examples.
"""

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
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


def _load_validate_schemas_module(repo_root: Path) -> ModuleType:
    """Import the CI script by path (it lives outside src/, not the package)."""
    spec = importlib.util.spec_from_file_location(
        "validate_schemas", repo_root / ".github/scripts/validate_schemas.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestNormalizedContentDiscovery:
    """Regression coverage for the CI schema-validation script discovering all
    files under contents/*/normalized/ rather than a hardcoded fixture list."""

    def test_sample_questions_are_discovered_via_id_pattern(self, repo_root: Path) -> None:
        module = _load_validate_schemas_module(repo_root)
        validators = {
            rel: Draft202012Validator(json.loads((repo_root / rel).read_text(encoding="utf-8")))
            for rel in [
                "contents/takken/schemas/question.schema.json",
                "contents/takken/schemas/reading-script.schema.json",
                "contents/takken/schemas/audio-metadata.schema.json",
            ]
        }
        errors = module._validate_normalized_content(validators)
        assert errors == []

    def test_unrecognized_id_pattern_is_reported(self, tmp_path: Path, repo_root: Path) -> None:
        module = _load_validate_schemas_module(repo_root)

        # Self-contained fake ROOT: a copy of the real question schema plus a
        # "fake" content category pointing at it, so path resolution doesn't
        # need to escape tmp_path.
        schema_dir = tmp_path / "contents" / "takken" / "schemas"
        schema_dir.mkdir(parents=True)
        schema_text = (repo_root / "contents/takken/schemas/question.schema.json").read_text(
            encoding="utf-8"
        )
        (schema_dir / "question.schema.json").write_text(schema_text, encoding="utf-8")

        category = tmp_path / "contents" / "fake"
        (category / "config").mkdir(parents=True)
        (category / "normalized").mkdir()
        (category / "config" / "content.yaml").write_text(
            "schemas:\n  question: ../../takken/schemas/question.schema.json\n",
            encoding="utf-8",
        )
        (category / "normalized" / "bad.yaml").write_text(
            "- id: not-a-known-prefix-0001\n", encoding="utf-8"
        )

        original_root = module.ROOT
        module.ROOT = tmp_path
        try:
            validators = {
                "contents/takken/schemas/question.schema.json": Draft202012Validator(
                    json.loads(schema_text)
                )
            }
            errors = module._validate_normalized_content(validators)
        finally:
            module.ROOT = original_root
        assert len(errors) == 1
        assert "no schema matches id" in errors[0]
