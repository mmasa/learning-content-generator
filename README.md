# learning-content-generator

資格試験・規格・認定制度・社内教育などの情報から、学習用コンテンツ、構造化データ、
クイズ、読み上げ原稿、音声教材を生成するための共通基盤です。

最初の対象コンテンツは **宅地建物取引士試験(Takken)** です。
将来的に通関士、行政書士、ISO規格、ISO/IEC 27001 / ISMS、Apple / Google /
Microsoft / AWS 関連認定、社内教育、法令読み上げ教材、ポッドキャスト形式教材などを
`contents/` 配下に追加できる構造になっています。

## 基本方針

1. すべての変更は Issue または Task に紐付ける(Issue なしで実装を開始しない)
2. すべての Issue に作業開始前の見積工数(person-hours)を設定する
3. 作業履歴と実績工数を Issue コメントの Work Log に記録する
4. すべての Pull Request は作成者以外によるレビューを必須とする(AI生成物も自動承認しない)
5. AI生成物は必ず人間が内容・権利・正確性・安全性を確認する
6. main ブランチへの直接 push を禁止し、Issue → ブランチ → PR → レビュー → マージの順で変更する
7. 作業記録・AI利用記録・レビュー記録を監査可能な形で保持する

本リポジトリの運用は **ISO 9001 / ISO IEC 27001(ISMS)の考え方を参考にした運用** であり、
ISO 認証の取得や規格への完全適合を主張するものではありません。
詳細は [docs/governance/](docs/governance/) を参照してください。

## はじめて作業する方へ

**[docs/operations/getting-started.md](docs/operations/getting-started.md)** を最初に読んでください。
読むべきドキュメントの順序、セットアップ、作業開始前チェックリスト、禁止事項をまとめています。

## セットアップ

```bash
# 依存関係のインストール(Python 3.12+ / uv が必要)
uv sync

# pre-commit フックの有効化
uv run pre-commit install

# テスト
uv run pytest

# lint / 型検査
uv run ruff check .
uv run mypy
```

## CLI

`lcg` コマンドで工数・AI利用の集計レポートとログ検証を実行できます。

```bash
uv run lcg report ai-usage                # AI利用統計
uv run lcg report effort                  # 工数統計(見積・実績・差異)
uv run lcg report issue --issue 123       # Issue別レポート
uv run lcg report monthly --month 2026-07 # 月別レポート
uv run lcg report contributor --name "Masato Miyaichi"

# 出力形式: --format markdown|json|csv(既定: markdown)
uv run lcg report effort --format csv

# ログ検証(CI でも実行)
uv run lcg validate ai-usage reports/ai-usage
uv run lcg validate work-log reports/effort
```

## ディレクトリ構成

| パス | 内容 |
| --- | --- |
| `docs/governance/` | ISO/ISMS の考え方を参考にした運用ルール |
| `docs/operations/` | Issue運用・作業記録・AI利用記録・レビューの実務手順 |
| `src/learning_content_generator/` | Python パッケージ(CLI・集計・検証・生成基盤) |
| `contents/takken/` | 宅建コンテンツ(スキーマ・架空サンプル・プロンプト) |
| `schemas/` | 共通ログスキーマ(JSON Schema) |
| `prompts/` | 共通プロンプトテンプレート |
| `reports/` | AI利用・工数・品質・セキュリティの実績ログ置き場 |
| `examples/` | 架空データによるログ・レポートのサンプル |

## データ取り扱い上の注意

- APIキー・トークン・個人情報・契約上非公開の資料は **コミット禁止**
- 実際の過去問本文・規格本文など著作権未確認データは `contents/*/raw/` にも **コミットしない**
  (`.gitignore` で除外済み)
- 生成音声・大容量中間ファイルはコミットしない
- データ分類(Public / Internal / Confidential / Restricted)は
  [docs/operations/data-classification.md](docs/operations/data-classification.md) を参照

## 参加方法

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。
AIエージェント(Claude Code 等)向けのルールは [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md) にあります。
