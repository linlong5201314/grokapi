"""
Grok API 中转站 - Health Check
Vercel Serverless Function
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import time


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        sso_configured = bool(os.environ.get('GROK_SSO_TOKEN', ''))
        api_key_configured = bool(os.environ.get('GROK_API_KEY', ''))

        status_data = {
            'status': 'ok',
            'timestamp': int(time.time()),
            'version': '1.0.0',
            'auth': {
                'sso_token': 'configured' if sso_configured else 'not_configured',
                'api_key': 'configured' if api_key_configured else 'not_configured',
            },
            'endpoints': {
                'chat_completions': '/v1/chat/completions',
                'models': '/v1/models',
                'health': '/api/health',
            }
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(status_data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        pass
