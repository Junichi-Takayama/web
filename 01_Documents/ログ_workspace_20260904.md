# 案件管理 workspace構造 構築・検討議事録

- **日時**: 2026/09/04
- **参加者**: 高山 潤一 様（Webディレクター）、Cline（AIエージェント）
- **目的**: AIエージェントを活用したマルチクライアント運用ディレクトリ構造の設計および自動化フローの定義

---

## 1. 施工事例 タスク定義（プロンプト）のレビュー結果
- **HITL（Human-In-The-Loop）の採用**: Step 3（素材・文章案の承認）と Step 5（デプロイ前プレビューの承認）の2段階承認フローで誤更新を防止。
- **Git操作の安全化**: 画像リネームやファイル変更が行われる前の Step 2（データ整形フェーズ）冒頭で作業用ブランチを作成・切り替える手順へ改訂。

---

## 2. マルチクライアント ディレクトリ構造の策定
共通資産管理とクライアント領域を明確に分離した構成を策定し、`workspace/` 配下に実体（サンプル）を構築。

```text
workspace/
├─ .clinerules                       # workspace構造専用運用ルール（プロシージャA〜D搭載）
├─ log.md                            # 本議事録ドキュメント
│
├─ _global/                          # [共通] ルール・テンプレート・コンポーネント
│   ├─ rules/                        # git_rules.md, operation_rules.md, security_rules.md
│   ├─ components/                   # 共通UIコンポーネント (ui/, sections/)
│   └─ templates/                    # client_about.md, task.md, log.md
│
└─ clients/                          # [個別] クライアント領域
    └─ 〇〇工務店/
        ├─ about.md                  # 基本情報・月次レポート契約フラグ・進行中Issue
        ├─ requirements.md           # システム全体要件定義（Astro Content Collections仕様）
        ├─ task.md                   # 予定・タスク管理
        ├─ log.md                    # コミュニケーション・更新ログ一元化
        ├─ content_rules/            # コンテンツ作成規約 (works.md, news.md, blog.md)
        ├─ materials/                # 支給素材データ (2026-09/)
        ├─ report/                   # GA4 CSVデータ & Marpスライド Markdown (old/ 内包)
        └─ website/                  # ★ Webサイトソースコード (開発/test/root を完全同期)
```

---

## 3. 主要運用プロシージャの確定（.clinerules へ反映）

1. **新規クライアント作成（プロシージャA）**:
   - 「xx工務店のフォルダつくって」の指示で、`_global/templates/` を基にドキュメントおよび標準サブフォルダ一式（`content_rules/`, `materials/`, `report/`, `website/`）を漏れなく一括生成。
2. **チャット・メールログ整理（プロシージャB）**:
   - 投げ込まれた連絡本文から対象クライアントを判定し、`log.md`（原文と要約）、`task.md`（新規タスクと参照元）、`about.md`（Issueステータス）の3点を同時連動更新。
3. **全体横断進捗回答（プロシージャC）**:
   - 「今月の更新対応は？」に対し、全クライアントの `task.md` / `about.md` を1回で一括読み込みし、各社の進捗状況（進行中・完了・依頼未受領）を箇条書きで即答。
4. **月次GA4レポート一括作成＆自動クリーンアップ（プロシージャD）**:
   - 「今月の月次レポートつくって」の指示で、`about.md` の `月次レポート契約: あり` を抽出。
   - `report/` 直下に当月度CSVが無い場合は「⚠️【エラー】〇〇工務店: CSV未配置」と明確にアラート報告。
   - レポート（Marp形式 `.md`）作成成功後、**使用したCSVファイルを即座に `report/old/` フォルダへ移動 (`mv`) させる自動後片付け**を実行。

---

## 4. 今後の拡張・自動化展望
- **GAS連携**: Google Analytics Data API を用いた毎月1日の全社GA4 CSV自動取得・Google Drive同期スクリプトの導入。
