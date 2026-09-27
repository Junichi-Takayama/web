# 【未着手】microCMS接続：お知らせ・制作施工事例のヘッドレスCMS連携と自動ビルド環境構築

## 1. 概要・背景
WordPressのような重く壊れやすいシステムから脱却し、**「直感的な専用管理画面」と「0秒台の超高速表示」を両立**させるため、国産ヘッドレスCMS「microCMS」とAstroサイトをAPI連携する。
なお、ブログはお知らせと構造が重複するため廃止し、**「お知らせ（news）」**とリッチな**「制作・施工事例（works）」**の2系統に特化して連携設計を行う。

## 2. 現在のステータス
- **ステータス**: `未着手 / 設計中` (To Do)
- **担当**: 高山 潤一 / AI (Cline)
- **対象**: `templates/astro_v2/` および microCMS API設定

## 3. 実装スコープ・要件
- [ ] **microCMS サービス環境の準備**:
  - サービス開設およびAPIキー発行
  - エンドポイント定義：
    1. `news` (お知らせ・新着情報: タイトル、日付、カテゴリ、本文)
    2. `works` (制作・施工事例: タイトル、所在地/種別、メイン画像、スライダー写真群、仕様テーブル、コンセプト、担当者コメント)
- [ ] **Astro側クライアント実装**:
  - `microcms-js-sdk` の導入
  - 環境変数（`.env`）での `MICROCMS_SERVICE_DOMAIN` / `MICROCMS_API_KEY` 管理
  - `src/lib/microcms.ts` による型安全なAPIクライアントの実装
- [ ] **コンテンツ取得・動的ルーティング統合**:
  - `src/pages/news/[slug].astro` での microCMS お知らせ記事取得・SSG生成
  - `src/pages/works/[slug].astro` での microCMS 事例詳細取得・SSG生成（スライダー画像群・スペック表対応）
  - リッチエディタ出力のサニタイズとTailwind Typography（`prose`）スタイリング
- [ ] **Webhook 自動ビルド連携**:
  - microCMS 記事公開・更新・削除時に Cloudflare Pages の Deploy Hook を叩くWebhook設定
  - 下書きプレビュー（Draft Key）表示機能の検証

## 4. 受け入れ基準 (Definition of Done)
- [ ] microCMS管理画面から入稿した記事が、Astroサイト上で正しくレンダリングされること
- [ ] 記事の投稿・更新後、Cloudflare Pages の自動ビルドが走り、数分以内に本番反映されること
- [ ] APIキーや機密情報が公開リポジトリに漏洩しないよう厳格に遮断されていること
