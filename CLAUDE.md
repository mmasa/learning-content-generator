# CLAUDE.md

Claude Code 向けのリポジトリ固有ルール。**まず [AGENTS.md](AGENTS.md) の共通ルールに従うこと。**

## 必須フロー(要約)

- 作業前にIssueを確認。なければ実装せずIssue作成を提案する
- 見積工数(Estimated Person-Hours)のないIssueでは実装を開始しない
- Scope外の変更を勝手に加えない
- 完了時に必ず提示する: (1) Work Log案 (2) AI利用ログ案 (3) PR本文案
- テストを実行してから完了報告する。未実行なら「テスト未実行」と明記する
- 生成物の正しさを仮定せず、人間の最終レビューを要求する

## コマンド

```bash
uv sync                                   # セットアップ
uv run pytest                             # テスト
uv run ruff check . && uv run mypy        # lint + 型検査
uv run lcg report effort                  # 工数レポート
uv run lcg validate ai-usage reports/ai-usage   # AI利用ログ検証
uv run lcg validate work-log reports/effort     # 作業ログ検証
```

## AI利用ログ

- 置き場所: `reports/ai-usage/YYYY-MM.yaml`(スキーマ: `schemas/ai-usage-log.schema.json`)
- トークン数: セッションから取得できれば実数を `measurement.type: actual` で記録。
  取得できなければ `not-provided`(数値のでっち上げ禁止)
- 記入例: `examples/ai-usage/2026-07.yaml`

## データ・セキュリティ上の禁止事項

- 秘密情報(APIキー・トークン・個人情報)の出力・コミット
- 実在の過去問本文・規格本文・有償資料など著作権未確認データの追加
- `contents/*/raw/` および `contents/*/audio/` へのファイルコミット(Git管理外)

## コード方針

- Python 3.12+ / uv / Ruff / Mypy(strict)/ Pytest / Pydantic / Typer
- 過度なDDD・Clean Architectureを導入しない。薄いレイヤ構成を維持する
  (構成は [ARCHITECTURE.md](ARCHITECTURE.md) 参照)
- ドキュメントは日本語、コード・コミットメッセージ・スキーマは英語
