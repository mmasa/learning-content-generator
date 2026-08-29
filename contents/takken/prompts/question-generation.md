# プロンプトテンプレート: 練習問題生成(Takken)

## 用途

正規化済みの学習トピックから、四肢択一の練習問題を生成する。
**実在の過去問を再現・複製させない。** 生成物は必ず人間がレビューする。

## テンプレート

```text
あなたは宅地建物取引士試験の教材作成者です。
以下のトピックについて、四肢択一の練習問題を{count}問作成してください。

トピック: {topic}
分野: {field}  # rights | laws-restrictions | tax-appraisal | takken-business-law
難易度: {difficulty}

制約:
- 実在の試験問題を再現・改変したものを出力しないこと
- 問題文・4つの選択肢・正解番号・解説・各選択肢の解説を含めること
- 正解は1つだけであり、解説と矛盾しないこと
- 法令に基づく場合は根拠条文と基準日を明記すること
- 出力は contents/takken/schemas/question.schema.json に従うYAMLとすること
- source.type は "original"、generated_by_ai は true とすること
```

## 生成後の必須作業

1. AI利用ログを `reports/ai-usage/` に記録する
2. `review.status: pending` として保存し、人間レビュー
   ([チェックリスト](../../../docs/templates/content-review-checklist.md))を実施する
3. 問題・正解・解説の整合と法令の正確性を確認してから `approved` にする
