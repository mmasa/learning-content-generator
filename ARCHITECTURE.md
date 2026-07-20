# Architecture

## 設計方針

- **シンプル優先**: 初期段階では厳密な DDD / Clean Architecture を導入せず、
  「読んで理解できる」薄いレイヤ構成にとどめる
- **コンテンツ非依存のコア**: `src/` はコンテンツ(宅建・通関士など)に依存しない共通処理のみを持ち、
  コンテンツ固有の設定・スキーマ・プロンプトは `contents/<name>/` に置く
- **パイプライン指向**: 取り込み(import) → 正規化(normalize) → 生成(generate) →
  検証(validate) → 出力(export) の流れを基本とする
- **監査可能性**: 作業ログ・AI利用ログは構造化ファイル(YAML/JSONL)を単一の情報源とし、
  集計はすべてそこから導出する(同じ情報の手動重複入力を避ける)

## パッケージ構成

```text
src/learning_content_generator/
├── domain/          # Pydanticモデル(作業ログ・AI利用ログ・見積)と工数計算
├── application/     # 集計・レポート生成のユースケース
├── infrastructure/  # ログファイル(YAML/JSONL)の読み込み
├── importers/       # 原データ取り込みの基底インターフェース
├── normalizers/     # 正規化処理の基底インターフェース
├── generators/      # コンテンツ生成(クイズ・読み上げ原稿)の基底インターフェース
├── validators/      # ログ・データの検証
├── exporters/       # Markdown / JSON / CSV 出力
├── llm/             # LLMクライアント抽象(利用ログ記録を必須とする)
├── tts/             # TTSプロバイダ抽象
└── cli/             # Typer による `lcg` CLI
```

現時点で実装があるのは domain / application / infrastructure / validators /
exporters / cli です。importers / normalizers / generators / llm / tts は
インターフェース定義のみで、コンテンツ生成機能の実装は今後の Issue で行います。

## データフロー(コンテンツ)

```text
contents/<name>/raw/        原データ(著作権未確認データはGit管理外)
        │  importers
contents/<name>/normalized/ 正規化データ(スキーマ準拠のJSON/YAML)
        │  generators(LLM利用時はAI利用ログ必須)
contents/<name>/generated/  クイズ・解説・読み上げ原稿
        │  tts
contents/<name>/audio/      音声ファイル(Git管理外、メタデータのみ管理)
```

## データフロー(運用ログ)

```text
reports/ai-usage/*.yaml|jsonl  AI利用ログ(スキーマ: schemas/ai-usage-log.schema.json)
reports/effort/*.yaml          作業ログ(スキーマ: schemas/work-log.schema.json)
reports/effort/estimates.yaml  Issue別見積工数
        │
        └─ lcg report ... → Markdown / JSON / CSV(Issue別・担当者別・月別・カテゴリ別)
```

## 主要な設計判断

| 判断 | 理由 |
| --- | --- |
| ログはGit管理のYAML/JSONLファイル | 監査証跡がPRレビューを通る・外部DB不要・差分レビュー可能 |
| トークン数は `int` または `unknown/not-provided/estimated` | 取得不能な値を実測値と混同させない |
| 見積は `estimates.yaml` に集約 | Issue本文のスクレイピングに依存せず集計を安定させる |
| コンテンツ別ディレクトリ + 共通スキーマ | 新コンテンツ追加時にコア改修を不要にする |
| TTS/LLMはプロトコル(抽象)のみ先行定義 | プロバイダ選定を遅延させ、認証情報の混入を防ぐ |
