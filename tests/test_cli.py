import json
from pathlib import Path

from typer.testing import CliRunner

from learning_content_generator.cli.main import app

runner = CliRunner()


class TestReportCommands:
    def test_report_ai_usage_markdown(self, examples_dir: Path) -> None:
        result = runner.invoke(app, ["report", "ai-usage", "--data-dir", str(examples_dir)])
        assert result.exit_code == 0
        assert "## AI Usage by Issue" in result.output
        assert "#123" in result.output

    def test_report_effort_json(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app, ["report", "effort", "--data-dir", str(examples_dir), "--format", "json"]
        )
        assert result.exit_code == 0
        payload = json.loads(result.output)
        titles = [table["title"] for table in payload]
        assert "Effort by Issue" in titles

    def test_report_effort_csv(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app, ["report", "effort", "--data-dir", str(examples_dir), "--format", "csv"]
        )
        assert result.exit_code == 0
        assert "# Effort by Issue" in result.output

    def test_report_issue(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app, ["report", "issue", "--issue", "123", "--data-dir", str(examples_dir)]
        )
        assert result.exit_code == 0
        assert "Work Log for Issue #123" in result.output

    def test_report_monthly(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app, ["report", "monthly", "--month", "2026-07", "--data-dir", str(examples_dir)]
        )
        assert result.exit_code == 0

    def test_report_monthly_rejects_bad_month(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app, ["report", "monthly", "--month", "July", "--data-dir", str(examples_dir)]
        )
        assert result.exit_code == 2

    def test_report_contributor(self, examples_dir: Path) -> None:
        result = runner.invoke(
            app,
            [
                "report",
                "contributor",
                "--name",
                "Masato Miyaichi",
                "--data-dir",
                str(examples_dir),
            ],
        )
        assert result.exit_code == 0
        assert "Work Entries for Masato Miyaichi" in result.output


class TestValidateCommands:
    def test_validate_ai_usage_ok(self, examples_dir: Path) -> None:
        result = runner.invoke(app, ["validate", "ai-usage", str(examples_dir / "ai-usage")])
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_validate_work_log_ok(self, examples_dir: Path) -> None:
        result = runner.invoke(app, ["validate", "work-log", str(examples_dir / "effort")])
        assert result.exit_code == 0

    def test_validate_missing_path_fails(self, tmp_path: Path) -> None:
        result = runner.invoke(app, ["validate", "ai-usage", str(tmp_path / "nope")])
        assert result.exit_code == 1

    def test_validate_invalid_file_fails(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.yaml"
        bad.write_text("- date: 2026-07-20\n", encoding="utf-8")
        result = runner.invoke(app, ["validate", "ai-usage", str(bad)])
        assert result.exit_code == 1
