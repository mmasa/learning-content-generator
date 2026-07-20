# プロンプトテンプレート: 読み上げ原稿生成(Takken)

## 用途

正規化済みの問題データから、TTS用の読み上げ原稿を生成する。

## テンプレート

```text
あなたは音声学習教材のシナリオライターです。
以下の四肢択一問題を、音声で聞いて学習しやすい読み上げ原稿に変換してください。

問題データ(YAML):
{question_yaml}

スタイル: {style}  # lecture(講義調) | drill(演習) | podcast(対話調)

制約:
- 耳で聞いて理解できる自然な日本語にすること(書き言葉の直読みを避ける)
- 数字・記号・法令名には読み仮名指示(reading_notes)を付けること
  例: 「第3条」→「だいさんじょう」
- 問題読み上げ → 考える間(pause) → 正解 → 解説 の順に構成すること
- 出力は contents/takken/schemas/reading-script.schema.json に従うYAMLとすること
- generated_by_ai は true とすること
```

## 生成後の必須作業

1. AI利用ログを `reports/ai-usage/` に記録する
2. 人間が音読または試聴して自然さを確認する(`review.naturalness_checked: true`)
3. 音声生成後は `schemas/audio-metadata.schema.json` に従うメタデータのみコミットする
   (音声ファイル本体はコミットしない)
