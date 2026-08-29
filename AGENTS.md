# AGENTS.md — AIエージェント共通ルール

このリポジトリで作業するすべてのAIエージェント(Claude Code、Codex、Copilot、Gemini 等)は
以下を厳守してください。Claude Code 固有の補足は [CLAUDE.md](CLAUDE.md) にあります。

## 作業開始前

1. **Issueを確認する。** 対応するIssueがなければ、実装を始めずにIssue作成を提案する
2. **見積工数(Estimated Person-Hours)がないIssueでは実装を開始しない**
3. Issueの Scope / Out of Scope を確認し、**作業対象外の変更を勝手に加えない**

## 作業中

4. 秘密情報(APIキー・トークン・個人情報)を出力・コミットしない
5. 実データ(過去問本文・規格本文・有償資料など著作権未確認データ)を無断で追加しない
6. 著作権やライセンスが不明なデータを追加しない
7. 推測と確認済み事実を区別して報告する(推測には「推測」と明記)

## 作業完了時

8. **AI利用ログを残す**(`reports/ai-usage/`、形式は `schemas/ai-usage-log.schema.json`)
   - トークン量を取得可能な場合は記録する
   - 取得できない場合は `not-provided` と記録する(推定値を実測値として扱わない)
9. **Work Log案を提示する**(形式は `docs/operations/work-logging.md`)
10. **Pull Request本文案を作成する**(`.github/PULL_REQUEST_TEMPLATE.md` の全項目)
11. **必ずテストを実行する**(`uv run pytest`、lint: `uv run ruff check .`、型: `uv run mypy`)
    - テストしていない場合はその旨を明記する
12. 自分の生成物を正しいと仮定しない。**人間による最終レビューを要求する**

## 開発コマンド

```bash
uv sync                 # 依存関係
uv run pytest           # テスト
uv run ruff check .     # lint
uv run mypy             # 型検査
uv run lcg --help       # CLI
```

## 変更フロー

Issue → ブランチ(`feature/<issue>-<desc>` 等)→ Conventional Commits(Issue番号必須)→
PR → 人間レビュー → マージ。main への直接 push は禁止。
詳細: [CONTRIBUTING.md](CONTRIBUTING.md)
