# Semrush 連携ツール

## 概要
Semrush API を利用して、ドメイン分析やキーワード調査のデータを取得するツールです。

## 使い方
`.env` ファイルに `SEMRUSH_API_KEY` を設定した後、以下のコマンド等で利用します。

```bash
# ドメイン分析（日本データベース jp）
python3 00_Tools/semrush/semrush_cli.py domain example.com jp

# キーワード分析（日本データベース jp）
python3 00_Tools/semrush/semrush_cli.py keyword "Web制作" jp
```

AIエージェント（Cline）に「〇〇のドメインをSemrushで分析して」「〇〇キーワードのデータを集めて」と指示することで、自動でデータを取得し整理・可視化します。
