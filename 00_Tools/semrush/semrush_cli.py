#!/usr/bin/env python3
"""
Semrush API CLI Tool
Semrush APIから各種データを取得するスクリプト
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# .envファイルの読み込み
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

SEMRUSH_API_KEY = os.getenv("SEMRUSH_API_KEY", "")

def check_api_key():
    if not SEMRUSH_API_KEY or SEMRUSH_API_KEY == "your_semrush_api_key_here":
        print("エラー: .env ファイルに SEMRUSH_API_KEY が正しく設定されていません。")
        sys.exit(1)

def send_request(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            return res.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        return f"API呼び出しエラー (HTTP {e.code}): {body or e.reason}"
    except Exception as e:
        return f"API呼び出しエラー: {e}"

def fetch_domain_overview(domain, database="us"):
    """ドメインの概要データを取得"""
    check_api_key()
    base_url = "https://api.semrush.com/"
    params = {
        "type": "domain_ranks",
        "key": SEMRUSH_API_KEY,
        "export_columns": "Dn,Rk,Or,Ot,Oc,Ad,At,Ac",
        "domain": domain,
        "database": database
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return send_request(url)

def fetch_keyword_overview(phrase, database="us"):
    """キーワードの検索ボリューム・競合度データを取得"""
    check_api_key()
    base_url = "https://api.semrush.com/"
    params = {
        "type": "phrase_this",
        "key": SEMRUSH_API_KEY,
        "export_columns": "Ph,Nq,Cp,Co,Nr",
        "phrase": phrase,
        "database": database
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return send_request(url)

def main():
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python semrush_cli.py domain <domain_name> [database(jp/us/...)]")
        print("  python semrush_cli.py keyword <keyword> [database(jp/us/...)]")
        sys.exit(1)

    cmd_type = sys.argv[1]
    target = sys.argv[2]
    db = sys.argv[3] if len(sys.argv) > 3 else "jp"

    if cmd_type == "domain":
        print(fetch_domain_overview(target, database=db))
    elif cmd_type == "keyword":
        print(fetch_keyword_overview(target, database=db))
    else:
        print(f"未対応のコマンド: {cmd_type}")

if __name__ == "__main__":
    main()

