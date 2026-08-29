# 作業記録(Work Logging)

## 工数の単位と計算

工数の基本単位は **person-hours**。

```text
Person-Hours = Elapsed Hours × Number of Participants
```

例:

```text
1人 × 1時間 = 1.0 person-hours
2人 × 30分 = 1.0 person-hours
3人 × 20分 = 1.0 person-hours
2人 × 2時間 = 4.0 person-hours
```

複数人で作業した場合は**参加者ごとの作業時間を個別に記録**する。
全員が同じ時間作業したとは限らないため、実績工数は原則として参加者時間の合計で算出する。

```text
Total Person-Hours = Member A Hours + Member B Hours + Member C Hours + ...
```

見積差異は次で計算する(差異率は見積工数が0より大きい場合のみ)。

```text
Variance Hours = Actual Person-Hours - Estimated Person-Hours
Variance Rate  = (Actual - Estimated) ÷ Estimated × 100
```

## 記録方法

### 1. Issue コメント(作業単位ごと)

```markdown
## Work Log

- Date: 2026-07-20
- Task: #123
- Work Type: Implementation
- Summary: 宅建問題データのJSONスキーマを作成
- Participants:
  - Masato Miyaichi: 0.5h
  - Reviewer Name: 0.5h
- Elapsed Time: 0.5h
- Spent: 1.0 person-hours
- AI Used: Yes
- AI Tool: Claude Code
- Result: Draft completed
- Remaining Work: Schema review and test data validation
```

1人の場合の簡易形式(正式記録では構造化形式を推奨):

```text
Spent 1.0h | 2026-07-20 | Masato Miyaichi | Implemented Takken JSON schema
```

### 2. 構造化ログ(集計用・正式記録)

統計集計の単一情報源として `reports/effort/YYYY-MM.yaml` に記録する
(スキーマ: [schemas/work-log.schema.json](../../schemas/work-log.schema.json)、
記入例: [examples/effort/](../../examples/effort/))。

```yaml
- date: 2026-07-20
  issue: 123
  work_type: Implementation
  summary: "Takken question JSON schema"
  participants:
    - name: "Masato Miyaichi"
      hours: 0.5
    - name: "Reviewer Name"
      hours: 0.5
  elapsed_hours: 0.5
  spent_person_hours: 1.0   # participants の合計と一致すること(検証される)
  ai_used: true
  ai_tool: "Claude Code"
  category: takken
  result: "Draft completed"
  remaining_work: "Schema review and test data validation"
```

## Work Type の区分

Implementation / Review / Fix / Meeting / Research / Data Creation /
Documentation / Testing / Incident Response / Other

## 検証と集計

```bash
uv run lcg validate work-log reports/effort   # 形式・工数計算の検証
uv run lcg report effort                      # 見積・実績・差異の集計
```
