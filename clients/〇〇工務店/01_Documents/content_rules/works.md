# 施工事例（Works）作成ルール

## ファイル保存先
- `clients/〇〇工務店/website/src/content/works/{slug}.md`

## フロントマター (YAML仕様)
`src/content/config.ts` で定義されている以下のスキーマに完全準拠すること：

```yaml
---
title: "光と風が通り抜ける吹き抜けのある家"
city: "東京都世田谷区"
structure: "木造軸組工法"
family: "夫婦＋子ども2人"
floorSpace: "112㎡（約33坪）"
priceRange: "2,500万円〜3,000万円"
tags: ["吹き抜け", "無垢フローリング", "家事楽動線"]
pubDate: 2026-09-04
featured: true
thumbnail: "../../assets/works/YYYYMMDD-〇〇工務店-01.jpg"
gallery:
  - "../../assets/works/YYYYMMDD-〇〇工務店-01.jpg"
  - "../../assets/works/YYYYMMDD-〇〇工務店-02.jpg"
---
```

## 画像保存先・命名規則
- 保存先: `clients/〇〇工務店/website/src/assets/works/`
- 命名規則: `YYYYMMDD-〇〇工務店-{連番2桁}.jpg` または `.webp`
- リサイズ: 横幅最大1200px

## 本文記述規約
- 文字数: 350〜450文字程度
- トーン＆マナー: 親しみやすく温かみのある「です・ます」調。
