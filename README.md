# Grok API 中转站

> 支持 SSO Token 和 API Key 的 Grok 模型中转代理，兼容 OpenAI API 格式，一键部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fxianyu110%2Fgrokapi)

---

## ✨ 特性

- **OpenAI API 兼容** — 支持所有兼容 OpenAI 格式的客户端（ChatGPT Next Web、LobeChat、OpenCat 等）
- **双重认证** — 支持 SSO Token（grokzhuce 注册工具生成）和 xAI 官方 API Key
- **Vercel 部署** — Serverless 架构，零成本部署
- **内置聊天界面** — MkDocs Material 文档站 + Web 聊天 UI
- **中文友好** — 完整的中文文档与界面

## 📦 项目结构

```
grokapi/
├── api/                    # Vercel Serverless Functions
│   ├── health.py          # 健康检查端点
│   └── v1/
│       ├── chat/
│       │   └── completions.py  # 聊天补全 API（核心）
│       └── models.py      # 模型列表 API
├── docs/                   # MkDocs 文档源码
│   ├── index.md           # 首页
│   ├── chat.md            # 在线聊天界面
│   ├── api.md             # API 文档
│   ├── zh.md              # 部署指南
│   └── models.md          # 模型参考
├── mkdocs.yml             # MkDocs 配置
├── vercel.json            # Vercel 部署配置
├── requirements.txt       # Python 依赖
└── .env.example           # 环境变量模板
```

## 🚀 快速部署

### 1. 一键部署

点击上方 **Deploy with Vercel** 按钮，或手动 Fork 后导入 Vercel。

### 2. 配置环境变量

在 Vercel Dashboard → Settings → Environment Variables 中添加：

| 变量名 | 说明 | 必填 |
|---|---|---|
| `GROK_SSO_TOKEN` | Grok SSO Token（JWT 格式，从 grokzhuce 获取） | 二选一 |
| `GROK_API_KEY` | xAI 官方 API Key（从 console.x.ai 获取） | 二选一 |
| `AUTH_TOKEN` | 保护中转站的访问令牌（客户端需要提供此令牌） | 可选 |

> 如果同时设置了 `GROK_API_KEY` 和 `GROK_SSO_TOKEN`，优先使用 API Key。

### 3. 重新部署

添加环境变量后，在 Deployments 页面选择 Redeploy。

## 📡 API 使用

### 端点

| 端点 | 方法 | 说明 |
|---|---|---|
| `/v1/chat/completions` | POST | 聊天补全 |
| `/v1/models` | GET | 模型列表 |
| `/api/health` | GET | 健康检查 |

### cURL 示例

```bash
curl -X POST "https://你的域名/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [{"role": "user", "content": "你好！"}]
  }'
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
    messages=[{"role": "user", "content": "你好！"}]
)
print(response.choices[0].message.content)
```

## 🧠 支持的模型

| 模型 | API 标识 | 说明 |
|---|---|---|
| Grok 3 | `grok-3` | 主力通用模型（推荐） |
| Grok 3 Mini | `grok-3-mini` | 轻量快速模型 |
| Grok 4 | `grok-4` | 新一代通用模型 |
| Grok 4 Heavy | `grok-4-heavy` | 高性能推理模型 |
| Grok 4.1 | `grok-4-1` | 内容优化模型 |

## 🔑 获取 SSO Token

使用 [grokzhuce](https://github.com/xianyu110/grokzhuce) 批量注册工具：

```bash
python grok.py
```

注册成功后，Token 保存在 `keys/` 目录下。

## ⚠️ 免责声明

- 本项目不隶属于 xAI 或 Grok 官方
- 仅用于技术学习与交流
- 请勿用于违法或违规用途
- SSO Token 有有效期，过期需重新获取

## 📄 License

MIT License