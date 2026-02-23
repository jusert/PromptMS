const ADAPTERS = {
    'gemini.google.com': {
        inputSelector: 'div[role="textbox"]',
        inject: (el, content) => {
            el.focus();
            document.execCommand('selectAll', false, null);
            document.execCommand('insertText', false, content);
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }
    },
    'chatgpt.com': {
        inputSelector: '#prompt-textarea', // ChatGPT 目前的主输入框 ID
        inject: (el, content) => {
            el.focus();
            // ChatGPT 使用 ContentEditable，insertText 通常有效
            document.execCommand('insertText', false, content);
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }
    },
    // 'grok.com': {
    //     inputSelector: 'textarea, [contenteditable="true"]',
    //     inject: (el, content) => {
    //         el.focus();
    //         document.execCommand('insertText', false, content);
    //     }
    // },
    'www.deepseek.com': {
        inputSelector: 'textarea', // DeepSeek 常用 textarea
        inject: (el, content) => {
            el.focus();
            // 针对标准 textarea，可以先设置值再触发事件
            el.value = content;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    },
    'default': {
        inputSelector: 'textarea, [contenteditable="true"]',
        inject: (el, content) => {
            el.focus();
            document.execCommand('insertText', false, content);
        }
    }
};

/**
 * 获取适配器：根据当前域名匹配，匹配不到则返回默认适配器
 */
const getAdapter = () => {
    const host = window.location.hostname;
    // 兼容带 www 和不带 www 的情况
    const key = Object.keys(ADAPTERS).find(k => host.includes(k));
    return ADAPTERS[key] || ADAPTERS['default'];
};