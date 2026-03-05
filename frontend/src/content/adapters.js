const ADAPTERS = {
    // 预留位置，只有当 default 搞不定时再写具体适配逻辑
    // 'special-ai.com': {
    //     inputSelector: '#very-special-input',
    //     inject: (el, content) => { ... }
    // }
};

/**
 * 获取当前页面的适配器
 */
export const getAdapter = () => {
    const host = window.location.hostname;
    const key = Object.keys(ADAPTERS).find(k => host.includes(k));
    
    // 如果匹配到特定适配器，将其与 default 合并（保留特定网站的覆盖能力）
    const adapter = ADAPTERS[key] || {};
    
    return {
        inputSelector: adapter.inputSelector || 'textarea, [contenteditable="true"]',
        inject: adapter.inject || ((el, content) => {
            el.focus();
            if (el.tagName === 'TEXTAREA' || el.tagName === 'INPUT') {
                // 在当前光标位置插入，而不是覆盖全文
                const start = el.selectionStart;
                const end = el.selectionEnd;
                el.setRangeText(content, start, end, 'end');
                el.dispatchEvent(new Event('input', { bubbles: true }));
            } else {
                const dataTransfer = new DataTransfer();
                dataTransfer.setData('text/plain', content);
                el.dispatchEvent(new ClipboardEvent('paste', {
                    clipboardData: dataTransfer,
                    bubbles: true,
                    cancelable: true
                }));
            }
        })
    };
};