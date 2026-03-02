# 📡 API 接口文档

## 基本信息

**Base URL:** `https://你的vercel域名/v1`

**认证方式:** Bearer Token（如果设置了 `AUTH_TOKEN` 环境变量）

## 端点列表

| 端点 | 方法 | 说明 |
|---|---|---|
| `/v1/chat/completions` | POST | 聊天补全（主要端点） |
| `/v1/models` | GET | 获取可用模型列表 |
| `/api/health` | GET | 健康检查 |

## 聊天补全

### 请求格式

```json
{
  "model": "grok-3",
  "messages": [
    {
      "role": "system",
      "content": "你是一个有帮助的助手"
    },
    {
      "role": "user",
      "content": "你好！"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4096,
  "stream": false
}
```

### 支持的模型

| 模型名称 | API 标识 | 实际映射 | 说明 |
|---|---|---|---|
| Grok 3 | `grok-3` | grok-3 | 主力模型 |
| Grok 3 Mini | `grok-3-mini` | grok-3-mini | 轻量模型 |
| Grok 4 | `grok-4` | grok-3 | 别名映射 |
| Grok 4 Heavy | `grok-4-heavy` | grok-3 | 别名映射 |
| Grok 4.1 | `grok-4-1` | grok-3 | 别名映射 |

## 请求示例

### cURL

```bash
curl -X POST "https://你的域名/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [
      {
        "role": "user",
        "content": "请介绍一下人工智能的发展历史"
      }
    ],
    "temperature": 0.7,
    "max_tokens": 2000
  }'
```

### Python

```python
import requests

url = "https://你的域名/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_AUTH_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "model": "grok-3",
    "messages": [
        {"role": "user", "content": "写一个 Python 斐波那契函数"}
    ],
    "temperature": 0.3,
    "max_tokens": 800
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Python（OpenAI SDK）

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_AUTH_TOKEN",
    base_url="https://你的域名/v1"
)

response = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "user", "content": "你好，请做一个自我介绍"}
    ]
)
print(response.choices[0].message.content)
```

### JavaScript

```javascript
const response = await fetch('https://你的域名/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_AUTH_TOKEN',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'grok-3',
    messages: [
      { role: 'user', content: '解释一下什么是机器学习' }
    ],
    temperature: 0.5,
    max_tokens: 600
  })
});

const result = await response.json();
console.log(result.choices[0].message.content);
```

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---|---|---|
| `model` | string | ✅ | - | 模型标识 |
| `messages` | array | ✅ | - | 对话消息列表 |
| `temperature` | number | ❌ | 0.7 | 输出随机性 (0-2) |
| `max_tokens` | number | ❌ | 4096 | 最大输出令牌数 |
| `stream` | boolean | ❌ | false | 流式输出（暂不支持） |
| `top_p` | number | ❌ | 1 | 核采样参数 (0-1) |

## 消息角色

| 角色 | 说明 |
|---|---|
| `system` | 系统指令，设定 AI 行为 |
| `user` | 用户消息 |
| `assistant` | AI 助手的历史回复 |

## 响应格式

### 成功响应

```json
{
  "id": "chatcmpl-abc123def456",
  "object": "chat.completion",
  "created": 1709366400,
  "model": "grok-3",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "你好！我是 Grok，很高兴认识你..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0
  }
}
```

### 错误响应

```json
{
  "error": {
    "message": "认证失败：无效的访问令牌",
    "type": "authentication_error",
    "param": null,
    "code": "invalid_api_key"
  }
}
```

## 错误码

| 状态码 | 说明 | 解决方案 |
|---|---|---|
| 400 | 请求参数错误 | 检查 JSON 格式和必填参数 |
| 401 | 认证失败 | 检查 AUTH_TOKEN 是否正确 |
| 500 | 服务器错误 | 检查 SSO Token 或 API Key 配置 |
| 502 | 上游服务不可用 | Grok 服务暂时不可用，稍后重试 |

## 最佳实践

!!! tip "温度设置建议"
    - **创意写作**: `temperature: 0.8-1.0`
    - **代码生成**: `temperature: 0.1-0.3`
    - **日常对话**: `temperature: 0.5-0.7`

!!! tip "多轮对话"
    将之前的对话历史包含在 `messages` 数组中，实现上下文连续的多轮对话。

!!! warning "注意事项"
    - Vercel Serverless 函数有 120 秒超时限制
    - 当前不支持流式输出（stream: true）
    - SSO Token 有有效期，过期需要更新