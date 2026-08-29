# 情報セキュリティ管理(Information Security)

> 本書は ISO/IEC 27001 および ISMS の考え方を参考にした実用的な運用ルールであり、
> 認証取得や規格への完全適合を主張するものではありません。

## 目的

学習コンテンツ・ソースデータ・認証情報・個人情報の機密性・完全性・可用性を保護する。

## データ分類

すべてのデータは次の4分類のいずれかに割り当てる
(運用手順は [data-classification](../operations/data-classification.md))。

| 分類 | 例 | Git コミット |
| --- | --- | --- |
| Public | 公開ドキュメント、架空サンプル | 可 |
| Internal | 内部運用ログ、集計レポート | 可(公開リポジトリ化する場合は再評価) |
| Confidential | 契約資料、未確認の教材データ | 不可 |
| Restricted | 認証情報、APIキー、個人情報 | 不可(検出時はインシデント) |

## 必須ルール

1. Restricted / Confidential 情報はコミット・Issue・PR・AIプロンプトのいずれにも含めない
2. 認証情報は環境変数またはローカルの `.env`(Git管理外)で扱う
3. AIサービスへ送信してよいのは Public / Internal 情報のみ
4. 秘密情報の混入を pre-commit(private key 検出)と CI(gitleaks)で検査する
5. 混入を発見した場合は[インシデント管理](incident-management.md)に従う

## アクセス・変更・証跡

- アクセス権限: [access-control](access-control.md)
- 変更の統制: [change-management](change-management.md)
- 証跡の保持: [audit-trail](audit-trail.md)
- リスクの識別と対応: [risk-management](risk-management.md)

## 見直し

セキュリティルールは少なくとも年1回、およびインシデント発生時に見直す。
