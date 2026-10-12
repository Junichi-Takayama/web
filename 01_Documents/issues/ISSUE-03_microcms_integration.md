# 【進行中】microCMS接続：お知らせ・制作施工事例のヘッドレスCMS連携と自動ビルド環境構築

## 1. 概要・背景
WordPressのような重く壊れやすいシステムから脱却し、**「直感的な専用管理画面」と「0秒台の超高速表示」を両立**させるため、国産ヘッドレスCMS「microCMS」とAstroサイトをAPI連携する。
なお、ブログはお知らせと構造が重複するため廃止し、**「お知らせ（news）」**とリッチな**「制作・施工事例（works）」**の2系統に特化して連携設計を行う。

## 2. 現在のステータス
- **ステータス**: `進行中 / クライアント・API接続待ち` (In Progress)
- **担当**: 高山 潤一 / AI (Cline)
- **対象**: `templates/astro_v2/` および microCMS API設定

## 3. 実装スコープ・要件
- [x] **Astro側クライアント実装・フォールバック基盤**:
  - `microcms-js-sdk` の導入
  - 環境変数テンプレート（`.env.example`）の整備
  - `src/lib/microcms.ts` による型安全なAPIクライアント＆未接続時モックフォールバック設計（オフライン・キー未設定でも100%ビルド成功）
- [x] **コンテンツ取得・動的ルーティング統合**:
  - `src/pages/news/index.astro` および `[slug].astro` での microCMS お知らせ記事取得・SSG生成
  - `src/pages/works/index.astro` および `[slug].astro` での microCMS 事例詳細取得・SSG生成（スライダー画像群・スペック表・コンセプト・メッセージ対応）
  - トップページ（`src/pages/index.astro`）の最新お知らせ動的連携
  - リッチエディタ出力のサニタイズとTailwind Typography（`prose`）スタイリング
- [x] **スキーマ設定仕様書の作成**:
  - `01_Documents/microcms_schema_spec.md` にて `news` / `works` の全フィールド定義を明文化
- [x] **microCMS サービス環境の開設とAPIキー設定**:
  - サービス開設およびAPIキー発行
  - 管理画面での `news`（お知らせ）および `categories`（お知らせカテゴリ）エンドポイント作成完了
  - `.env` への設定および実データ通信疎通確認完了（worksは後続対応）
- [ ] **Webhook 自動ビルド連携**:
  - microCMS 記事公開・更新・削除時に Cloudflare Pages の Deploy Hook を叩くWebhook設定
  - 下書きプレビュー（Draft Key）表示機能の検証

## 4. 受け入れ基準 (Definition of Done)
- [x] microCMSのキーが未設定の状態でもモックデータによりビルド（`npm run build`）が100%成功すること
- [x] microCMS管理画面から入稿した記事（news）が、Astroサイト上で正しくレンダリングされること
- [ ] 記事の投稿・更新後、Cloudflare Pages の自動ビルドが走り、数分以内に本番反映されること
- [x] APIキーや機密情報が公開リポジトリに漏洩しないよう厳格に遮断されていること

