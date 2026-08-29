# AI利用記録(AI Usage Logging)

## 対象

Claude Code、ChatGPT、Codex、GitHub Copilot、Gemini、その他の生成AIを利用した
すべての作業。

## 記録項目

日時 / Issue番号 / PR番号 / 操作者 / プロバイダ / 製品 / モデル名 / 目的 /
入力・出力・キャッシュ入力・推論トークン数 / 総トークン数 / 推定費用・通貨 /
プロンプト(または参照)/ 生成ファイル / 人間レビュー状況・レビュアー・結果 / 備考

## トークン数のルール

- 取得できる CLI/API では**可能な限り自動取得**して実数を記録し、
  `measurement.type: actual` とする
- 取得できない場合は `unknown` / `not-provided` / `estimated` のいずれかを記録する
- **推定値を実測値として扱わない**(推定なら `measurement.type: estimated`)

## 記録場所

単一の構造化ログを情報源とし、同じ情報の手動重複入力を避ける。

1. **正式記録**: `reports/ai-usage/YYYY-MM.yaml`(または `.jsonl`)
   - スキーマ: [schemas/ai-usage-log.schema.json](../../schemas/ai-usage-log.schema.json)
   - 記入例: [examples/ai-usage/2026-07.yaml](../../examples/ai-usage/2026-07.yaml)
2. Issue コメント / PR 本文: 正式記録の要約または参照を記載
3. 集計レポート: `lcg report ai-usage`(GitHub Actions でも検証・集計)

## 記録例

```yaml
- date: 2026-07-20T14:30:00+09:00
  issue: 123
  pull_request: 45
  operator: "Masato Miyaichi"
  provider: Anthropic
  product: "Claude Code"
  model: claude-fable-5
  purpose: "repository scaffolding"
  category: takken
  tokens:
    input: 12000
    cached_input: 5000
    output: 4200
    reasoning: not-provided
    total: 16200
  measurement:
    type: actual
  cost:
    amount: 0.0
    currency: USD
    type: unknown
  prompt_reference: prompts/repository-bootstrap.md
  generated_files:
    - README.md
    - CONTRIBUTING.md
  human_review:
    status: pending
    reviewer: null
    result: null
  notes: "Initial repository generation"
```

## 検証と集計

```bash
uv run lcg validate ai-usage reports/ai-usage
uv run lcg report ai-usage
uv run lcg report issue --issue 123
uv run lcg report monthly --month 2026-07
```

## 禁止事項

- 秘密情報・個人情報・著作権未確認データをAIサービスへ送信しない
  ([information-security](../governance/information-security.md))
- AI生成物を人間レビューなしで承認しない
