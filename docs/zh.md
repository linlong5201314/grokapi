# 📖 部署与使用指南

## 一键部署到 Vercel

### 第一步：Fork 仓库

1. 打开 [github.com/xianyu110/grokapi](https://github.com/xianyu110/grokapi)
2. 点击右上角 **Fork** 按钮

### 第二步：部署到 Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fxianyu110%2Fgrokapi)

1. 登录 [vercel.com](https://vercel.com)（可使用 GitHub 账号登录）
2. 点击上方部署按钮，或手动导入你 Fork 的仓库
3. Vercel 会自动检测项目配置并开始构建
4. 等待构建完成（约 1-2 分钟）

### 第三步：配置环境变量

部署完成后，进入 Vercel 项目页面：

1. 点击 **Settings** → **Environment Variables**
2. 添加以下变量：

| 变量名 | 值 | 说明 |
|---|---|---|
| `GROK_SSO_TOKEN` | 你的 SSO Token | 从 grokzhuce 获取的 JWT Token |
| `AUTH_TOKEN` | 自定义密码（可选） | 保护你的中转站不被他人使用 |

!!! tip "获取 SSO Token"
    使用 [grokzhuce](https://github.com/xianyu110/grokzhuce) 注册工具：
    
    1. 运行 `python grok.py` 批量注册
    2. 成功后在 `keys/` 目录找到 Token 文件
    3. 复制其中的 JWT Token 字符串

!!! info "也支持 xAI 官方 API Key"
    如果你有 xAI 官方 API Key（从 [console.x.ai](https://console.x.ai) 获取），
    可以设置 `GROK_API_KEY` 变量代替 SSO Token，效果更稳定。

### 第四步：重新部署

添加环境变量后需要重新部署：

1. 进入 **Deployments** 页面
2. 点击最近一次部署的 **...** 菜单
3. 选择 **Redeploy**

## 使用方式

### 方式一：网页在线聊天

直接访问你的 Vercel 域名，进入 **在线体验** 页面即可对话。

### 方式二：API 接口调用

```bash
curl -X POST "https://你的域名/v1/chat/completions" \
  -H "Authorization: Bearer 你的AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-3",
    "messages": [{"role": "user", "content": "你好！"}]
  }'
```

### 方式三：第三方客户端接入

支持所有兼容 OpenAI API 的客户端：

| 客户端 | 设置方式 |
|---|---|
| **ChatGPT Next Web** | Settings → API Endpoint 填入你的域名 |
| **LobeChat** | 设置 → 模型服务商 → 自定义 OpenAI |
| **OpenCat** | 设置 → API 域名 |
| **BotGem** | 设置 → Custom API |
| **Chatbox** | 设置 → API Host |

配置参数：

- **API 地址**: `https://你的vercel域名`
- **API Key**: 你设置的 `AUTH_TOKEN`（如果没设置则留空）
- **模型**: `grok-3`、`grok-4` 等

## 支持的模型

| 模型 | API 标识 | 推荐场景 |
|---|---|---|
| Grok 3 | `grok-3` | 通用对话（推荐） |
| Grok 3 Mini | `grok-3-mini` | 快速回复 |
| Grok 4 | `grok-4` | 对话问答 |
| Grok 4 Heavy | `grok-4-heavy` | 复杂推理 |
| Grok 4.1 | `grok-4-1` | 内容创作 |

## 常见问题

??? question "部署后访问显示 404？"
    检查 Vercel 构建是否成功，查看 Deployments 页面的构建日志。

??? question "API 请求返回认证失败？"
    1. 确认环境变量已正确设置
    2. 确认已重新部署
    3. 如果设置了 AUTH_TOKEN，请求时需要在 Header 中携带

??? question "SSO Token 过期了怎么办？"
    SSO Token 有有效期，过期后需要重新注册获取。
    更新 Vercel 环境变量中的 `GROK_SSO_TOKEN` 并重新部署即可。

??? question "可以同时使用多个 SSO Token 吗？"
    目前只支持单个 Token。如需轮询多个 Token，可以自行修改 API 代码。