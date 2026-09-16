#!/usr/bin/env python3
"""
コンテンツ幅1200px トップページワイヤーフレーム(WF) 自動描画送信メインスクリプト
"""

import urllib.request
import json
import sys
import os

# 同一ディレクトリのモジュールを読み込めるようにパス追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wf_builder import build_part_1, build_part_2, build_part_3, CANVAS_W, C_BG_MAIN

BRIDGE_URL = "http://localhost:3030/push"

def assemble_all_commands():
    cmds = []
    
    # 概算トータル高さ計算のために全セクションを順次構築
    c1, y1 = build_part_1(0)
    c2, y2 = build_part_2(y1)
    c3, y3 = build_part_3(y2)
    
    total_height = y3
    
    # 親フレームを追加
    cmds.append({
        "action": "create_frame",
        "key": "parent_wf_1200",
        "name": "PC_Top_Wireframe_1200pxContent",
        "x": 0, "y": 0,
        "width": CANVAS_W, "height": total_height,
        "bg": C_BG_MAIN,
        "clipsContent": False
    })
    
    cmds.extend(c1)
    cmds.extend(c2)
    cmds.extend(c3)
    
    return cmds, total_height

def send_to_bridge(commands):
    data = json.dumps({"commands": commands}).encode('utf-8')
    req = urllib.request.Request(BRIDGE_URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as res:
            resp = json.loads(res.read().decode('utf-8'))
            print(f"✅ 成功: Bridge Server に {resp.get('queued')} 件の描画コマンドを送信しました！")
            return True
    except Exception as e:
        print(f"⚠️ 注意: Bridge Server (localhost:3030) に接続できませんでした ({e})。")
        print("💡 次のコマンドで Bridge Server を起動してください:")
        print("   python3 00_Tools/figma/figma_bridge_server.py")
        return False

if __name__ == "__main__":
    commands, total_height = assemble_all_commands()
    print(f"📐 描画準備完了: コンテンツ幅 1200px トップWF (全幅 1440px × 高さ {total_height}px)")
    print(f"📦 生成コマンド数: {len(commands)} 件")
    send_to_bridge(commands)

