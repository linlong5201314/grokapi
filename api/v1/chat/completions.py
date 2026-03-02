"""
Grok API 中转站 - Chat Completions Proxy
Vercel Serverless Function

支持两种认证模式：
1. GROK_API_KEY - 使用 xAI 官方 API Key，直接代理到 api.x.ai
2. GROK_SSO_TOKEN - 使用 SSO Token，通过 Grok Web API 代理
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import time
import uuid
import urllib.request
import urllib.error
import urllib.parse
import ssl

# ==================== 配置 ====================
GROK_SSO_TOKEN = os.environ.get('GROK_SSO_TOKEN', '')
GROK_API_KEY = os.environ.get('GROK_API_KEY', '')
GROK_API_BASE = os.environ.get('GROK_API_BASE', 'https://api.x.ai')
GROK_WEB_BASE = os.environ.get('GROK_WEB_BASE', 'https://grok.x.ai')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN', '')  # 保护此代理的访问令牌
DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'grok-3')

# SSL 上下文
ssl_ctx = ssl.create_default_context()

# 模型映射（OpenAI 格式 -> Grok 实际模型标识）
MODEL_ALIASES = {
    'grok-4': 'grok-3',
    'grok-4-heavy': 'grok-3',
    'grok-4-1': 'grok-3',
    'grok-3': 'grok-3',
    'grok-3-mini': 'grok-3-mini',
    'grok-2': 'grok-2',
}


def build_openai_response(content, model='grok-3', finish_reason='stop'):
    """构建 OpenAI 格式的响应"""
    return {
        'id': f'chatcmpl-{uuid.uuid4().hex[:24]}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': model,
        'choices': [{
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': content
            },
            'finish_reason': finish_reason
        }],
        'usage': {
            'prompt_tokens': 0,
            'completion_tokens': 0,
            'total_tokens': 0
        }
    }


def build_error_response(message, error_type='server_error', code=None):
    """构建错误响应"""
    resp = {
        'error': {
            'message': message,
            'type': error_type,
            'param': None,
            'code': code
        }
    }
    return resp


def do_http_request(url, data=None, headers=None, method='POST', timeout=120):
    """执行 HTTP 请求"""
    if data and isinstance(data, (dict, list)):
        data = json.dumps(data).encode('utf-8')
    elif data and isinstance(data, str):
        data = data.encode('utf-8')

    req = urllib.request.Request(url, data=data, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=timeout) as resp:
            return resp.read().decode('utf-8'), resp.status
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        return error_body, e.code
    except urllib.error.URLError as e:
        return str(e.reason), 502
    except Exception as e:
        return str(e), 500


# ==================== API Key 模式 ====================
def proxy_via_api_key(body):
    """使用 xAI API Key 直接代理到官方 API"""
    url = f'{GROK_API_BASE}/v1/chat/completions'

    # 不使用流式（Vercel serverless 对流式支持有限）
    body['stream'] = False

    headers = {
        'Authorization': f'Bearer {GROK_API_KEY}',
        'Content-Type': 'application/json',
    }

    resp_text, status = do_http_request(url, data=body, headers=headers, timeout=120)

    try:
        return json.loads(resp_text), status
    except json.JSONDecodeError:
        return build_error_response(f'Backend error: {resp_text[:500]}'), status


# ==================== SSO Token 模式 ====================
def proxy_via_sso(body):
    """使用 SSO Token 通过 Grok Web API 代理"""
    model = body.get('model', DEFAULT_MODEL)
    actual_model = MODEL_ALIASES.get(model, model)
    messages = body.get('messages', [])
    temperature = body.get('temperature', 0.7)
    max_tokens = body.get('max_tokens', 4096)

    if not messages:
        return build_error_response('messages 不能为空', 'invalid_request_error'), 400

    # 从 messages 构建完整对话文本
    system_prompt = ''
    conversation_parts = []
    last_user_message = ''

    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'system':
            system_prompt = content
        elif role == 'user':
            last_user_message = content
            conversation_parts.append(f'User: {content}')
        elif role == 'assistant':
            conversation_parts.append(f'Assistant: {content}')

    # 构建发送的消息
    if len(messages) <= 2:  # 单轮对话
        full_message = last_user_message
        if system_prompt:
            full_message = f"[System: {system_prompt}]\n\n{last_user_message}"
    else:  # 多轮对话，拼接历史
        history = '\n'.join(conversation_parts[:-1])
        full_message = f"以下是之前的对话历史：\n{history}\n\n请回答最后一个问题：{last_user_message}"
        if system_prompt:
            full_message = f"[System: {system_prompt}]\n\n{full_message}"

    # 请求头
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sso={GROK_SSO_TOKEN}; sso-rw={GROK_SSO_TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Origin': GROK_WEB_BASE,
        'Referer': f'{GROK_WEB_BASE}/',
    }

    try:
        # 步骤 1：创建新对话
        conv_url = f'{GROK_WEB_BASE}/rest/app-chat/conversations/new'
        conv_text, conv_status = do_http_request(
            conv_url, data={}, headers=headers, timeout=30
        )

        if conv_status != 200:
            return build_error_response(
                f'创建对话失败 (HTTP {conv_status}): {conv_text[:200]}',
                'api_error'
            ), conv_status

        try:
            conv_data = json.loads(conv_text)
        except json.JSONDecodeError:
            return build_error_response(
                f'创建对话返回格式错误: {conv_text[:200]}',
                'api_error'
            ), 500

        conv_id = conv_data.get('conversationId', '')
        if not conv_id:
            return build_error_response(
                '无法获取 conversationId',
                'api_error'
            ), 500

        # 步骤 2：发送消息
        msg_url = f'{GROK_WEB_BASE}/rest/app-chat/conversations/{conv_id}/responses'
        msg_body = {
            'message': full_message,
            'modelSlug': actual_model,
            'parentResponseId': '',
            'isReasoning': False,
            'sendFeedbackOnEveryResponse': False,
        }

        resp_text, resp_status = do_http_request(
            msg_url, data=msg_body, headers=headers, timeout=120
        )

        if resp_status != 200:
            return build_error_response(
                f'发送消息失败 (HTTP {resp_status}): {resp_text[:200]}',
                'api_error'
            ), resp_status

        # 步骤 3：解析响应
        content = parse_grok_web_response(resp_text)
        return build_openai_response(content, model), 200

    except Exception as e:
        return build_error_response(f'SSO 代理异常: {str(e)}', 'server_error'), 500


def parse_grok_web_response(response_text):
    """
    解析 Grok Web API 的响应
    响应可能是 SSE 格式或 JSON 格式
    """
    lines = response_text.strip().split('\n')
    content_parts = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 处理 SSE 格式
        if line.startswith('data: '):
            line = line[6:]

        if line == '[DONE]':
            break

        try:
            data = json.loads(line)

            # 尝试多种可能的响应格式
            token = None

            # 格式 1: {"result": {"response": {"token": "..."}}}
            if 'result' in data:
                result = data['result']
                if isinstance(result, dict) and 'response' in result:
                    resp = result['response']
                    if isinstance(resp, dict):
                        token = resp.get('token') or resp.get('text') or resp.get('message')

            # 格式 2: {"token": "..."}
            if token is None and 'token' in data:
                token = data['token']

            # 格式 3: {"text": "..."}
            if token is None and 'text' in data:
                token = data['text']

            # 格式 4: {"delta": {"content": "..."}}
            if token is None and 'delta' in data:
                delta = data['delta']
                if isinstance(delta, dict):
                    token = delta.get('content')

            # 格式 5: {"choices": [{"delta": {"content": "..."}}]}
            if token is None and 'choices' in data:
                choices = data['choices']
                if choices and isinstance(choices[0], dict):
                    delta = choices[0].get('delta', {})
                    if isinstance(delta, dict):
                        token = delta.get('content')

            # 格式 6: {"message": {"content": "..."}}
            if token is None and 'message' in data:
                msg = data['message']
                if isinstance(msg, dict):
                    token = msg.get('content')
                elif isinstance(msg, str):
                    token = msg

            if token:
                content_parts.append(str(token))

        except json.JSONDecodeError:
            # 非 JSON 行，可能是纯文本响应
            if not line.startswith('{') and not line.startswith('['):
                content_parts.append(line)

    if content_parts:
        return ''.join(content_parts)
    else:
        # 如果无法解析，返回原始文本（可能是纯文本响应）
        return response_text.strip()


# ==================== HTTP Handler ====================
class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function Handler"""

    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        """处理 Chat Completions 请求"""
        # 解析请求体
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                raw = self.rfile.read(content_length)
                body = json.loads(raw)
            else:
                body = {}
        except json.JSONDecodeError:
            self._send_json(build_error_response('请求体 JSON 格式错误', 'invalid_request_error'), 400)
            return
        except Exception as e:
            self._send_json(build_error_response(f'请求解析失败: {str(e)}', 'invalid_request_error'), 400)
            return

        # 访问令牌验证
        if AUTH_TOKEN:
            auth_header = self.headers.get('Authorization', '')
            provided_token = auth_header.replace('Bearer ', '').strip()
            if provided_token != AUTH_TOKEN:
                self._send_json(build_error_response('认证失败：无效的访问令牌', 'authentication_error', 'invalid_api_key'), 401)
                return

        # 基本参数验证
        if 'messages' not in body or not body['messages']:
            self._send_json(build_error_response('缺少必填参数 messages', 'invalid_request_error'), 400)
            return

        # 选择代理模式
        if GROK_API_KEY:
            result, status = proxy_via_api_key(body)
        elif GROK_SSO_TOKEN:
            result, status = proxy_via_sso(body)
        else:
            self._send_json(build_error_response(
                '服务未配置：请在 Vercel 环境变量中设置 GROK_API_KEY 或 GROK_SSO_TOKEN',
                'server_error'
            ), 500)
            return

        self._send_json(result, status)

    def do_GET(self):
        """处理 GET 请求 - 返回端点信息"""
        info = {
            'endpoint': '/v1/chat/completions',
            'method': 'POST',
            'description': 'Grok API 中转站 - Chat Completions',
            'auth_mode': 'api_key' if GROK_API_KEY else ('sso_token' if GROK_SSO_TOKEN else 'not_configured'),
            'supported_models': list(MODEL_ALIASES.keys()),
        }
        self._send_json(info, 200)

    def _send_json(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def _set_cors_headers(self):
        """设置 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '86400')

    def log_message(self, format, *args):
        """抑制默认日志输出"""
        pass
