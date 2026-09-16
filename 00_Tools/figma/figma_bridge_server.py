#!/usr/bin/env python3
"""
Cline Figma Bridge Server
Cline (AI) と Figma デスクトップアプリ（プラグイン）をつなぐローカルHTTPサーバー
"""

import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

command_queue = []

class BridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # ログ表示の抑制
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        global command_queue
        if self.path == '/poll':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            payload = {"commands": command_queue}
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))
            if command_queue:
                print(f"[Bridge Server] Figmaに {len(command_queue)} 件のコマンドを送信しました。")
                command_queue = []
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global command_queue
        if self.path == '/push':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                cmds = data.get("commands", [])
                command_queue.extend(cmds)
                print(f"[Bridge Server] 新規コマンド {len(cmds)} 件を受信・キューに追加しました。")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "queued": len(cmds)}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=3030):
    server_address = ('', port)
    httpd = HTTPServer(server_address, BridgeHandler)
    print(f"==================================================")
    print(f"  Cline Figma Bridge Server 起動中 (Port {port})")
    print(f"  http://localhost:{port}/poll")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nサーバーを停止しました。")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3030
    run_server(port)
