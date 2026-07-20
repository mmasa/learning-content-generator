# Contributing Guide

## 変更の基本フロー

すべての変更は次の順で行います。**Issue を作成せずに実装作業を開始しないでください。**

1. **Issue 作成** — [テンプレート](.github/ISSUE_TEMPLATE/)を使い、目的・スコープ・
   Acceptance Criteria・**見積工数(Estimated Person-Hours)** を必ず記入する
2. **ブランチ作成** — 命名規則は下記
3. **実装** — 作業単位ごとに Issue コメントへ Work Log を記録する
4. **Pull Request 作成** — [PRテンプレート](.github/PULL_REQUEST_TEMPLATE.md)の全項目を記入する
5. **レビュー** — 作成者以外によるレビューを必須とする(暫定的な自己レビュー運用は
   [docs/governance/review-and-approval.md](docs/governance/review-and-approval.md) 参照)
6. **マージ** — main への直接 push は禁止

## ブランチ命名

```text
feature/<issue-number>-<short-description>
fix/<issue-number>-<short-description>
docs/<issue-number>-<short-description>
data/<issue-number>-<short-description>
security/<issue-number>-<short-description>
chore/<issue-number>-<short-description>
```

## コミットメッセージ

[Conventional Commits](https://www.conventionalcommits.org/ja/) を基本とし、Issue 番号を含めます。

```text
feat(takken): add question schema (#123)
docs(governance): add AI usage policy (#124)
fix(report): correct person-hour calculation (#125)
```

## 工数記録

- 単位は **person-hours**(`Person-Hours = Elapsed Hours × Number of Participants`)
- 複数人作業では参加者ごとの時間を個別記録し、実績は参加者時間の合計とする
- 形式は [docs/operations/work-logging.md](docs/operations/work-logging.md) を参照

## AI利用記録

生成AI(Claude Code、ChatGPT、Copilot 等)を利用した場合は、必ず AI 利用ログを残します。
トークン数が取得できない場合は `not-provided` 等と明記し、推定値を実測値として扱いません。
詳細は [docs/operations/ai-usage-logging.md](docs/operations/ai-usage-logging.md) を参照してください。

## 開発環境

```bash
uv sync
uv run pre-commit install
```

PR 提出前に以下がすべて成功することを確認してください。

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

## データと著作権

- 著作権・ライセンスが未確認のデータ(実際の過去問本文、規格本文、有償資料の複製など)は
  追加しない
- データを追加する場合は `contents/<name>/metadata/` に出典記録
  ([source-record スキーマ](contents/takken/schemas/source-record.schema.json))を残す
- 秘密情報(APIキー・個人情報等)のコミットは禁止。誤コミット時は
  [インシデント管理](docs/governance/incident-management.md) に従い直ちに報告する
