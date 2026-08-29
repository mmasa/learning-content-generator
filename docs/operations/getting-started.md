# 作業開始ガイド(Getting Started)

このリポジトリをcloneして作業を始めるときは、まずこのページを読んでください。

## 1. 最初に読むもの(この順で)

| 順 | ドキュメント | 内容 | 所要目安 |
| --- | --- | --- | --- |
| 1 | このページ | 作業の流れ全体 | 5分 |
| 2 | [README.md](../../README.md) | プロジェクト概要・基本方針 | 5分 |
| 3 | [CONTRIBUTING.md](../../CONTRIBUTING.md) | 変更フロー・ブランチ・コミット規約 | 10分 |
| 4 | [issue-workflow.md](issue-workflow.md) | Issueの書き方・見積の登録 | 5分 |
| 5 | [work-logging.md](work-logging.md) | 工数(person-hours)の記録方法 | 5分 |
| 6 | [ai-usage-logging.md](ai-usage-logging.md) | AI利用時のログ記録(AI使用時のみ) | 5分 |

ガバナンス文書([docs/governance/](../governance/))は最初に通読する必要はありません。
レビュー・セキュリティ・インシデント対応など、該当する場面で参照すれば十分です。
AIエージェント(Claude Code等)を使う場合、エージェントは [AGENTS.md](../../AGENTS.md) /
[CLAUDE.md](../../CLAUDE.md) のルールに従います。

## 2. 環境セットアップ

前提: Python 3.12+ と [uv](https://docs.astral.sh/uv/) がインストール済みであること。

```bash
git clone git@github.com:mmasa/learning-content-generator.git
cd learning-content-generator
uv sync                      # 依存関係のインストール
uv run pre-commit install    # コミット時の自動チェックを有効化
uv run pytest                # 動作確認(全テストが通ればOK)
```

## 3. 作業開始前チェックリスト

**Issueなしで実装を始めないこと。** 作業前に必ず確認します。

- [ ] 対応する **Issue がある**(なければ [テンプレート](../../.github/ISSUE_TEMPLATE/) で作成)
- [ ] Issue に **Estimated Person-Hours(見積工数)** が記入されている
- [ ] 見積が `reports/effort/estimates.yaml` にも登録されている
- [ ] Scope / Out of Scope を理解した(**対象外の変更はしない**)
- [ ] 扱うデータの分類を確認した([data-classification.md](data-classification.md))

## 4. 作業の流れ

```text
Issue確認 → ブランチ作成 → 実装 → Work Log記録 → PR作成 → レビュー → マージ
```

1. **ブランチ作成**: `feature/<issue番号>-<説明>`(他に fix/ docs/ data/ security/ chore/)
2. **実装**: コミットは Conventional Commits + Issue番号
   (例: `feat(takken): add question schema (#7)`)
3. **作業記録**: 作業単位ごとに Issue コメントへ Work Log、正式記録は
   `reports/effort/YYYY-MM.yaml` へ([テンプレート](../templates/work-log.md))
4. **AI利用時**: `reports/ai-usage/YYYY-MM.yaml` へ記録
   (トークン数は実測または `not-provided`。[テンプレート](../templates/ai-usage-log.yaml))
5. **PR作成前**: 以下がすべて通ることを確認

   ```bash
   uv run ruff check . && uv run ruff format --check .
   uv run mypy
   uv run pytest
   uv run lcg validate work-log reports/effort
   uv run lcg validate ai-usage reports/ai-usage   # AI利用時
   ```

6. **PR**: [PRテンプレート](../../.github/PULL_REQUEST_TEMPLATE.md)の全セクションを記入
   (CIが未記入を検出して fail します)。レビューは作成者以外
   (暫定の自己レビュー条件は [review-and-approval](../governance/review-and-approval.md))

## 5. 絶対にやらないこと

- **main への直接 push**(ブランチ保護対象)
- **秘密情報のコミット**: APIキー・トークン・パスワード・個人情報・`.env`
- **著作権未確認データのコミット**: 実在の過去問本文・規格本文・有償資料
  (原データは `contents/*/raw/` に置く=Git管理外。出典は `metadata/sources.yaml` に記録)
- **音声ファイルのコミット**(メタデータのみ管理)
- **AI生成物の無レビューマージ**(AI出力も人間が内容・権利・正確性を確認)

## 6. よく使うコマンド

```bash
uv run lcg report effort                  # 工数レポート(見積・実績・差異)
uv run lcg report ai-usage                # AI利用統計
uv run lcg report issue --issue 7         # Issue別レポート
uv run lcg report monthly --month 2026-07 # 月別レポート
uv run lcg --help                         # その他のコマンド
```

## 7. 困ったとき

| 状況 | 参照先 |
| --- | --- |
| 秘密情報をコミットしてしまった | [incident-management.md](../governance/incident-management.md)(まず認証情報を無効化) |
| データの著作権が不明 | 追加しない。[contents/takken/README.md](../../contents/takken/README.md) の出典記録手順 |
| レビューの観点が分からない | PRテンプレートのチェックリスト、[content-review-checklist](../templates/content-review-checklist.md) |
| 全体構成を知りたい | [ARCHITECTURE.md](../../ARCHITECTURE.md) |
| 今後の予定 | [ROADMAP.md](../../ROADMAP.md)、[GitHub Issues](https://github.com/mmasa/learning-content-generator/issues) |
