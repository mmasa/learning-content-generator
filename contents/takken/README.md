# 宅地建物取引士試験(Takken)コンテンツ

宅建試験向けの学習コンテンツを管理するディレクトリです。

> **重要**: 実際の過去問本文・市販教材など著作権未確認のデータはコミット禁止です。
> `raw/` と `audio/` は `.gitignore` で Git 管理外になっています。
> 現在含まれるサンプル問題はすべて**架空(fictional)**のデータです。

## 構成

| パス | 内容 | Git管理 |
| --- | --- | --- |
| `config/` | コンテンツ設定(`content.yaml`) | ○ |
| `raw/` | 原データ(過去問・教材など) | **×(README以外は管理外)** |
| `normalized/` | スキーマ準拠の正規化データ(`samples/` は架空サンプル) | ○(著作権確認済みのみ) |
| `generated/` | 生成されたクイズ・解説・読み上げ原稿 | ○(レビュー済みのみ) |
| `audio/` | 生成音声 | **×(メタデータのみ管理)** |
| `prompts/` | 生成用プロンプトテンプレート | ○ |
| `schemas/` | データスキーマ(JSON Schema) | ○ |
| `metadata/` | 出典記録・著作権確認・音声メタデータ | ○ |
| `tests/` | コンテンツ固有の検証データ・テスト | ○ |

## データ形式

1. **入力データ(raw)** — 形式自由。取り込み時に出典記録(`metadata/sources.yaml`、
   スキーマ: `schemas/source-record.schema.json`)を必ず作成する
2. **正規化データ(normalized)** — 問題は `schemas/question.schema.json` に準拠。
   1ファイル = 問題のリスト(YAML または JSON)
3. **読み上げ原稿(generated)** — `schemas/reading-script.schema.json` に準拠
4. **音声メタデータ(metadata)** — `schemas/audio-metadata.schema.json` に準拠。
   音声ファイル本体はコミットせず、`file_path` はローカル/外部ストレージ参照とする

## 検証ルール

- すべての正規化データはスキーマ検証に合格すること(`tests/test_schemas.py` で検証)
- `source.copyright_status` が `unverified` のデータはコミットしない
- `source.type: fictional` のデータには架空であることを明記する
- 問題・正解・解説の整合性を人間がレビューする
  ([レビューチェックリスト](../../docs/templates/content-review-checklist.md))

## 著作権確認欄

各問題の `source` に以下を記録する。

```yaml
source:
  type: fictional          # fictional | original | past-exam | textbook | other
  reference: src-fict-001  # metadata/sources.yaml の id
  year: null
  copyright_status: fictional   # fictional | owned | licensed | public-domain | unverified
  copyright_confirmed_by: "Masato Miyaichi"
  copyright_confirmed_at: "2026-07-20"
```

## 出題分野(field)

| 値 | 分野 |
| --- | --- |
| `rights` | 権利関係(民法等) |
| `laws-restrictions` | 法令上の制限 |
| `tax-appraisal` | 税・価格の評定 |
| `takken-business-law` | 宅建業法 |
| `other` | その他(免除科目等) |
