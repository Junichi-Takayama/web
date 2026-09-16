# 住宅・工務店向け Astro 自社スターターテンプレート仕様書

住宅業界・工務店に特化した、高速・高SEO・丸投げ保守（月2回更新）に最適な自社Astroテンプレートの設計仕様です。

---

## 1. サイト基本構造（ディレクトリ構成）

```text
astro-koumuten-starter/
├── src/
│   ├── assets/                 # 共通画像（ロゴ、ダミー施工写真など）
│   ├── components/             # 再利用可能コンポーネント
│   │   ├── common/             # ヘッダー、フッター、ナビゲーション、パンくず
│   │   ├── works/              # 施工事例カード、事例ギャラリー、スペック表
│   │   ├── events/             # 見学会・イベントカード、ステータスバッジ
│   │   ├── form/               # Formrun埋め込み、来場予約コンポーネント
│   │   └── ui/                 # ボタン、セクションタイトル、FVスライダー
│   ├── content/                # Content Collections（データ・記事管理）
│   │   ├── config.ts           # スキーマ定義（Zod）
│   │   ├── works/              # 施工事例（Markdown/MDX）
│   │   ├── events/             # 見学会・イベント情報（Markdown/MDX）
│   │   └── news/               # お知らせ（Markdown/MDX）
│   ├── layouts/
│   │   └── Layout.astro        # 共通レイアウト（SEO/OGP/共通Head含む）
│   └── pages/
│       ├── index.astro         # トップページ
│       ├── concept.astro       # 家づくりのこだわり・性能
│       ├── works/
│       │   ├── index.astro     # 施工事例一覧（タグ・条件絞り込み対応）
│       │   └── [slug].astro    # 施工事例詳細
│       ├── events/
│       │   ├── index.astro     # イベント・見学会一覧
│       │   └── [slug].astro    # イベント詳細
│       ├── news/
│       │   ├── index.astro     # お知らせ一覧
│       │   └── [slug].astro    # お知らせ詳細
│       ├── company.astro       # 会社概要・アクセスマップ
│       ├── contact.astro       # 資料請求・お問い合わせ（Formrun）
│       └── reservation.astro   # 来場予約・見学会予約（Formrun）
```

---

## 2. Content Collections（コンテンツ構造・Zodスキーマ）

`src/content/config.ts` で管理する工務店特化のスキーマ定義です。

### ① 施工事例 (`works`)
```typescript
import { defineCollection, z } from 'astro:content';

const worksCollection = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string(),                   # 事例タイトル（例: 「光と風が通り抜ける中庭のある平屋」）
    thumbnail: image(),                 # メインアイキャッチ画像
    gallery: z.array(image()).optional(),# 施工写真ギャラリー（複数枚）
    city: z.string(),                   # 施工エリア（例: 「〇〇市」）
    structure: z.string(),              # 工法・構造（例: 「木造軸組工法」「2x4」）
    family: z.string().optional(),       # 家族構成（例: 「夫婦＋子ども2人」）
    floorSpace: z.string().optional(),   # 延床面積（例: 「32.5坪」）
    priceRange: z.string().optional(),   # 価格帯（例: 「2,000万円〜2,500万円」）
    tags: z.array(z.string()),          # タグ（例: ["平屋", "中庭", "高気密・高断熱", "自然素材"]）
    pubDate: z.date(),                  # 掲載日
    featured: z.boolean().default(false),# トップページ用ピックアップフラグ
  }),
});
```

### ② 見学会・イベント情報 (`events`)
```typescript
const eventsCollection = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string(),                   # イベント名（例: 「〇〇市 完成見学会」）
    thumbnail: image(),                 # イベント画像
    status: z.enum(['開催前', '開催中', '予約受付け終了', '常設']), # 開催ステータス
    eventDate: z.string(),               # 開催日時（例: 「2026年9月10日(土)〜11日(日) 10:00〜17:00」）
    location: z.string(),               # 開催場所（例: 「〇〇市〇〇町1-2-3」）
    reservationRequired: z.boolean().default(true), # 完全予約制フラグ
    pubDate: z.date(),
  }),
});
```

---

## 3. 工務店サイトで必須のモジュール＆機能

1. **施工事例ギャラリー & スペック表**
   * 写真をスワイプ/拡大表示できるモーダルギャラリー。
   * 延床面積・工法・価格帯・断熱性能などをスマートにまとめたテーブル表示。

2. **見学会・予約動線（CTAs）**
   * 画面下部に追従する「資料請求」「来場予約」のフローティングバナー（スマホCV率向上）。
   * Formrunの埋め込みコンポーネント（`contact` / `reservation` ページ）。

3. **家づくりのこだわり・断熱性能（コンセプトロジック）**
   * C値・Q値・UA値・耐震等級3などの専門数値を分かりやすくアイコンカード化する共通コンポーネント。

4. **月2回更新（お知らせ/イベント/事例追記）の超簡単運用**
   * Markdownファイルを `src/content/works/2026-house-a.md` などの形式で1ファイル追加するだけで、AI（Cline）が自動ビルド＆デプロイ完了。

---

## 4. この自社テンプレを使うメリット（営業＆制作）

* **制作スピード**: 従来のゼロ構築から**最速半日〜1日**で初期デザイン・組み上げが完了。
* **画像の高画質＆超高速化**: 住宅写真はデータ量が大きいですが、Astroの `<Image />` 処理により、画質を保ったまま自動でWebP変換・次世代フォーマット配信。PageSpeed Insightsで90点以上を連発可能。
* **運用丸投げ（月1万円）との親和性**: 「写真3枚と坪数・文章をLINEで送ってもらう」→ AIがMarkdownを作成しGit Push → 秒速で本番反映。
