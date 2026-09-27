# Astro × AI（Cline）開発ガイドライン・ルール

Astro公式ドキュメント「Build with AI」に基づき、Cline（AIエージェント）がAstro + Node.js環境で開発・コーディングを行う際の標準運用規約です。

---

## 1. プロジェクト初期化ルール
* **ゼロベース作成の禁止**: 独自にファイル構造を一から組むのではなく、原則としてリポジトリ内の検証済みテンプレート（`templates/astro_v2` 等）を使用する。利用できない場合のみ、高山様へ確認したうえで公式スターターテンプレートを使用する。
* **TypeScriptの利用**: 原則として TypeScript（StrictまたはStrictest設定）を標準採用する。

---

## 2. インテグレーション・パッケージ追加ルール
* **公式インテグレーションの追加**: Tailwind CSS、React、Sitemapなどの公式機能を追加する場合は、`package.json` や `astro.config.mjs` を手動編集せず、必ず `npx astro add <integration>` コマンド（例: `npx astro add tailwind`）を実行する。
* **一般パッケージ**: その他のnpmパッケージは `npm install <package-name>` を使用し、`package.json` を直接手動編集しない。

---

## 3. 導入済みバージョンへの準拠
`package.json`、lockfile、Astro設定ファイルを正本とし、プロジェクトへ導入されているバージョンに対応する公式APIを使用する。「最新」という理由だけでAPI、構成、依存関係を変更せず、依頼されていないメジャーバージョンアップや依存関係の一括更新を行わない。

* **Content Collections (Content Layer)**:
  * 導入済みバージョンに対応する `astro:content` およびスキーマAPIを使用する。
* **動的処理・フォーム**:
  * 既存構成、ホスティング環境、セキュリティ要件を確認し、必要最小限の実装方式を選択する。Astro Actionsを使用する場合は導入済みバージョンに対応するAPIを使用し、不要なサーバーサイド機能や依存関係を追加しない。
* **画像最適化**:
  * ローカル画像は原則として `src/assets/` に配置し、`astro:assets` の `<Image />` または `<Picture />` コンポーネントを使用する。外部画像やCMS配信画像等で `<img>` が必要な場合は、alt、サイズ指定、遅延読み込み、レイアウトシフト対策を行う。
* **Scoped CSS & Tailwind**:
  * スタイルは `.astro` ファイル内の `<style>` タグ（Scoped CSS）または Tailwind CSS クラスを使用し、冗長なグローバルクラス名（BEMや独自の長いプレフィックス）を作成しない。

---

## 4. コーディング・コンポーネント規約
* **コンポーネント命名**: PascalCase（例: `HeaderNav.astro`, `Card.astro`）
* **Props定義**: 必ず TypeScript の `interface Props` を定義する。
* **Island Architecture（アイランド構造）**:
  * クライアントJavaScriptが必要な場合のみ `client:load` や `client:visible` ディレクティブを付与し、不必要なクライアントスクリプトの全域読み込みを避ける。

---


## 5. タイポグラフィ・レスポンシブ運用規約（PC/SPフォントサイズ標準）
地方工務店・中小企業向けWeb制作における、デバイス別（SP: iPhone SE 375px基準 〜 PC）フォントサイズおよびレイアウト標準設計ルールです。

### 5.1. レスポンシブ・タイポグラフィスケール
| 要素種別 | SP (モバイル: < 768px) | PC (デスクトップ: >= 768px) | ウェイト | 行送り (leading) | アラインメント原則 |
|---|---|---|---|---|---|
| **H1 (Hero大見出し)** | `text-2xl sm:text-3xl` (24px〜30px) | `md:text-5xl lg:text-6xl` (48px〜60px) | `font-medium` | `leading-snug` (1.3) | 原則中央（改行は意味単位の `inline-block`） |
| **H2 (セクション見出し)** | `text-xl sm:text-2xl` (20px〜24px) | `md:text-3xl` (30px) 〜 `md:text-4xl` (36px) | `font-medium` | `leading-snug` (1.375) | **`text-left md:text-center`**（SP左寄せ・PC中央） |
| **H3 (カード・ブロック見出し)** | `text-base` (16px) | `md:text-lg` (18px) 〜 `md:text-xl` (20px) | `font-medium` (明朝は500統一) | `leading-snug` | 原則左寄せ |
| **H4 / サブ見出し** | `text-sm` (14px) | `md:text-base` (16px) | `font-medium` | `leading-normal` | 左寄せ |
| **リード文・サブ説明** | `text-xs sm:text-sm` (12px〜14px) | `md:text-sm` (14px) | `font-light` | `leading-relaxed` | `text-left md:text-center` |
| **本文 (Body)** | `text-xs` (12px) 〜 `text-[13px]` | `md:text-sm` (14px) | `font-light` / `font-normal` | `leading-relaxed` (1.625) | 左寄せ |
| **アイブロウ / メタ情報** | `text-[10px]` 〜 `text-[11px]` | `md:text-xs` (12px) | `font-mono tracking-widest uppercase` | `leading-none` | `text-left md:text-center` |
| **ボタンラベル** | `text-xs` (12px) | `md:text-sm` (14px) | `font-medium tracking-wider` | `leading-none` | 中央 |

### 5.2. タイポグラフィ品質原則
1. **明朝体（`font-serif-title`）のウェイト制限**:
   - macOS・iOS環境のWebKit/CoreTextレンダリングにおいて、明朝体に `font-bold`（700）を適用すると線が太く潰れて野暮ったくなるため、明朝体見出しはすべて **`font-medium`（500）に統一**する。
2. **SP時セクションヘッダーの左寄せ原則**:
   - セクションヘッダー（アイブロウ・H2見出し・リード文）は、スマホ可変幅（320px〜390px）における1〜3文字の不自然な泣き別れ改行を防止し、自然な視線誘導を確保するため、**`text-left md:text-center`** を標準とする。
3. **見出しの折り返し保護（泣き別れ防止）**:
   - 長い見出し文字列は意味のまとまりごとに `<span class="inline-block">単語</span>` または `<br class="hidden sm:inline" />` を用い、助詞単体（「の、」「と」等）が次行へ脱落しないよう配慮する。
4. **汎用テンプレートでの実在クライアント名使用禁止**:
   - カタログや検証用テンプレート内に実在する特定クライアント名（加藤淳設計事務所等）を記載することは永久に厳禁とし、必ず架空のダミー企業名（例: 株式会社アーキスタジオ 様）を使用する。

