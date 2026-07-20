# 変更管理(Change Management)

> ISO 9001 / ISO IEC 27001 の考え方を参考にした運用ルールです(認証・完全適合の主張ではありません)。

## 原則

1. すべての変更は Issue に紐付ける(Issue なしの実装開始は禁止)
2. main ブランチへの直接 push は禁止
3. 変更は Issue → ブランチ → Pull Request → レビュー → マージ の順で行う
4. 変更内容は小さくレビュー可能な単位に分割する

## 変更の流れ

| 段階 | 必須事項 |
| --- | --- |
| 計画 | Issue に Purpose / Scope / Acceptance Criteria / 見積工数 / リスクを記載 |
| 実装 | 命名規則に従うブランチ、Conventional Commits(Issue番号入り) |
| 検証 | CI 成功、テスト証跡を PR に記載 |
| レビュー | 作成者以外のレビュー([review-and-approval](review-and-approval.md)) |
| リリース | マージ後 CHANGELOG 更新、必要に応じタグ付け |

## 緊急変更

セキュリティインシデント対応などの緊急変更でも Issue と PR は必須とする。
事後でよいのは詳細な見積のみとし、実績工数と経緯は必ず記録する。

## ロールバック

- PR には Rollback Plan を記載する
- 破壊的変更・スキーマ変更は PR 内で後方互換性への影響を明示する

## 構成管理

- 依存関係は `pyproject.toml` / `uv.lock` で固定し、変更は PR レビューを通す
- スキーマ(`schemas/`、`contents/*/schemas/`)の変更は影響範囲の記載を必須とする
