# レポート出力の実運用検証(Issue #5)

`lcg report` の各サブコマンド(ai-usage / effort / issue / monthly / contributor)を
markdown / json / csv の全出力形式で実データ(`reports/effort/`, `reports/ai-usage/`)に対して
実行し、内容を検証した。

## 検証結果サマリ

| レポート | markdown | json | csv | 判定 |
| --- | --- | --- | --- | --- |
| `report ai-usage` | OK | OK | OK | 合格 |
| `report effort` | OK | OK | OK | 合格 |
| `report issue --issue N` | OK(該当なしIssueも `(no data)` で安全) | OK | OK | 合格 |
| `report monthly --month YYYY-MM` | **既知の問題あり(#19)** | 同左 | 同左 | 条件付き合格 |
| `report contributor --name NAME` | OK(該当なし名前も安全) | OK | OK | 合格 |

## 差異率・承認率の定義の妥当性確認

- **Variance Rate** = `(Actual - Estimated) / Estimated * 100`
  (`domain/effort.py: variance_rate`)。見積が0以下の場合は `None` を返し
  ゼロ除算を回避している。`docs/operations/work-logging.md` の定義と一致。妥当と判断。
- **Approval Rate** = `approved / (approved + rejected + revised) * 100`
  (`application/reporting.py: _review_status_table`)。`pending` は分母から除外される
  (未レビューを承認率に混ぜない設計)で、挙動としては妥当と判断する。
  ただし `docs/governance/review-and-approval.md` はレビュー手順を定めるのみで
  承認率の算出式そのものは明文化していない。本検証時点ではこの式は実装から読み取れる
  仕様であって文書化された仕様ではないため、「文書と一致」ではなく「実装は妥当だが、
  式の文書化が未了」という扱いとする(文書化自体は本Issueのスコープ外)。

## 見つかった問題(改善Issueを起票)

検証中に2件の実装上の問題を発見し、Issueを起票した(このPRでは修正しない、方針は
[change-management](../../docs/governance/change-management.md) に従い別Issue・別PRで対応)。

1. **[#19](https://github.com/mmasa/learning-content-generator/issues/19)**
   月次レポート(`report monthly`)の「Effort by Issue」が、対象月に無関係なIssueについても
   プロジェクト全体の見積とその月だけの実績(0)を比較してしまい、
   ほぼ全件が Variance Rate -100% という誤解を招く表示になる。
   下の実行例(2026-08分)でも #1・#5〜#14・#19・#20 が該当。
2. **[#20](https://github.com/mmasa/learning-content-generator/issues/20)**
   Markdownテーブル出力がセル内の `|` をエスケープしていないため、
   自由記述欄(summary / purpose / notes)に `|` が含まれると列がずれる可能性がある。

## 実行例: `lcg report monthly --month 2026-08`

```text
uv run lcg report monthly --month 2026-08
```

```markdown
## Effort by Issue

| Issue | Title | Estimated PH | Actual PH | Variance Hours | Variance Rate (%) |
| --- | --- | --- | --- | --- | --- |
| #1 | Repository bootstrap | 6.00 | 0.00 | -6.00 | -100.00 |
| #2 | Governance documents review | 3.00 | 1.00 | -2.00 | -66.70 |
| #3 | AI usage logging operation | 1.50 | 0.50 | -1.00 | -66.70 |
| #4 | Human work logging operation | 1.00 | 0.50 | -0.50 | -50.00 |
| #5 | Effort reporting validation | 2.00 | 2.00 | 0.00 | 0.00 |
| #6 | GitHub Actions validation | 2.50 | 0.00 | -2.50 | -100.00 |
| #7 | Takken data schema | 3.00 | 0.00 | -3.00 | -100.00 |
| #8 | Takken sample content | 4.00 | 0.00 | -4.00 | -100.00 |
| #9 | Takken text normalization | 6.00 | 0.00 | -6.00 | -100.00 |
| #10 | Takken reading-script generation | 8.00 | 0.00 | -8.00 | -100.00 |
| #11 | TTS provider abstraction | 8.00 | 0.00 | -8.00 | -100.00 |
| #12 | Copyright and source management | 4.00 | 0.00 | -4.00 | -100.00 |
| #13 | Security review | 3.00 | 0.00 | -3.00 | -100.00 |
| #14 | Initial release preparation | 2.00 | 0.00 | -2.00 | -100.00 |
| #19 | Monthly report shows all-project estimates against month-filtered actuals | 1.50 | 0.00 | -1.50 | -100.00 |
| #20 | Markdown report cells don't escape literal pipe characters | 0.50 | 0.00 | -0.50 | -100.00 |

## Effort by Contributor

| Contributor | Person-Hours | AI-Assisted PH | Non-AI PH |
| --- | --- | --- | --- |
| Masato Miyaichi | 4.00 | 4.00 | 0.00 |

## Effort by Work Type (2026-08)

| Work Type | Entries | Person-Hours |
| --- | --- | --- |
| Data Creation | 1 | 0.50 |
| Review | 1 | 1.00 |
| Testing | 2 | 2.50 |

## AI Usage by Issue (2026-08)

| Issue | Runs | Input Tokens | Cached Input | Output Tokens | Total Tokens | Cost | Entries w/o Numeric Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #2 | 1 | 0 | 0 | 0 | 0 | - | 1 |
| #3 | 1 | 0 | 0 | 0 | 0 | - | 1 |
| #4 | 1 | 0 | 0 | 0 | 0 | - | 1 |
| #5 | 1 | 0 | 0 | 0 | 0 | - | 1 |

## AI Usage by Model (2026-08)

| Model | Runs | Input Tokens | Cached Input | Output Tokens | Total Tokens | Cost | Entries w/o Numeric Tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| claude-sonnet-5 | 4 | 0 | 0 | 0 | 0 | - | 4 |
```

(このコマンドはこのPRの最終コミットを対象に再実行して再現性を確認したもの。
Issue #5 の実績エントリ自体を含む月なので #5 行は Estimated/Actual が一致し Variance 0 になる。)

見ての通り #1(7月に6.0h実施・見積と完全一致)が8月レポートでは
Estimated 6.00 / Actual 0.00 / Variance -100.00% と表示されており、これが #19 の指す問題である。

## 結論

- `report ai-usage` / `report effort` / `report issue` / `report contributor` は
  markdown/json/csv すべてで実データに対し正しい値を出力することを確認した
- `report monthly` の Effort by Issue のみ、見積と実績の集計範囲不一致という設計上の問題があり、
  Issue #19 として起票し次のIssueで修正する
- 表示の頑健性として Issue #20(`|` エスケープ)を追加で起票した
- 差異率の定義は `docs/operations/work-logging.md` の仕様と一致しており妥当。
  承認率の定義は実装として妥当だが、算出式は現時点でどの文書にも明文化されていない
  (`docs/governance/review-and-approval.md` はレビュー手順のみを定める)
