/**
 * 格式化预览文本：如果内容过长，仅保留首尾
 * @param {string} text 原始输入内容
 * @returns {string} 格式化后的内容
 */
const formatValuePreview = (text) => {
    if (!text) return "";
    // 如果字符长度超过 50，保留前 20 和 后 20，中间用 ... 链接
    if (text.length > 50) {
        return `${text.slice(0, 20)}...${text.slice(-20)}`;
    }
    return text;
};

/**
 * 实时预览函数：将模板中的变量替换为当前输入的值（截断展示）
 */
const getPreviewText = (template, inputs) => {
    let preview = template;
    inputs.forEach(input => {
        const varPlaceholder = input.dataset.var; // 例如 {{code}}
        const rawValue = input.value;
        
        // 预览时使用格式化后的内容，如果是空则显示占位提示
        const displayValue = rawValue 
            ? `<span style="color: #007aff; font-weight: 500;">${formatValuePreview(rawValue)}</span>`
            : `<span style="color: #999;">[等待输入 ${varPlaceholder}]</span>`;
        
        preview = preview.replaceAll(varPlaceholder, displayValue);
    });
    return preview;
};

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "INJECT_PROMPT") {
        const content = request.content;
        const adapter = getAdapter();
        const inputEl = document.querySelector(adapter.inputSelector);

        if (!inputEl) {
            sendResponse({ status: "error", message: "未找到输入框" });
            return;
        }

        const varRegex = /\{\{(.+?)\}\}/g;
        const variables = [...new Set(content.match(varRegex) || [])];

        if (variables.length > 0) {
            renderVariablePanel(content, variables, (finalText) => {
                adapter.inject(inputEl, finalText);
            });
            sendResponse({ status: "success" });
        } else {
            adapter.inject(inputEl, content);
            sendResponse({ status: "success" });
        }
    }
    return true;
});

// 替换 content.js 中的 renderVariablePanel 函数
function renderVariablePanel(template, variables, onConfirm) {
    let host = document.getElementById('prompt-ms-variable-host');
    if (host) host.remove();

    host = document.createElement('div');
    host.id = 'prompt-ms-variable-host';
    const shadow = host.attachShadow({ mode: 'open' });
    document.body.appendChild(host);

    const container = document.createElement('div');
    container.className = 'modal-overlay';
    
    const style = document.createElement('style');
    style.textContent = `
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.6); display: flex; align-items: center; justify-content: center;
            z-index: 2147483647; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            backdrop-filter: blur(4px);
        }
        .modal-card {
            background: #ffffff !important; width: 700px; border-radius: 14px; padding: 20px;
            box-shadow: 0 24px 48px rgba(0,0,0,0.3); display: flex; flex-direction: column; 
            max-height: 80vh; border: 1px solid rgba(255,255,255,0.2);
        }
        .header { 
            font-size: 16px; font-weight: 600; margin-bottom: 16px; 
            color: #1a1a1a !important; display: flex; align-items: center; gap: 8px; 
        }
        .header::before { content: ""; width: 3px; height: 16px; background: #007aff; border-radius: 2px; }
        
        .content-layout { display: flex; gap: 16px; overflow: hidden; flex: 1; }
        
        /* 输入区域优化：高度调低 */
        .inputs-area { flex: 0 0 280px; overflow-y: auto; padding-right: 8px; }
        .field { margin-bottom: 10px; }
        label { 
            display: block; font-size: 12px; color: #666 !important; 
            margin-bottom: 4px; font-weight: 500; 
        }
        
        /* 修复输入框：强制背景色和文字色 */
        textarea.var-input { 
            width: 100%; padding: 8px 10px; 
            border: 1px solid #dcdfe6 !important; 
            border-radius: 6px; 
            box-sizing: border-box; 
            font-size: 13px !important; 
            font-family: inherit;
            resize: vertical; 
            min-height: 45px; /* 调低初始高度 */
            max-height: 120px;
            transition: all 0.2s;
            background-color: #ffffff !important; /* 强制白色背景 */
            color: #333333 !important;           /* 强制深色文字 */
            outline: none;
        }
        textarea.var-input:focus { 
            border-color: #007aff !important; 
            box-shadow: 0 0 0 3px rgba(0,122,255,0.1); 
        }
        textarea.var-input::placeholder { color: #bbb !important; }

        /* 预览区域 */
        .preview-area { 
            flex: 1; background: #f8f9fa !important; padding: 14px; border-radius: 10px; 
            font-size: 13px; color: #444 !important; white-space: pre-wrap; 
            border: 1px solid #eee !important;
            overflow-y: auto; line-height: 1.5;
        }
        .preview-title { font-size: 11px; color: #999; margin-bottom: 6px; font-weight: bold; }
        
        .footer { margin-top: 16px; display: flex; gap: 10px; }
        button { 
            flex: 1; padding: 10px; border-radius: 8px; cursor: pointer; 
            border: none; font-size: 14px; font-weight: 600; transition: opacity 0.2s; 
        }
        .btn-confirm { background: #007aff !important; color: white !important; }
        .btn-confirm:hover { opacity: 0.9; }
        .btn-cancel { background: #f2f2f7 !important; color: #666 !important; }
        .btn-cancel:hover { background: #e5e5ea !important; }

        /* 滚动条美化 */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #ddd; border-radius: 10px; }
    `;

    container.innerHTML = `
        <div class="modal-card">
            <div class="header">填充变量</div>
            <div class="content-layout">
                <div class="inputs-area">
                    ${variables.map(v => `
                        <div class="field">
                            <label>${v.replace(/[{}]/g, '')}</label>
                            <textarea class="var-input" data-var="${v}" placeholder="请输入内容..."></textarea>
                        </div>
                    `).join('')}
                </div>
                <div class="preview-area">
                    <div class="preview-title">最终提示词预览 (长内容已折叠)</div>
                    <div id="preview-text"></div>
                </div>
            </div>
            <div class="footer">
                <button class="btn-cancel">取消</button>
                <button class="btn-confirm">确认注入</button>
            </div>
        </div>
    `;

    shadow.appendChild(style);
    shadow.appendChild(container);

    const previewEl = shadow.getElementById('preview-text');
    const inputs = shadow.querySelectorAll('.var-input');

    const updatePreview = () => {
        previewEl.innerHTML = getPreviewText(template, inputs);
    };

    inputs.forEach(input => input.oninput = updatePreview);
    updatePreview(); 

    shadow.querySelector('.btn-confirm').onclick = () => {
        let finalText = template;
        inputs.forEach(input => {
            finalText = finalText.replaceAll(input.dataset.var, input.value || "");
        });
        onConfirm(finalText);
        host.remove();
    };

    shadow.querySelector('.btn-cancel').onclick = () => host.remove();
}