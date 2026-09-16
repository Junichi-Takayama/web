# GA4 レポート用 Marp スライドコンポーネント カタログ＆利用ガイド

本ドキュメントは、GA4のアクセス解析CSVデータを基に、コンサルティング品質の美しいプレゼンテーションスライド（Marp）を自動・半自動で再現性高く生成するための「共通CSSスタイル」および「HTML/SVGコンポーネント集」です。

---

## 1. 参照CSVと適用コンポーネントの対応ルール（マッピング仕様）

| 対象CSVデータ | 推奨スライドタイトル | 使用するコンポーネント |
| :--- | :--- | :--- |
| **全体情報** | 表紙 / レポート基本情報 | `Title Cover` / `Info Card (2列)` |
| **月間主要指標 (MoM / YoY)** | 月間主要指標比較 | `Modern Data Table (増減バッジ付き)` |
| **指標規模感** | 主要指標の実績規模 | `Horizontal Bar Chart (棒グラフ)` |
| **当月サマリー** | 当月主要4指標ハイライトサマリー | `Big Number KPI Card (2×2 グリッド)` |
| **集客チャネル一覧** | 集客チャネル別アクセスデータ | `Modern Data Table` |
| **チャネル構成比** | 流入チャネル別セッション構成比 | `SVG Donut Chart + Legend Card (2カラム)` |
| **日次推移データ** | 日次アクセス指標の特徴データ | `Feature Stat Card (4列グリッド / ハイライト枠)` |
| **閲覧ページランキング** | 閲覧ページ TOP15 (前半/後半) | `Ranking Data Table` |
| **サマリー要約** | 事実データ集計要約 | `Summary Card (3列グリッド)` |

---

## 2. デザイン・トンマナ原則

- **ベースカラー**:
  - メインブルー: `#1e3a8a` / `#2563eb`
  - アクセント: `#06b6d4` (シアン), `#0d9488` (ティール), `#f59e0b` (アンバー)
  - 成功/増: `#15803d` / 背景 `#dcfce7`
  - 減少/減: `#b91c1c` / 背景 `#fee2e2`
  - 背景色: `#f8fafc` (スレート薄グレー)
  - テキスト: `#0f172a` (見出し用ダークスレート), `#334155` (本文), `#64748b` (補助)
- **余白・フォント**:
  - 16:9 比率（1280×720px）
  - フォント: `Hiragino Sans, Hiragino Kaku Gothic ProN, sans-serif`
  - パディング: 上下左右 36px〜45px、セクション上部に4pxのグラデーションバー


---

## 3. Marp スライド共通スタイル定義 (Frontmatter style)

```yaml
---
marp: true
theme: default
size: 16:9
paginate: true
header: "GA4アクセス解析レポート | {クライアント名}（{対象年月}）"
footer: "{ドメイン名}"
style: |
  section {
    background-color: #f8fafc;
    font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', -apple-system, BlinkMacSystemFont, sans-serif;
    padding: 36px 50px 45px;
    color: #1e293b;
    position: relative;
  }
  section::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%);
  }
  header { font-size: 11px; color: #64748b; letter-spacing: 0.05em; }
  footer { font-size: 11px; color: #94a3b8; }

  /* 見出し */
  .slide-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
  }
  .slide-title h2 {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
    border: none;
    padding: 0;
  }
  .slide-title .subtitle {
    font-size: 13px;
    color: #64748b;
    margin-left: auto;
  }

  /* モダンテーブル */
  .tbl-container {
    width: 100%;
    margin-top: 10px;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    overflow: hidden;
    border: 1px solid #e2e8f0;
  }
  table.modern-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    text-align: left;
  }
  table.modern-table th {
    background: #0f172a;
    color: #ffffff;
    padding: 10px 14px;
    font-weight: 600;
    font-size: 12px;
  }
  table.modern-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
  }
  table.modern-table tr:nth-child(even) td { background-color: #f8fafc; }
  .bold { font-weight: 700; color: #0f172a; }
  .text-right { text-align: right; }
  .text-center { text-align: center; }

  /* 増減ピルバッジ */
  .badge-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
  }
  .badge-up { background-color: #dcfce7; color: #15803d; }
  .badge-down { background-color: #fee2e2; color: #b91c1c; }

  /* KPIカード */
  .kpi-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 10px; }
  .kpi-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 20px 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    border-top: 4px solid #3b82f6;
  }
  .kpi-card.teal { border-top-color: #0d9488; }
  .kpi-card.purple { border-top-color: #7c3aed; }
  .kpi-card.amber { border-top-color: #d97706; }
  .kpi-val { font-size: 34px; font-weight: 800; color: #0f172a; line-height: 1.1; }
---
```
