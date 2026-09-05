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

## スキーマ変更手順(影響範囲)

`schemas/` 配下のスキーマを変更する際は、[change-management](../../docs/governance/change-management.md)
に従い Issue と PR を通す。影響範囲は以下を確認する。

| 変更内容 | 確認すること |
| --- | --- |
| 必須プロパティの追加・型変更(破壊的) | 既存データ(`normalized/`, `metadata/`)が新スキーマで検証に通るか。通らない場合は移行(マイグレーション)方針をPRに明記する |
| 任意プロパティの追加(非破壊的) | `tests/test_schemas.py` のサンプル検証、`.github/scripts/validate_schemas.py`(`contents/*/normalized/` を動的に走査する)がグリーンであること |
| `id` の pattern 変更 | `validate_schemas.py` は各スキーマの `properties.id.pattern` で対象データを振り分けるため、pattern を変えると振り分けが変わる。既存IDとの整合を確認する |
| `field` / `enum` の値の追加・削除 | `config/content.yaml` の `fields` リストとの整合、既存データへの影響 |
| 新しいコンテンツ種別の追加(スキーマ新設) | `config/content.yaml` の `schemas:` にキーを追加すれば `validate_schemas.py` が自動的に対象データを検出する(ハードコードされたファイルリストは持たない設計) |

実データ投入(Issue #8以降)より前にスキーマを固めることを優先する
(投入後の破壊的変更はリスクが高いため、[risk-management](../../docs/governance/risk-management.md) 参照)。

`source.copyright_status` / `metadata/sources.yaml` の `copyright_status` が
`unverified` のデータをコミットさせない自動チェックは未実装([Issue #12](https://github.com/mmasa/learning-content-generator/issues/12)
で対応予定)。現状はレビュー([content-review-checklist](../../docs/templates/content-review-checklist.md))
での人間確認が唯一の防波堤である。

## 出題分野(field)

| 値 | 分野 |
| --- | --- |
| `rights` | 権利関係(民法等) |
| `laws-restrictions` | 法令上の制限 |
| `tax-appraisal` | 税・価格の評定 |
| `takken-business-law` | 宅建業法 |
| `other` | その他(免除科目等) |
