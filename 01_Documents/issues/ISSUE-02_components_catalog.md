# 【進行中】カタログ・コンポーネント化：汎用共通25種コンポーネント群の開発とスタイルガイド統合

## 1. 概要・背景
工務店・建築系に偏っていた既存UIコンポーネントを再整理し、製造業・士業・サービス業など**地方中小企業全般のWebサイト制作・リニューアルへ即時転用可能な「汎用共通25種コンポーネント群」**として再設計・カタログ化を行う。

## 2. 現在のステータス
- **ステータス**: `実装完了・検証済` (Completed / In Review)
- **担当**: 高山 潤一 / AI (Cline)
- **対象ディレクトリ**: `templates/astro_v2/src/components/catalog/` & `templates/astro_v2/src/pages/components.astro`

## 3. 実装スコープ・25種コンポーネント内訳
1. **ナビゲーション・ヘッダー系 (3種)**:
   - [x] `HeaderNav`: レスポンシブ対応グローバルナビ
   - [x] `MegaMenu`: 複数階層サービス案内メニュー
   - [x] `FooterDefault`: サイトマップ＆企業情報フッター
2. **ヒーロー・ファーストビュー系 (3種)**:
   - [x] `HeroCentered`: 中央揃え・キャッチコピー重視型
   - [x] `HeroSplit`: 左右分割型（画像×テキスト）
   - [x] `HeroMinimal`: テキスト主導・洗練型
3. **課題・特徴・強み系 (4種)**:
   - [x] `ProblemCards`: 顧客の「悩み・課題」提示カード
   - [x] `FeatureGrid`: 3〜4カラムの強み・特徴グリッド
   - [x] `AlternatingRows`: 画像とテキストが交互に並ぶ詳細解説セクション
   - [x] `KeyBenefits`: 3大メリット強調ブロック
4. **料金・比較表系 (3種)**:
   - [x] `PricingCards`: プラン比較・推奨バッジ付き料金表
   - [x] `ComparisonTable`: 従来手法 vs 自社サービスの対比表
   - [x] `FeatureChecklist`: プラン別機能一覧表
5. **実績・事例・ギャラリー系 (3種)**:
   - [x] `CaseStudies`: 導入事例・実績一覧カード（サムネイル・タグ付き）
   - [x] `BentoGrid`: モダンなBento Gridレイアウト
   - [x] `ImageGallery`: 施工・製品写真ギャラリー
6. **信頼・会社・メッセージ系 (3種)**:
   - [x] `ProfileMessage`: 代表者メッセージ・顔写真・経歴カード
   - [x] `TimelineHistory`: 沿革・歴史タイムライン
   - [x] `StatCounters`: 実績数値・統計ハイライト
7. **FAQ・コンテンツ系 (3種)**:
   - [x] `AccordionFAQ`: よくある質問アコーディオン
   - [x] `TabbedContent`: タブ切り替えコンテンツ表示
   - [x] `ProcessSteps`: 問い合わせから納品までのステップフロー
8. **CTA・フォーム系 (3種)**:
   - [x] `LeadCTA`: ページ末尾の資料請求・無料相談誘導バナー
   - [x] `ContactForm`: 標準問い合わせ入力フォームUI
   - [x] `FloatingCTA`: モバイル追従型アクションボタン

## 4. 受け入れ基準 (Definition of Done)
- [x] 各コンポーネントが TypeScript の `interface Props` を備え、引数経由でテキストや画像をカスタマイズ可能であること
- [x] `src/pages/components.astro` 上に全25種が実動カタログとしてプレビュー一覧化されていること
- [x] Tailwind CSS ユーティリティのみで完結し、外部依存ライブラリを最小限に抑えていること
