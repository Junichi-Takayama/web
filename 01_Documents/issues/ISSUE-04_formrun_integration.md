# 【進行中】フォーム接続：Webサイト無料診断・お問い合わせフォームのWeb3Forms連携と反響通知

## 1. 概要・背景
Webサイト無料診断やお問合せの反響を確実・安全に管理し、サーバー保守放置によるメール不達やスパムリスクを完全排除するため、サーバーレス・フォーム送信サービス「Web3Forms」を導入・連携する。
（※formrunの無料枠仕様改定・コード型有料化に伴い、広告完全非表示・完全無料・ArCraft自作デザイン100%維持が可能な「Web3Forms」へ方針決定・移行）

## 2. 現在のステータス
- **ステータス**: `実装完了 / 実機プレビュー検証中` (In Review)
- **担当**: 高山 潤一 / AI (Cline)
- **対象**: `templates/astro_v2/src/pages/contact/index.astro`, `thanks.astro`
- **作業ブランチ**: `feat/form-web3forms-integration`

## 3. 実装スコープ・要件
- [x] **サービス選定・Access Key発行**:
  - formrun無料枠仕様改定（コード型有料化）の確認とWeb3Formsへの切り替え決定
  - 高山様によるWeb3Forms Access Keyの発行（`66e948f7-371b-4ca3-8038-d0513f893b3a`）
- [x] **UI・非同期送信（Fetch API）実装**:
  - `templates/astro_v2/src/pages/contact/index.astro` のArCraftデザインを100%維持
  - 非同期POST送信（Fetch API）による画面遷移なしのスムーズな送信体験
  - 二重送信防止（送信中ボタン非活性化・スピナーアニメーション）
  - エラー時のインラインメッセージ表示とボタン復旧
- [x] **項目マッピング・通知最適化**:
  - ご相談項目（チェックボックス複数選択をカンマ区切りで集約）
  - 貴社名・お名前・電話番号・メールアドレス・現行WebサイトURL・現在のお困りごと
  - `name="email"` 指定によるメーラーワンクリック返信（Reply-To連動）の担保
  - メール件名（`subject`）および送信者名（`from_name`）の設定
- [x] **セキュリティ・スパム対策**:
  - Honeypotボットガード（`name="botcheck"` 非表示フィールド）の設置
  - 必須項目・メールアドレス形式・URL形式のHTML5ネイティブ検証
- [x] **サンクスページ導線**:
  - 送信成功時の独自サンクスページ（ `/contact/thanks/` ）への確実な自動遷移
  - JS無効環境時のフォールバックリダイレクト設定

## 4. 受け入れ基準 (Definition of Done)
- [x] 静的ビルド（`astro check && npm run build`）が 0 errors / 0 warnings で正常完了すること
- [ ] プレビュー環境でのテスト送信が成功し、高山様のメールアドレスへ通知が即時届くこと
- [ ] 送信完了後に独自サンクスページ（ `/contact/thanks/` ）へ正常遷移すること
