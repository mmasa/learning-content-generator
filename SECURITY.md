# Security Policy

## 報告方法

脆弱性・秘密情報の漏えい・不審な挙動を発見した場合は、公開 Issue にせず、
リポジトリオーナー(Masato Miyaichi)へ非公開で連絡してください。
対応は [docs/governance/incident-management.md](docs/governance/incident-management.md)
に従って記録します。緊急の場合は Security Incident テンプレートで
**秘密情報そのものを含めずに** Issue を作成してください。

## コミット禁止情報

以下は理由を問わず Git にコミットしないでください。

- APIキー、アクセストークン、パスワード、TTS/LLMサービスの認証情報
- 個人情報
- 契約上非公開の資料、ライセンス上再配布できない教材
- 未確認の試験問題全文・規格本文、有償資料の複製

誤ってコミットした場合は、直ちに該当認証情報を無効化し、履歴からの除去を含む
インシデント対応を行います。

## 技術的対策

- pre-commit による秘密情報検出(private key / AWS credentials)
- CI での secret scanning(gitleaks)と依存脆弱性チェック(pip-audit)
- `.gitignore` による raw データ・認証情報ファイルの除外

## データ分類

Public / Internal / Confidential / Restricted の4分類を使用します。
詳細は [docs/operations/data-classification.md](docs/operations/data-classification.md)
と [docs/governance/information-security.md](docs/governance/information-security.md) を参照してください。
