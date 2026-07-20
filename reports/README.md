# reports/

運用の実績ログ置き場です。**ここが統計の単一情報源**であり、
`uv run lcg report ...` はこのディレクトリを集計します。

| パス | 内容 | 形式 |
| --- | --- | --- |
| `ai-usage/YYYY-MM.yaml` | AI利用ログ | `schemas/ai-usage-log.schema.json` |
| `effort/YYYY-MM.yaml` | 作業ログ(Work Log) | `schemas/work-log.schema.json` |
| `effort/estimates.yaml` | Issue別見積工数 | `schemas/issue-estimate.schema.json` |
| `quality/` | 品質記録(レビュー集計・差戻し等の要約) | 自由(Markdown推奨) |
| `security/` | セキュリティ記録(インシデント要約・棚卸し) | 自由(Markdown推奨) |

記入例は `examples/` を参照。CI が `lcg validate` で形式と工数計算を検証します。
秘密情報・個人情報はログにも記載しないでください。
