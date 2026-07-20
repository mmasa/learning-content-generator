from pathlib import Path

from learning_content_generator.validators.logs import (
    validate_ai_usage,
    validate_work_logs,
)


class TestValidateExamples:
    def test_example_ai_usage_is_valid(self, examples_dir: Path) -> None:
        assert validate_ai_usage(examples_dir / "ai-usage") == []

    def test_example_work_logs_are_valid(self, examples_dir: Path) -> None:
        assert validate_work_logs(examples_dir / "effort") == []


class TestValidateBrokenFiles:
    def test_detects_person_hour_mismatch(self, tmp_path: Path) -> None:
        log = tmp_path / "2026-07.yaml"
        log.write_text(
            """
- date: 2026-07-20
  issue: 1
  work_type: Implementation
  summary: mismatch
  participants:
    - name: A
      hours: 1.0
  elapsed_hours: 1.0
  spent_person_hours: 3.0
  ai_used: false
""",
            encoding="utf-8",
        )
        errors = validate_work_logs(tmp_path)
        assert len(errors) == 1
        assert "does not match" in errors[0]

    def test_detects_missing_fields(self, tmp_path: Path) -> None:
        log = tmp_path / "2026-07.yaml"
        log.write_text("- date: 2026-07-20\n", encoding="utf-8")
        assert validate_work_logs(tmp_path)

    def test_detects_non_list_file(self, tmp_path: Path) -> None:
        log = tmp_path / "bad.yaml"
        log.write_text("just a string\n", encoding="utf-8")
        errors = validate_ai_usage(tmp_path)
        assert len(errors) == 1
        assert "expected a list" in errors[0]

    def test_empty_file_is_valid(self, tmp_path: Path) -> None:
        (tmp_path / "empty.yaml").write_text("", encoding="utf-8")
        assert validate_ai_usage(tmp_path) == []
