import { defineCollection, z } from 'astro:content';

// 1. 施工事例コレクション (works)
const worksCollection = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string(),                   // 例: 「光と風が通り抜ける中庭のある平屋」
    thumbnail: z.union([image(), z.string()]).optional(), // 画像オブジェクトまたは文字列パス
    gallery: z.array(z.union([image(), z.string()])).optional(),// 施工写真ギャラリー
    city: z.string().optional(),        // 施工エリア（例: 「〇〇市」）
    structure: z.string().optional(),   // 工法・構造（例: 「木造軸組工法」）
    family: z.string().optional(),      // 家族構成（例: 「夫婦＋子ども2人」）
    floorSpace: z.string().optional(),  // 延床面積（例: 「32.5坪」）
    priceRange: z.string().optional(),  // 価格帯（例: 「2,000万円〜2,500万円」）
    tags: z.array(z.string()).default([]), // タグ（例: ["平屋", "中庭", "高気密・高断熱"]）
    pubDate: z.coerce.date(),           // 掲載日
    featured: z.boolean().default(false),// トップページピックアップ
    category: z.string().optional(),
    client: z.string().optional(),
  }),
});

// 2. 見学会・イベント情報コレクション (events)
const eventsCollection = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string(),                   // 例: 「〇〇市 完成見学会」
    thumbnail: z.union([image(), z.string()]).optional(),
    status: z.enum(['開催前', '開催中', '予約受付け終了', '常設']).default('開催前'), // ステータス
    eventDate: z.string().optional(),    // 日時表記（例: 「2026年9月10日(土)〜11日(日)」）
    location: z.string().optional(),     // 開催場所
    reservationRequired: z.boolean().default(true), // 完全予約制
    pubDate: z.coerce.date(),
  }),
});

// 3. お知らせコレクション (news)
const newsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.string().default('お知らせ'),
    pubDate: z.coerce.date(),
    description: z.string().optional(),
  }),
});

export const collections = {
  'works': worksCollection,
  'events': eventsCollection,
  'news': newsCollection,
};


