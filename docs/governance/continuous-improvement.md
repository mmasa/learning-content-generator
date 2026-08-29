# 継続的改善(Continuous Improvement)

> ISO 9001 の考え方(PDCA)を参考にした運用ルールです(認証・完全適合の主張ではありません)。

## 目的

運用データ(工数・AI利用・品質・インシデント)から改善点を見つけ、仕組みに反映する。

## 改善サイクル

1. **Plan** — Issue で目的・Acceptance Criteria・見積工数を定義する
2. **Do** — 実装し、Work Log / AI利用ログを記録する
3. **Check** — `lcg report` による集計と PR レビューで結果を評価する
4. **Act** — Improvement Proposal テンプレートで改善 Issue を作成し、ルール・CI・文書へ反映する

## 定期レビュー(月次目安)

以下を確認し、気づきを Improvement Proposal として起票する。

- 見積差異(`Variance Hours` / `Variance Rate`)の傾向
- AI利用コスト・トークン量の推移(モデル別・カテゴリ別)
- AI利用あり/なしの作業時間比較、AI生成物の差戻し件数・承認率
- CI 失敗の傾向、レビュー指摘の傾向
- インシデント・ヒヤリハットの有無

## 改善の記録

- 改善提案 → Issue(Improvement Proposal)
- 採否と理由 → Issue コメント
- 実施結果 → PR と CHANGELOG

小さな改善(誤字修正やスクリプトの微修正など)も Issue に紐付け、証跡を維持する。
