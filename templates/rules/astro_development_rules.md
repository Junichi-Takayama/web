# Astro × AI（Cline）開発ガイドライン・ルール

Astro公式ドキュメント「Build with AI」に基づき、Cline（AIエージェント）がAstro + Node.js環境で開発・コーディングを行う際の標準運用規約です。

---

## 1. プロジェクト初期化ルール
* **ゼロベース作成の禁止**: 独自にファイル構造を一から組むのではなく、必ず `npm create astro@latest -- --template <template-name>` または公式スターターテンプレートをベースに初期構築する。
* **TypeScriptの利用**: 原則として TypeScript（StrictまたはStrictest設定）を標準採用する。

---

## 2. インテグレーション・パッケージ追加ルール
* **公式インテグレーションの追加**: Tailwind CSS、React、Sitemapなどの公式機能を追加する場合は、`package.json` や `astro.config.mjs` を手動編集せず、必ず `npx astro add <integration>` コマンド（例: `npx astro add tailwind`）を実行する。
* **一般パッケージ**: その他のnpmパッケージは `npm install <package-name>` を使用し、`package.json` を直接手動編集しない。

---

## 3. 現行・最新APIの遵守（旧API使用の禁止）
AIが過去の古い知識を出力するのを防ぐため、以下の最新Astro仕様を厳格に適用する。

* **Content Collections (Content Layer)**:
  * 旧仕様（Astro v2/v3初期）の書き方に囚われず、最新の `astro:content` モジュールおよび `defineCollection` / `zod` スキーマを使用する。
* **Actions (Astro Actions)**:
  * フォーム処理やバックエンド処理には、最新の Astro Actions API（`astro:actions`）を活用する。
* **画像最適化**:
  * 画像は `src/assets/` に配置し、必ず `astro:assets` の `<Image />` または `<Picture />` コンポーネントを使用する。（`public/` への置くだけ運用や `<img>` 直書きは避ける）
* **Scoped CSS & Tailwind**:
  * スタイルは `.astro` ファイル内の `<style>` タグ（Scoped CSS）または Tailwind CSS クラスを使用し、冗長なグローバルクラス名（BEMや独自の長いプレフィックス）を作成しない。

---

## 4. コーディング・コンポーネント規約
* **コンポーネント命名**: PascalCase（例: `HeaderNav.astro`, `Card.astro`）
* **Props定義**: 必ず TypeScript の `interface Props` を定義する。
* **Island Architecture（アイランド構造）**:
  * クライアントJavaScriptが必要な場合のみ `client:load` や `client:visible` ディレクティブを付与し、不必要なクライアントスクリプトの全域読み込みを避ける。
