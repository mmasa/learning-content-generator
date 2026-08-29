# 監査証跡(Audit Trail)

> ISO 9001 / ISO/IEC 27001 の考え方を参考にした運用ルールです(認証・完全適合の主張ではありません)。

## 目的

「誰が・いつ・何を・なぜ・どのように」変更したかを、後から追跡できる状態を維持する。

## 証跡の構成

| 証跡 | 保存場所 | 内容 |
| --- | --- | --- |
| 変更理由・計画 | Issue | 目的、スコープ、見積工数、リスク |
| 作業記録 | Issue コメント + `reports/effort/` | Work Log(参加者別時間、実績工数) |
| AI利用記録 | Issue/PR + `reports/ai-usage/` | モデル、トークン数、費用、レビュー状況 |
| 変更内容 | Git コミット / PR | 差分、Conventional Commits(Issue番号入り) |
| 検証記録 | PR + CI | テスト結果、lint、スキーマ検証 |
| レビュー記録 | PR | 指摘、対応、承認、差戻し理由 |
| インシデント記録 | Issue + `reports/security/` | 検知、対応、再発防止 |

## トレーサビリティ

Issue 番号を軸に、Issue ↔ ブランチ名 ↔ コミットメッセージ ↔ PR ↔ ログファイルを相互参照する。

```text
Issue #123 ← feature/123-question-schema ← "feat(takken): add question schema (#123)"
          ← PR #45 ← reports/ai-usage/2026-07.yaml (issue: 123)
                   ← reports/effort/2026-07.yaml (issue: 123)
```

## 保持ルール

- 証跡は削除しない(誤記は打ち消し訂正し、履歴を残す)
- 構造化ログ(`reports/`)を単一の情報源とし、集計は `lcg report` で導出する
- 秘密情報は証跡にも含めない(必要な場合は参照のみ記録)
