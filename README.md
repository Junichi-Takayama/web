# 次世代Web制作ソリューション・実務開発環境 (`web`)

本リポジトリは、**Astro × Claude Code × Figma** を中核とした、個人事業（地方工務店・中小企業向け ストック型Web制作・保守運用ビジネス）の実務開発環境およびドキュメント群を一元管理しています。

---

## 🧭 全体構造と本リポジトリの位置づけ

本リポジトリは、**「個人事業（高山様主体のストック型ビジネス）」**を一人で低工数・高利益率に完結・運用するために特化しています。

- **制作ワークフロー（コアエンジン）**:
  - Astroカタログ蓄積 × Claude Code × Figma双方向連携
  - WF先行型：カタログから最速で動くWebモック生成 ➔ Figmaでデザイン
  - デザイン先行型：Auto LayoutなしFigma ➔ Claudeが清書してWebモック化
- **個人事業モデル（小さく・速く・確実に稼ぐ）**:
  - 低工数のストック収益構築（月額保守）
  - 営業しない代理店/OEM構造（コンサル等をフロントに活用）
  - 一人で完結する自動化体制（GitHub PRワンクリック公開・入稿ポータル）
- **技術・インフラ構成**:
  - Cloudflare Pages（インフラ原価0円・高速エッジ）
  - さくらメール分離（既存メールを止めずに安全Web移行）
  - Formrun（無料枠活用）
  - GitHub PR自動マージ（Cloudflare Worker自動化）

---

## 📁 フォルダ構成と役割

```text
web/
├── .clinerules                           # AI（Cline）向けの運用ルール・行動規範・Astro規約
├── .gitignore                            # node_modules, *.secret.*, credentials.* 除外設定
├── README.md                             # 本書（全体定義・運用ガイド）
│
├── 00_Tools/                             # 【自動化ツール】office_parser, figma, semrush等
│
├── 01_Documents/                         # 【事業正本・全体ドキュメント】
│   ├── 新規Web制作サービス概要・運用仕様書.md    # 【正本】技術スタック・運用SLA・自動公開
│   ├── 新規Web制作・保守運用サービス構想.md      # 【構想】代理店/OEMビジネスモデル
│   ├── 初回ヒアリングシート.md                  # エンドクライアント向け初回ヒアリング
│   └── ログ.md                                  # 検討・合意事項の一元化ログ
│
├── clients/                              # 【クライアント別実案件領域】
│   └── 〇〇工務店/                       # 実案件ディレクトリ
│       ├── 01_Documents/                 # クライアント概要.md, タスク.md, ログ.md, 要件定義.md
│       │   └── credentials.secret.md     # ★ログイン・接続情報（Obsidian閲覧可・Git完全遮断）
│       ├── materials/                    # 支給素材（写真・原稿）
│       └── site/                         # Astroサイトソースコード本体
│
└── templates/                            # 【制作テンプレート・共通アセット一元化】
    ├── client_docs/                      # 新規案件用ドキュメントひな形（01_Documents一式）
    ├── astro_v1/                         # 汎用工務店Astroスターター（第1世代）
    ├── astro_v2/                         # ★本命：最新改良版スターター（第2世代・入稿ポータル/request搭載）
    ├── marp/                             # Marpスライド設定・テーマCSS
    └── rules/                            # Astro × AI 開発ガイドライン等
```

---

## 📝 運用・記録ルール

### 1. 案件管理の「3点強制連動」
進捗・連絡が発生した際は、必ず各案件の以下の3ファイルを同一ターンで一括更新します：
1. **`01_Documents/ログ.md`**: 事実・決定事項を箇条書きで追記
2. **`01_Documents/タスク.md`**: チェックボックス、完了移動、直近予定、参照元を更新
3. **`01_Documents/クライアント概要.md`**: 進行中のIssueステータスを最新化

### 2. 秘密情報・ログイン情報の安全管理
- サーバー、ドメイン、Cloudflare、CMS等のログイン情報は、各案件の `01_Documents/credentials.secret.md` に記載します。
- `.gitignore`（`*.secret.*`）により Git 管理から自動除外されるため、GitHub への誤流出が 100% 防がれます。Obsidian からは通常の Markdown ノートとして閲覧・編集が可能です。

---

## 🚀 Astroローカル動作確認方法

```bash
# astro_v1（第1世代スターター）
cd /Users/apple/Documents/projects/web/templates/astro_v1
npm run dev
# -> http://localhost:4321

# astro_v2（第2世代・改良版スターター / 入稿ポータル /request 搭載）
cd /Users/apple/Documents/projects/web/templates/astro_v2
npm run dev
# -> http://localhost:4321

# 実案件（例: 〇〇工務店）
cd /Users/apple/Documents/projects/web/clients/〇〇工務店/site
npm run dev
# -> http://localhost:4321
```
