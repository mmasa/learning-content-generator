# audio/ — 生成音声置き場(Git管理外)

このディレクトリの内容は README を除き `.gitignore` で **Git 管理外** です。

- 音声ファイル(mp3/wav 等)は大容量のためコミットしません
- 生成した音声は `../metadata/` に `audio-metadata.schema.json` 準拠のメタデータのみを記録します
- TTSサービスの認証情報は環境変数で扱い、絶対にコミットしないでください
