# 初期Issue案

> **登録済み(2026-07-20)**: 以下の14件は GitHub Issue #1〜#14 として登録済み。
> 本ファイルは登録時の原稿として保存している。最新の状態は
> [GitHub Issues](https://github.com/mmasa/learning-content-generator/issues) を参照。
> 見積は `reports/effort/estimates.yaml` に登録済み。
Reviewer はいずれも暫定として Masato Miyaichi
(自己レビュー運用: [review-and-approval](../governance/review-and-approval.md) の条件に従う)。

---

## 1. Repository bootstrap(Task)

- **Purpose**: リポジトリ初期構造・基本文書・CI・ログ基盤を確立し、以後の作業をIssue駆動にする
- **Deliverables**: 初期構築PR一式(本リポジトリの初期コミット内容)、初期構築のWork Log / AI利用ログ
- **Acceptance Criteria**: CI green / `lcg report`・`lcg validate` が動作 / 全文書がレビュー済み
- **Estimated Person-Hours**: 6.0
- **Risks**: 一括生成による未レビュー箇所の残存
- **Security Considerations**: 秘密情報・実データが含まれないことの確認
- **AI Usage Planned**: Yes(Claude Code による生成、人間レビュー必須)
- **Reviewer**: Masato Miyaichi(自己レビュー・12時間以上空ける)

## 2. Governance documents(Documentation)

- **Purpose**: ISO/ISMSの考え方を参考にした運用ルール10文書の内容レビューと確定
- **Deliverables**: `docs/governance/` 10文書のレビュー済み版
- **Acceptance Criteria**: 全文書レビュー完了 / 「認証・完全適合を主張しない」表現の確認 / 相互リンク整合
- **Estimated Person-Hours**: 3.0
- **Risks**: 実運用と乖離した過剰な形式化
- **Security Considerations**: なし(Public/Internal文書のみ)
- **AI Usage Planned**: Yes(ドラフト生成済み、レビューは人間)
- **Reviewer**: Masato Miyaichi

## 3. AI usage logging(Feature)

- **Purpose**: AI利用ログの運用開始(記録手順の確立と初回ログの登録)
- **Deliverables**: `reports/ai-usage/2026-07.yaml`(初期構築分)、記録手順の確定
- **Acceptance Criteria**: `lcg validate ai-usage reports/ai-usage` 合格 / トークン実測値または not-provided が記録されている
- **Estimated Person-Hours**: 1.5
- **Risks**: 記録漏れ・推定値と実測値の混同
- **Security Considerations**: プロンプト・ログに秘密情報を含めない
- **AI Usage Planned**: No
- **Reviewer**: Masato Miyaichi

## 4. Human work logging(Feature)

- **Purpose**: Work Log 運用の開始(初期構築分の実績記録)
- **Deliverables**: `reports/effort/2026-07.yaml`、`reports/effort/estimates.yaml`(初期Issue分)
- **Acceptance Criteria**: `lcg validate work-log reports/effort` 合格 / person-hours が参加者別時間の合計と一致
- **Estimated Person-Hours**: 1.0
- **Risks**: 記録の後回しによる精度低下
- **Security Considerations**: なし
- **AI Usage Planned**: No
- **Reviewer**: Masato Miyaichi

## 5. Effort reporting(Feature)

- **Purpose**: `lcg report` の出力内容の実運用検証と不足集計の洗い出し
- **Deliverables**: レポート出力例(`reports/quality/` に月次レポート試行)、改善Issueリスト
- **Acceptance Criteria**: issue/monthly/contributor 各レポートが実データで正しい値を出す
- **Estimated Person-Hours**: 2.0
- **Risks**: 集計仕様の解釈違い(差異率・承認率の定義)
- **Security Considerations**: なし
- **AI Usage Planned**: Undecided
- **Reviewer**: Masato Miyaichi

## 6. GitHub Actions validation(Task)

- **Purpose**: CI(lint/型/テスト/スキーマ/ログ/シークレット/依存/PR検証)の実環境動作確認
- **Deliverables**: 全ワークフローの成功実績、ブランチ保護設定(main直push禁止・レビュー必須)
- **Acceptance Criteria**: PRで全ジョブが動作 / 不備PRが正しく fail する / ブランチ保護有効
- **Estimated Person-Hours**: 2.5
- **Risks**: Actionsのバージョン非互換、gitleaks等の誤検知
- **Security Considerations**: Actions Secrets の最小化、権限は read 基本
- **AI Usage Planned**: Undecided
- **Reviewer**: Masato Miyaichi

## 7. Takken data schema(Feature)

- **Purpose**: 宅建の問題・読み上げ原稿・音声メタデータ・出典記録スキーマの内容確定
- **Deliverables**: `contents/takken/schemas/` 4スキーマのレビュー済み版、スキーマ変更手順
- **Acceptance Criteria**: 実運用を想定したレビュー完了 / サンプルがスキーマ検証合格 / 変更時の影響範囲が文書化
- **Estimated Person-Hours**: 3.0
- **Risks**: 実データ投入後のスキーマ破壊的変更
- **Security Considerations**: copyright_status: unverified のコミット防止策の検討
- **AI Usage Planned**: Yes(ドラフト生成済み)
- **Reviewer**: Masato Miyaichi

## 8. Takken sample content(Data Creation)

- **Purpose**: 架空サンプル問題の拡充(各分野1問以上)とレビュー運用の試行
- **Deliverables**: 架空サンプル問題(4分野)、レビュー記録、AI利用ログ
- **Acceptance Criteria**: すべて `source.type: fictional` / スキーマ検証合格 / チェックリストによるレビュー完了
- **Estimated Person-Hours**: 4.0
- **Risks**: 架空のつもりが実在過去問に酷似する可能性
- **Security Considerations**: 実在問題の混入防止(生成プロンプトの制約とレビュー)
- **AI Usage Planned**: Yes
- **Reviewer**: Masato Miyaichi

## 9. Takken text normalization(Feature)

- **Purpose**: 原データを正規化データへ変換する normalizer の最小実装
- **Deliverables**: `normalizers/` 実装、単体テスト、正規化手順文書
- **Acceptance Criteria**: 架空サンプル入力で正規化データが生成されスキーマ検証合格 / テストあり
- **Estimated Person-Hours**: 6.0
- **Risks**: 入力形式の多様性への過剰対応(スコープ肥大)
- **Security Considerations**: raw データを処理してもGit管理下へ出力しない設計
- **AI Usage Planned**: Yes
- **Reviewer**: Masato Miyaichi

## 10. Takken reading-script generation(Feature)

- **Purpose**: 正規化問題から読み上げ原稿を生成する generator の最小実装
- **Deliverables**: `generators/` 実装、プロンプト確定版、生成サンプル(架空問題ベース)、テスト
- **Acceptance Criteria**: 架空サンプルから reading-script スキーマ準拠の原稿が生成される / 人間が自然さを確認
- **Estimated Person-Hours**: 8.0
- **Risks**: 読み上げ品質の主観差、LLM出力の不安定さ
- **Security Considerations**: LLM送信内容は Public/Internal のみ / AI利用ログ必須
- **AI Usage Planned**: Yes
- **Reviewer**: Masato Miyaichi

## 11. TTS provider abstraction(Feature)

- **Purpose**: TTSプロバイダ抽象の実装と最初のプロバイダ接続
- **Deliverables**: `tts/` 実装、音声メタデータ生成、認証情報の環境変数管理手順
- **Acceptance Criteria**: 架空サンプル原稿から音声を生成しメタデータのみコミット / 認証情報が環境変数のみ
- **Estimated Person-Hours**: 8.0
- **Risks**: プロバイダ選定・コスト、音声ファイル管理の運用不備
- **Security Considerations**: TTS認証情報のコミット禁止 / 音声のGit管理外化の維持
- **AI Usage Planned**: Yes
- **Reviewer**: Masato Miyaichi

## 12. Copyright and source management(Task)

- **Purpose**: 実データ導入前に出典・著作権確認フローを確定する
- **Deliverables**: 出典確認手順書、source-record 運用ルール、unverified 検出の自動チェック(CI)
- **Acceptance Criteria**: 手順書レビュー完了 / unverified データのコミットをCIが検出して fail する
- **Estimated Person-Hours**: 4.0
- **Risks**: 権利判断の誤り(法的リスク)
- **Security Considerations**: Confidential データの取り扱い手順を含める
- **AI Usage Planned**: Undecided
- **Reviewer**: Masato Miyaichi

## 13. Security review(Task)

- **Purpose**: 初期構築全体のセキュリティレビュー(秘密情報・権限・CI・依存)
- **Deliverables**: レビュー結果(`reports/security/`)、改善Issue、リスク一覧の更新
- **Acceptance Criteria**: チェック項目全件確認 / 検出事項がIssue化されている / gitleaks・pip-audit green
- **Estimated Person-Hours**: 3.0
- **Risks**: 個人開発による確認の形骸化
- **Security Considerations**: 本Issue自体が対策(2FA・ブランチ保護・Secrets棚卸しを含む)
- **AI Usage Planned**: Yes(補助として。判断は人間)
- **Reviewer**: Masato Miyaichi

## 14. Initial release preparation(Task)

- **Purpose**: v0.1.0 としての初期リリース準備(タグ付け・CHANGELOG確定・残課題整理)
- **Deliverables**: CHANGELOG 0.1.0、リリースタグ、未完了項目のIssue化、LICENSE方針の決定
- **Acceptance Criteria**: 完了条件チェックリスト(初期構築指示 §17)を全件確認 / 残課題がすべてIssue化
- **Estimated Person-Hours**: 2.0
- **Risks**: 未完了項目の見落とし
- **Security Considerations**: 公開範囲(private維持/公開)の判断とデータ分類の再確認
- **AI Usage Planned**: Undecided
- **Reviewer**: Masato Miyaichi
