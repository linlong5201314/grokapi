"""
Grok API 中转站 - Models Listing
Vercel Serverless Function
"""

from http.server import BaseHTTPRequestHandler
import json
import time

MODELS = [
    {
        'id': 'grok-3',
        'object': 'model',
        'created': int(time.time()),
        'owned_by': 'xai',
        'permission': [],
        'root': 'grok-3',
        'parent': None,
    },
    {
        'id': 'grok-3-mini',
        'object': 'model',
        'created': int(time.time()),
        'owned_by': 'xai',
        'permission': [],
        'root': 'grok-3-mini',
        'parent': None,
    },
    {
        'id': 'grok-4',
        'object': 'model',
        'created': int(time.time()),
        'owned_by': 'xai',
        'permission': [],
        'root': 'grok-4',
        'parent': None,
    },
    {
        'id': 'grok-4-heavy',
        'object': 'model',
        'created': int(time.time()),
        'owned_by': 'xai',
        'permission': [],
        'root': 'grok-4-heavy',
        'parent': None,
    },
    {
        'id': 'grok-4-1',
        'object': 'model',
        'created': int(time.time()),
        'owned_by': 'xai',
        'permission': [],
        'root': 'grok-4-1',
        'parent': None,
    },
]


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            'object': 'list',
            'data': MODELS,
        }
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def log_message(self, format, *args):
        pass
