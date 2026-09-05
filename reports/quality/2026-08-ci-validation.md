# GitHub Actions / ブランチ保護の実地検証(Issue #6)

`.github/workflows/ci.yml` / `pr-checks.yml` の全ジョブと、main のブランチ保護設定を
実際のPRで検証した。

## 1. 正常系: 全ジョブが動作する

PR #15〜#21(Issue #1〜#5)で毎回 `gh pr checks` を実行し、以下10ジョブすべてが
`pass` することを繰り返し確認済み。

- Ruff / Mypy / YAML lint
- Pytest
- JSON Schema validation
- AI usage / work log validation
- Markdown lint
- Secret scanning (gitleaks)
- Dependency vulnerability check
- License check
- PR title (Conventional Commits)
- PR body (issue ref / reviewer / hours / AI usage / tests / security / copyright)

## 2. 異常系: 不備のあるPRが正しくfailする

本Issue専用に、意図的に壊れた内容のPRを作成して検証した(PR #22、検証後クローズ・
ブランチ削除、mainへのマージなし)。

### 仕込んだ不備

| 不備 | 対象ジョブ |
| --- | --- |
| `tests/_ci_negative_check.py` に未使用import(`import os`) | Ruff / Mypy / YAML lint |
| 同ファイルに `assert False` の失敗テスト | Pytest |
| `contents/takken/normalized/_ci_negative_check.yaml` に必須フィールド欠落の不正データ | JSON Schema validation |
| PRタイトルを Conventional Commits 形式にしない(`testing ci negative path`) | PR title |
| PR本文を必須セクション欠落のまま提出 | PR body |

### 結果(`gh pr checks 22`)

```text
JSON Schema validation                                                        fail
PR body (issue ref / reviewer / hours / AI usage / tests / security / copyright)  fail
PR title (Conventional Commits)                                               fail
Pytest                                                                        fail
Ruff / Mypy / YAML lint                                                       fail
AI usage / work log validation                                                pass
Dependency vulnerability check                                                pass
License check                                                                 pass
Markdown lint                                                                 pass
Secret scanning (gitleaks)                                                    pass
```

仕込んだ5件の不備に対応するジョブがすべて `fail`、無関係な5ジョブは `pass` のまま
であることを確認した(誤検知・見逃しなし)。

### マージ拒否の確認

チェックが `fail` の状態で `gh pr merge 22 --squash` を実行すると、
ブランチ保護により拒否されることを確認した:

```text
X Pull request mmasa/learning-content-generator#22 is not mergeable:
  the base branch policy prohibits the merge.
```

## 3. ブランチ保護設定の確認

`gh api repos/mmasa/learning-content-generator/branches/main/protection` で確認。

| 設定 | 値 | 意味 |
| --- | --- | --- |
| `required_status_checks.contexts` | 上記10ジョブ全件 | 全ジョブ成功がマージ条件 |
| `required_pull_request_reviews` | 設定あり(`required_approving_review_count: 0`) | PR経由必須(直push不可)。承認数0は[review-and-approval](../../docs/governance/review-and-approval.md)の個人開発時暫定運用(自己レビュー)に整合させた意図的な設定 |
| `enforce_admins` | `true` | 管理者もルールをバイパスしない |
| `required_conversation_resolution` | `true` | レビュースレッド未解決だとマージ不可 |
| `allow_force_pushes` | `false` | main への force push 不可 |
| `allow_deletions` | `false` | main の削除不可 |

「直push禁止」は `required_pull_request_reviews` が設定されている時点でGitHub側の
仕様上ブロックされる(PR経由以外のpushを受け付けない)ため、実際に direct push を
試すリスクは取らず設定確認のみで判断した。

## 結論

- Acceptance Criteria 3件すべて満たしていることを実地検証で確認した
  - [x] PRで全ジョブが動作する
  - [x] 不備のあるPRが正しくfailする
  - [x] ブランチ保護が有効
- ブランチ保護設定の変更は不要と判断(現状の `required_approving_review_count: 0` は
  自己レビュー運用と整合しており、意図的な設定として妥当)
