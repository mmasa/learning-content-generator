# ログ形式仕様

## 概要

運用ログは Git 管理の構造化ファイルを単一の情報源とする。

| ログ | 置き場所 | 形式 | スキーマ |
| --- | --- | --- | --- |
| AI利用ログ | `reports/ai-usage/YYYY-MM.yaml` または `.jsonl` | エントリのリスト | `schemas/ai-usage-log.schema.json` |
| 作業ログ | `reports/effort/YYYY-MM.yaml` | エントリのリスト | `schemas/work-log.schema.json` |
| 見積 | `reports/effort/estimates.yaml` | エントリのリスト | `schemas/issue-estimate.schema.json` |

Pydantic モデル(`src/learning_content_generator/domain/models.py`)が実装上の正であり、
JSON Schema は外部ツール連携・CI検証用に同内容を表現する。両者が乖離した場合は Issue 化する。

## 共通ルール

- 日付は ISO 8601(date: `YYYY-MM-DD`、datetime: タイムゾーン付き)
- 人名は表記を統一する(集計キーになるため)
- `category` はコンテンツカテゴリ(`takken` など、`contents/` のディレクトリ名と一致させる)

## トークン数の値

`input` / `cached_input` / `output` / `reasoning` / `total` は次のいずれか。

- 非負整数(実測または推定値)
- `"unknown"` — 値が存在するはずだが不明
- `"not-provided"` — サービスが提供していない
- `"estimated"` — 数値ではなく「推定であること」だけを示す場合

`measurement.type`(`actual` / `estimated` / `unknown`)で計測区分を必ず示す。

## 工数の検証規則

`lcg validate work-log` は以下を検査する。

1. スキーマ準拠(必須項目・型)
2. `spent_person_hours` = 参加者 `hours` の合計(許容誤差 0.01)
3. `hours` >= 0、`elapsed_hours` >= 0
4. `ai_used: true` の場合 `ai_tool` が記載されていること
