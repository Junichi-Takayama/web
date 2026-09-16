#!/usr/bin/env python3
"""
Figma API CLI Tool
Figma APIからデザインファイル情報、ノードデータ、画像書き出しURLなどを取得するスクリプト
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

def load_env():
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()

FIGMA_PAT = os.getenv("FIGMA_PAT", "")

def check_token():
    if not FIGMA_PAT or FIGMA_PAT == "your_figma_pat_here":
        print("エラー: .env ファイルに FIGMA_PAT が正しく設定されていません。")
        sys.exit(1)

def send_figma_request(endpoint):
    check_token()
    url = f"https://api.figma.com/v1{endpoint}"
    headers = {
        "X-Figma-Token": FIGMA_PAT,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            data = res.read().decode('utf-8')
            return json.loads(data)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        return {"error": f"HTTP {e.code}: {body or e.reason}"}
    except Exception as e:
        return {"error": str(e)}

def get_me():
    """現在のユーザー情報を取得 (疎通確認用)"""
    return send_figma_request("/me")

def get_file(file_key):
    """指定したファイルの概要・構造を取得"""
    return send_figma_request(f"/files/{file_key}")

def get_file_nodes(file_key, ids):
    """指定したノードの詳細を取得"""
    ids_param = ",".join(ids) if isinstance(ids, list) else ids
    return send_figma_request(f"/files/{file_key}/nodes?ids={urllib.parse.quote(ids_param)}")

def get_images(file_key, ids, format="png", scale=1):
    """指定したノードの画像書き出しURLを取得"""
    ids_param = ",".join(ids) if isinstance(ids, list) else ids
    endpoint = f"/images/{file_key}?ids={urllib.parse.quote(ids_param)}&format={format}&scale={scale}"
    return send_figma_request(endpoint)

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python figma_cli.py me                        # 疎通テスト")
        print("  python figma_cli.py file <file_key>           # ファイルメタデータ・構造取得")
        print("  python figma_cli.py image <file_key> <node_id> # 画像書き出しURL取得")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "me":
        res = get_me()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "file" and len(sys.argv) >= 3:
        file_key = sys.argv[2]
        res = get_file(file_key)
        # レスポンスサイズが大きい場合があるため必要情報を抜粋表示
        if "error" in res:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            name = res.get("name", "")
            last_modified = res.get("lastModified", "")
            document = res.get("document", {})
            pages = [node.get("name") for node in document.get("children", [])]
            print(f"ファイル名: {name}")
            print(f"最終更新日時: {last_modified}")
            print(f"ページ一覧: {', '.join(pages)}")
    elif cmd == "image" and len(sys.argv) >= 4:
        file_key = sys.argv[2]
        node_id = sys.argv[3]
        res = get_images(file_key, node_id)
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("不正な引数です。")

if __name__ == "__main__":
    main()
