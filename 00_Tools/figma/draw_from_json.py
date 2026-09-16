#!/usr/bin/env python3
"""
JSONからFigmaコマンドを生成して Bridge Server へ送信する汎用描画エンジン
"""

import sys
import json
import urllib.request

BRIDGE_URL = "http://localhost:3030/push"

def send_json_to_figma(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        commands = data.get("commands", [])
        if not commands:
            print("エラー: JSON内に valid な 'commands' がありません。")
            return

        payload = json.dumps({"commands": commands}).encode('utf-8')
        req = urllib.request.Request(BRIDGE_URL, data=payload, headers={'Content-Type': 'application/json'})
        
        with urllib.request.urlopen(req) as res:
            resp = json.loads(res.read().decode('utf-8'))
            print(f"成功: {resp.get('queued')} 件の描画コマンドをFigmaに送信しました！")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python3 draw_from_json.py <path_to_json>")
        sys.exit(1)
    send_json_to_figma(sys.argv[1])
