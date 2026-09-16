# Figma 連携・自動描画ツール (Cline Figma Bridge)

PDF資料「先端技術部_Claude_Cowork_活用.pdf」で定義された、**AIからの自動指示でFigmaキャンバス上に直接ワイヤーフレーム（Frame / Text / Rectangle）を描画するツール**です。

---

## 🚀 使い方（簡単3ステップ）

### ステップ 1: Bridge サーバーの起動
ターミナルで以下のコマンドを実行し、Bridge サーバーを起動します。
```bash
python3 00_Tools/figma/figma_bridge_server.py
```
*( `http://localhost:3030` で待機が開始されます )*

---

### ステップ 2: Figma デスクトップアプリでプラグインをインポート
1. **Figma デスクトップアプリ**を開きます（アプリ版推奨）。
2. メニューバーから `Plugins` ＞ `Development` ＞ `Import plugin from manifest...` を選択します。
3. 以下のファイルを選択します：
   `/Users/junichi.takayama/Desktop/案件管理/00_Tools/figma/plugin/manifest.json`
4. インポート後、Figmaアプリで `Plugins` ＞ `Development` ＞ `Cline Figma Bridge Plugin` を選択して **Run（実行）** します。
5. プラグイン画面で緑色の文字 **「接続中 (Cline Bridge Active)」** と表示されれば完了です！

---

### ステップ 3: ワイヤーフレーム一括自動描画の実行
別のターミナルタブで以下を実行すると、開いている Figma キャンバス上に **PC表示トップWF雛形（1440px幅）が一括自動描画** されます。

```bash
python3 00_Tools/figma/figma_draw.py
```

---

## ✨ Cline（AI）での活用
チャットで**「〇〇という案件のSP版ワイヤーフレームを作って」「トップページのサービス紹介セクションをFigmaに追加して」**と指示いただければ、私（AI）が自動で要素（Frame/Text/Box）を生成し、Figmaキャンバス上に直接描画いたします。

