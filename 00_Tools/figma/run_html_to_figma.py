#!/usr/bin/env python3
"""
HTML/CSS → Figma 一括自動描画ランナー
使用方法:
  python3 run_html_to_figma.py [HTMLファイルのパス] [アートボード名]
"""

import sys
import os
from html_to_figma_engine import HTMLToFigmaEngine

def main():
    html_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/junichi.takayama/Desktop/案件管理/00_Tools/figma/sample_top_page.html"
    artboard_name = sys.argv[2] if len(sys.argv) > 2 else "PC_Top_Wireframe_1440px"

    if not os.path.exists(html_path):
        print(f"エラー: HTMLファイルが見つかりません: {html_path}")
        sys.exit(1)

    print(f"==================================================")
    print(f"  HTML/CSS → Figma 自動描画エンジン 実行中")
    print(f"  入力HTML: {html_path}")
    print(f"  アートボード: {artboard_name} (1440px)")
    print(f"==================================================")

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    engine = HTMLToFigmaEngine()
    commands = engine.convert_html_to_commands(html_content, artboard_name=artboard_name, artboard_width=1440)
    print(f"[Engine] 生成された描画コマンド数: {len(commands)} 件")

    success = engine.send_to_figma()
    if success:
        print("[完了] Figma Bridge Server に正常送信されました。Figmaキャンバスをご確認ください。")
    else:
        print("[注意] 送信に失敗しました。`figma_bridge_server.py` が起動しているか確認してください。")

if __name__ == "__main__":
    main()
