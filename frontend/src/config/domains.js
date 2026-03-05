// 支持的域名列表
export const SUPPORTED_DOMAINS = [
    "gemini.google.com",
    "chatgpt.com",
    "grok.com",
    "chat.deepseek.com",
    "chat.qwen.ai",
    "www.qianwen.com",
    "www.doubao.com",
    "poe.com"
];

// 自动生成用于 manifest.json 的匹配规则
export const MANIFEST_MATCHES = SUPPORTED_DOMAINS.map(domain => `https://${domain}/*`);