#!/usr/bin/env python3
import urllib.request
import json

BRIDGE_URL = "http://localhost:3030/push"

def create_top_wf_commands():
    cmds = []
    # Parent Frame (1440x1860)
    cmds.append({"action": "create_frame", "key": "parent", "name": "PC_Top_Wireframe_1440px", "x": 0, "y": 0, "width": 1440, "height": 1860, "bg": {"r": 0.96, "g": 0.96, "b": 0.97}, "clipsContent": False})
    
    # 01_Header
    cmds.append({"action": "create_frame", "name": "01_Header", "x": 0, "y": 0, "width": 1440, "height": 80, "bg": {"r": 1.0, "g": 1.0, "b": 1.0}})
    cmds.append({"action": "create_text", "name": "Logo", "x": 120, "y": 28, "text": "COMPANY LOGO", "fontSize": 20, "fontStyle": "Bold", "color": {"r": 0.1, "g": 0.1, "b": 0.1}})
    cmds.append({"action": "create_text", "name": "Nav", "x": 600, "y": 30, "text": "サービス概要   ｜   特長・強み   ｜   導入事例   ｜   FAQ", "fontSize": 14, "color": {"r": 0.3, "g": 0.3, "b": 0.3}})
    cmds.append({"action": "create_rect", "name": "CTA_H", "x": 1180, "y": 18, "width": 140, "height": 44, "cornerRadius": 6, "color": {"r": 0.0, "g": 0.47, "b": 0.85}})
    cmds.append({"action": "create_text", "name": "CTA_HT", "x": 1210, "y": 32, "text": "お問い合わせ", "fontSize": 14, "fontStyle": "Bold", "color": {"r": 1.0, "g": 1.0, "b": 1.0}})
    
    # 02_FirstView
    cmds.append({"action": "create_frame", "name": "02_FirstView", "x": 0, "y": 80, "width": 1440, "height": 560, "bg": {"r": 0.93, "g": 0.95, "b": 0.98}})
    cmds.append({"action": "create_text", "name": "Catch", "x": 120, "y": 180, "width": 600, "text": "ビジネスの課題をテクノロジーで解決する\n次世代型ソリューションプラットフォーム", "fontSize": 32, "fontStyle": "Bold", "color": {"r": 0.1, "g": 0.1, "b": 0.1}})
    cmds.append({"action": "create_text", "name": "Sub", "x": 120, "y": 280, "width": 560, "text": "簡単な導入で業務効率を最大化。豊富な実績と手厚いサポートでDXを強力推進。", "fontSize": 16, "color": {"r": 0.4, "g": 0.4, "b": 0.4}})
    cmds.append({"action": "create_rect", "name": "FV_Btn", "x": 120, "y": 360, "width": 240, "height": 56, "cornerRadius": 8, "color": {"r": 0.0, "g": 0.47, "b": 0.85}})
    cmds.append({"action": "create_text", "name": "FV_BT", "x": 165, "y": 378, "text": "無料資料ダウンロード", "fontSize": 16, "fontStyle": "Bold", "color": {"r": 1.0, "g": 1.0, "b": 1.0}})
    cmds.append({"action": "create_rect", "name": "FV_Img", "x": 760, "y": 140, "width": 560, "height": 360, "cornerRadius": 12, "color": {"r": 0.82, "g": 0.85, "b": 0.9}})
    cmds.append({"action": "create_text", "name": "FV_IL", "x": 920, "y": 310, "text": "【メインビジュアル / UIイメージ】", "fontSize": 14, "color": {"r": 0.5, "g": 0.5, "b": 0.5}})
    
    # 03_News
    cmds.append({"action": "create_frame", "name": "03_News", "x": 0, "y": 640, "width": 1440, "height": 160, "bg": {"r": 1.0, "g": 1.0, "b": 1.0}})
    cmds.append({"action": "create_text", "name": "News_T", "x": 120, "y": 40, "text": "NEWS", "fontSize": 24, "fontStyle": "Bold", "color": {"r": 0.1, "g": 0.1, "b": 0.1}})
    cmds.append({"action": "create_text", "name": "News_1", "x": 280, "y": 44, "width": 800, "text": "2026.08.20   【お知らせ】 新機能アップデートのご案内", "fontSize": 15, "color": {"r": 0.2, "g": 0.2, "b": 0.2}})
    
    # 04_Services
    cmds.append({"action": "create_frame", "name": "04_Services", "x": 0, "y": 800, "width": 1440, "height": 540, "bg": {"r": 0.97, "g": 0.97, "b": 0.98}})
    cmds.append({"action": "create_text", "name": "Svc_T", "x": 120, "y": 50, "text": "SERVICES", "fontSize": 28, "fontStyle": "Bold", "color": {"r": 0.1, "g": 0.1, "b": 0.1}})
    for i in range(3):
        x = 120 + i * 420
        cmds.append({"action": "create_rect", "name": f"Bg_{i+1}", "x": x, "y": 120, "width": 360, "height": 340, "cornerRadius": 12, "color": {"r": 1.0, "g": 1.0, "b": 1.0}})
        cmds.append({"action": "create_rect", "name": f"Img_{i+1}", "x": x + 20, "y": 140, "width": 320, "height": 150, "cornerRadius": 8, "color": {"r": 0.88, "g": 0.9, "b": 0.94}})
        cmds.append({"action": "create_text", "name": f"T_{i+1}", "x": x + 20, "y": 310, "width": 320, "text": f"0{i+1}. サービス名称 {i+1}", "fontSize": 18, "fontStyle": "Bold", "color": {"r": 0.1, "g": 0.1, "b": 0.1}})
    
    # 05_CTA & Footer
    cmds.append({"action": "create_frame", "name": "05_CTA", "x": 0, "y": 1340, "width": 1440, "height": 340, "bg": {"r": 0.05, "g": 0.15, "b": 0.25}})
    cmds.append({"action": "create_text", "name": "CTA_T", "x": 120, "y": 80, "width": 1200, "text": "まずはお気軽にご相談・お問い合わせください", "fontSize": 28, "fontStyle": "Bold", "color": {"r": 1.0, "g": 1.0, "b": 1.0}})
    cmds.append({"action": "create_rect", "name": "CTA_B", "x": 120, "y": 160, "width": 260, "height": 56, "cornerRadius": 8, "color": {"r": 0.0, "g": 0.47, "b": 0.85}})
    cmds.append({"action": "create_text", "name": "CTA_BT", "x": 175, "y": 178, "text": "お問い合わせフォームへ", "fontSize": 16, "fontStyle": "Bold", "color": {"r": 1.0, "g": 1.0, "b": 1.0}})
    
    cmds.append({"action": "create_frame", "name": "06_Footer", "x": 0, "y": 1680, "width": 1440, "height": 180, "bg": {"r": 0.03, "g": 0.08, "b": 0.12}})
    cmds.append({"action": "create_text", "name": "F_Copy", "x": 120, "y": 80, "text": "© 2026 Company Name Inc. All Rights Reserved.", "fontSize": 12, "color": {"r": 0.5, "g": 0.5, "b": 0.5}})
    
    return cmds

def send_to_bridge(commands):
    data = json.dumps({"commands": commands}).encode('utf-8')
    req = urllib.request.Request(BRIDGE_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as res:
            resp = json.loads(res.read().decode('utf-8'))
            print(f"成功: Bridge Server に {resp.get('queued')} 件の描画コマンドを送信しました！")
    except Exception as e:
        print(f"エラー: Bridge Server に接続できませんでした ({e})。先に figma_bridge_server.py を起動してください。")

if __name__ == "__main__":
    send_to_bridge(create_top_wf_commands())
