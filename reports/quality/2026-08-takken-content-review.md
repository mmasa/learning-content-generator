# 宅建サンプルコンテンツ レビュー記録(Issue #8)

`docs/templates/content-review-checklist.md` に基づき、新規追加した2問
(`takken-q-sample-0003`, `takken-q-sample-0004`)をレビューした記録。

## 対象

| id | field | 状態 |
| --- | --- | --- |
| `takken-q-sample-0003` | laws-restrictions(高さ制限地区・架空都市計画法) | 新規、承認 |
| `takken-q-sample-0004` | tax-appraisal(架空不動産取得税) | 新規、承認 |
| `takken-q-sample-0001` | takken-business-law | 既存(変更なし) |
| `takken-q-sample-0002` | rights | 既存(変更なし) |

これで `rights` / `laws-restrictions` / `tax-appraisal` / `takken-business-law`
の4分野すべてに1問以上が揃った。

## チェックリスト結果

### 正確性

- [x] 問題文・選択肢・正解・解説が相互に整合している(2問とも `uv run pytest`
  でスキーマ検証済み、`correct_choice` と `choice_explanations` の対応を目視確認)
- [ ] 法令・規格・技術情報が現行の内容と一致している — **対象外**。
  両問とも「架空都市計画法」「架空不動産取得税」という架空の法制度を設例として
  用いており、実在の都市計画法・建築基準法・地方税法の規定とは意図的に異なる
  数値・要件にしている(高さ上限15m、課税標準の扱い等)。実在過去問との類似リスク
  ([risk-management](../../docs/governance/risk-management.md) 参照)を下げる狙い
- [x] 誤字脱字・不自然な日本語がない
- [x] 難易度・タグ・カテゴリの設定が妥当である(`medium`、`field` 一致)

### 権利・出典

- [x] 出典記録(source record)が存在する(`metadata/sources.yaml` の
  `src-fictional-samples` を参照)
- [x] 著作権確認欄(copyright_status)が記入済みである(`fictional`)
- [x] 実在の過去問・規格本文の無断転載が含まれていない(ゼロから作成した架空設例)
- [x] サンプル・架空データには fictional であることが明記されている
  (`source.type: fictional`、問題文冒頭に「(架空の設例)」明記)

### AI生成物

- [x] AI生成箇所が明示されている(`generated_by_ai: true`)
- [x] AI利用ログが記録されている(`reports/ai-usage/2026-08.yaml`、issue 8)
- [x] 人間が内容の正確性を確認した — Claude Codeが2問をドラフトし、
  セッション内でユーザー(Masato Miyaichi)が個別に内容を確認して承認した
  (AIレビューのみで完了していない)

### 読み上げ・音声(該当時)

対象外(読み上げ原稿・音声はIssue #10/#11で扱う。本Issueは正規化データのみ)

### データ

- [x] スキーマ検証に合格している(`uv run python .github/scripts/validate_schemas.py`)
- [x] データ分類(Data Classification)が設定されている(`Public`)
- [x] 秘密情報・個人情報が含まれていない

## 結論

Acceptance Criteria 3件を満たした。

- [x] すべて `source.type: fictional`
- [x] スキーマ検証合格
- [x] content-review-checklist によるレビュー完了
