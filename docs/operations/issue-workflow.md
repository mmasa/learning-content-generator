# Issue運用

## 原則

- すべての作業は Issue 単位で管理する。**Issue を作成せずに実装作業を開始しない**
- すべての Issue に**作業開始前の見積工数(Estimated Person-Hours)** を設定する
- 作業中は Work Log([work-logging](work-logging.md))を Issue コメントへ記録する

## Issue に記載する項目

[Issueテンプレート](../../.github/ISSUE_TEMPLATE/)は以下の項目を持つ。

| 項目 | 説明 |
| --- | --- |
| Task ID | Issue番号を使用(外部タスクがある場合はそのIDを併記) |
| Title | 変更内容が分かる簡潔な題名 |
| Purpose | 何のために行うか |
| Background | 経緯・前提 |
| Scope / Out of Scope | 対象範囲と対象外 |
| Deliverables | 成果物 |
| Acceptance Criteria | 完了判定条件(検証可能な形で) |
| Risks / Security Considerations | リスクとセキュリティ上の考慮 |
| Data Classification | Public / Internal / Confidential / Restricted |
| Assignee / Reviewer | 担当者とレビュアー |
| Planned Start / End Date | 予定期間 |
| Estimated Person-Hours | 見積工数(**着手前に必須**) |
| Actual Person-Hours | 実績工数(Work Log の合計、完了時に確定) |
| AI Usage Planned | AI利用予定の有無と用途 |
| Related Issues / Pull Requests | 関連リンク |

## テンプレート一覧

Feature / Task / Bug / Documentation / Data Creation / Content Review /
Security Incident / Improvement Proposal

## 見積の登録

集計のため、見積は Issue 本文に加えて `reports/effort/estimates.yaml` にも登録する。

```yaml
- issue: 123
  title: "Takken question schema"
  estimated_person_hours: 4.0
  category: takken
  assignee: "Masato Miyaichi"
```

## ライフサイクル

Open(見積記入)→ In Progress(Work Log記録)→ PR作成 → レビュー →
マージ → 実績工数確定 → Close
