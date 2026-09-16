# Astro 標準ディレクトリ構造 (ダミー案件)

このプロジェクトは、AI（Cline）による高速ビルド・静的サイト生成（SSG）用に標準化されたAstroプロジェクト構造です。

## ディレクトリ構成
- `public/`: ファビコン、OGP、直貼り静的ファイル
- `src/assets/`: Astroで自動最適化・WebP変換される画像
- `src/components/`: 再利用可能なコンポーネント群（common/parts/section）
- `src/content/`: マークダウン原稿データ（news/works）
- `src/layouts/`: サイト共通レイアウト（Layout.astro）
- `src/pages/`: ファイルベースルーティング（URL直結）
