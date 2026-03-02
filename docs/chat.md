# 💬 在线体验

<style>
.chat-container {
    max-width: 800px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, "Noto Sans SC", sans-serif;
}
.chat-config {
    background: var(--md-code-bg-color, #f5f5f5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}
.chat-config label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
    color: var(--md-default-fg-color--light, #666);
}
.chat-config input, .chat-config select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--md-default-fg-color--lightest, #ddd);
    border-radius: 8px;
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
    background: var(--md-default-bg-color, #fff);
    color: var(--md-default-fg-color, #333);
    box-sizing: border-box;
}
.chat-config input:focus, .chat-config select:focus {
    outline: none;
    border-color: var(--md-primary-fg-color, #1976d2);
    box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
}
.chat-messages {
    border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0);
    border-radius: 12px;
    height: 450px;
    overflow-y: auto;
    padding: 1rem;
    margin-bottom: 1rem;
    background: var(--md-default-bg-color, #fff);
}
.chat-msg {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.chat-msg.user {
    align-items: flex-end;
}
.chat-msg.assistant {
    align-items: flex-start;
}
.chat-msg .bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    line-height: 1.6;
    word-break: break-word;
    white-space: pre-wrap;
}
.chat-msg.user .bubble {
    background: var(--md-primary-fg-color, #1976d2);
    color: white;
    border-bottom-right-radius: 4px;
}
.chat-msg.assistant .bubble {
    background: var(--md-code-bg-color, #f0f0f0);
    color: var(--md-default-fg-color, #333);
    border-bottom-left-radius: 4px;
}
.chat-msg .role-label {
    font-size: 0.75rem;
    color: var(--md-default-fg-color--lighter, #999);
    margin-bottom: 0.25rem;
    padding: 0 0.5rem;
}
.chat-input-area {
    display: flex;
    gap: 0.5rem;
}
.chat-input-area textarea {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid var(--md-default-fg-color--lightest, #ddd);
    border-radius: 12px;
    font-size: 0.95rem;
    resize: none;
    height: 60px;
    font-family: inherit;
    background: var(--md-default-bg-color, #fff);
    color: var(--md-default-fg-color, #333);
}
.chat-input-area textarea:focus {
    outline: none;
    border-color: var(--md-primary-fg-color, #1976d2);
    box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
}
.chat-input-area button {
    padding: 0.75rem 1.5rem;
    background: var(--md-primary-fg-color, #1976d2);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}
.chat-input-area button:hover {
    background: var(--md-primary-fg-color--dark, #1565c0);
    transform: translateY(-1px);
}
.chat-input-area button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
}
.chat-status {
    text-align: center;
    padding: 0.5rem;
    font-size: 0.85rem;
    color: var(--md-default-fg-color--lighter, #999);
}
.chat-status.error {
    color: #d32f2f;
}
.chat-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
}
.chat-actions button {
    padding: 0.4rem 1rem;
    background: transparent;
    color: var(--md-default-fg-color--light, #666);
    border: 1px solid var(--md-default-fg-color--lightest, #ddd);
    border-radius: 8px;
    font-size: 0.8rem;
    cursor: pointer;
    transition: all 0.2s;
}
.chat-actions button:hover {
    background: var(--md-code-bg-color, #f5f5f5);
}
.loading-dots::after {
    content: '';
    animation: dots 1.5s infinite;
}
@keyframes dots {
    0%, 20% { content: '.'; }
    40% { content: '..'; }
    60%, 100% { content: '...'; }
}
.config-toggle {
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--md-primary-fg-color, #1976d2);
}
.config-toggle:hover {
    opacity: 0.8;
}
.config-body {
    display: none;
}
.config-body.show {
    display: block;
}
</style>

<div class="chat-container" markdown>

<div class="chat-config">
    <div class="config-toggle" onclick="toggleConfig()">
        <span id="config-arrow">▶</span> API 配置
    </div>
    <div class="config-body" id="config-body">
        <label>API 地址</label>
        <input type="text" id="api-endpoint" placeholder="留空使用当前站点" value="">
        <label>API Key / 访问令牌</label>
        <input type="password" id="api-key" placeholder="如果设置了 AUTH_TOKEN 则需填写">
        <label>模型</label>
        <select id="model-select">
            <option value="grok-3">Grok 3（通用）</option>
            <option value="grok-3-mini">Grok 3 Mini（轻量）</option>
            <option value="grok-4">Grok 4（通用）</option>
            <option value="grok-4-heavy">Grok 4 Heavy（高性能）</option>
            <option value="grok-4-1">Grok 4.1（优化版）</option>
        </select>
    </div>
</div>

<div class="chat-messages" id="chat-messages">
    <div class="chat-status">👋 发送消息开始对话</div>
</div>

<div class="chat-input-area">
    <textarea id="chat-input" placeholder="输入你的消息... (Enter 发送, Shift+Enter 换行)" onkeydown="handleKeyDown(event)"></textarea>
    <button id="send-btn" onclick="sendMessage()">发送</button>
</div>

<div class="chat-actions">
    <span class="chat-status" id="status-text"></span>
    <button onclick="clearChat()">清空对话</button>
</div>

</div>

<script>
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const statusText = document.getElementById('status-text');
let messages = [];

function toggleConfig() {
    const body = document.getElementById('config-body');
    const arrow = document.getElementById('config-arrow');
    if (body.classList.contains('show')) {
        body.classList.remove('show');
        arrow.textContent = '▶';
    } else {
        body.classList.add('show');
        arrow.textContent = '▼';
    }
}

function getApiEndpoint() {
    const input = document.getElementById('api-endpoint').value.trim();
    if (input) return input.replace(/\/$/, '');
    return window.location.origin;
}

function addMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${role}`;
    
    const label = document.createElement('div');
    label.className = 'role-label';
    label.textContent = role === 'user' ? '你' : 'Grok';
    
    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = content;
    
    msgDiv.appendChild(label);
    msgDiv.appendChild(bubble);
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return bubble;
}

async function sendMessage() {
    const content = chatInput.value.trim();
    if (!content) return;
    
    chatInput.value = '';
    sendBtn.disabled = true;
    
    // 清除欢迎消息
    const welcomeMsg = chatMessages.querySelector('.chat-status');
    if (welcomeMsg) welcomeMsg.remove();
    
    // 添加用户消息
    addMessage('user', content);
    messages.push({ role: 'user', content: content });
    
    // 添加加载指示
    const assistantBubble = addMessage('assistant', '');
    assistantBubble.innerHTML = '<span class="loading-dots">思考中</span>';
    statusText.textContent = '正在请求...';
    statusText.className = 'chat-status';
    
    try {
        const endpoint = getApiEndpoint();
        const apiKey = document.getElementById('api-key').value.trim();
        const model = document.getElementById('model-select').value;
        
        const headers = { 'Content-Type': 'application/json' };
        if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`;
        
        const response = await fetch(`${endpoint}/v1/chat/completions`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                model: model,
                messages: messages,
                temperature: 0.7,
                max_tokens: 4096,
                stream: false
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            assistantBubble.textContent = `❌ 错误: ${data.error.message}`;
            assistantBubble.style.color = '#d32f2f';
            statusText.textContent = '请求失败';
            statusText.className = 'chat-status error';
            messages.pop(); // 移除失败的用户消息
        } else if (data.choices && data.choices[0]) {
            const reply = data.choices[0].message.content;
            assistantBubble.textContent = reply;
            messages.push({ role: 'assistant', content: reply });
            statusText.textContent = `模型: ${data.model || model}`;
            statusText.className = 'chat-status';
        } else {
            assistantBubble.textContent = '⚠️ 未收到有效响应';
            statusText.textContent = '响应异常';
            statusText.className = 'chat-status error';
        }
    } catch (err) {
        assistantBubble.textContent = `❌ 网络错误: ${err.message}`;
        assistantBubble.style.color = '#d32f2f';
        statusText.textContent = '连接失败';
        statusText.className = 'chat-status error';
        messages.pop();
    }
    
    sendBtn.disabled = false;
    chatInput.focus();
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function clearChat() {
    messages = [];
    chatMessages.innerHTML = '<div class="chat-status">👋 发送消息开始对话</div>';
    statusText.textContent = '';
}
</script>

---

## 使用说明

!!! tip "快速开始"
    1. 如果部署时未设置 `AUTH_TOKEN`，可以直接发送消息
    2. 如果设置了 `AUTH_TOKEN`，需要在 **API 配置** 中填写访问令牌
    3. 点击 **▶ API 配置** 展开设置面板

!!! info "外部接入"
    你也可以使用任何支持 OpenAI API 的客户端接入本中转站：
    
    - **API 地址**: `https://你的域名/v1/chat/completions`
    - **模型列表**: `https://你的域名/v1/models`
    - **认证方式**: `Authorization: Bearer YOUR_TOKEN`

    支持的客户端：ChatGPT Next Web、LobeChat、OpenCat、BotGem 等
