# scripts/

開発・運用の補助スクリプト置き場です。

- CI用の検証スクリプトは `.github/scripts/` にあります
  (`check_pr_title.py` / `check_pr_body.py` / `validate_schemas.py`)
- ログ検証・集計は `uv run lcg ...` を使用します(`README.md` 参照)

今後の候補: 月次ログファイルの雛形生成、AI利用ログの自動追記ヘルパーなど。
