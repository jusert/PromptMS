import { MODAL_STYLES } from './styles';
import { createModalHTML } from './template';
import { getAdapter } from './adapters.js'; 
import { getPreviewHTML, generateFinalText } from './injector';

/**
 * 渲染变量填充模态框 (Shadow DOM)
 * @param {string} template - 包含 {{var}} 的提示词模板
 * @param {Array} variables - 从模板中提取出的变量名数组
 * @param {Function} onConfirm - 用户点击确认后的回调函数，参数为填充后的最终文本
 */
function renderVariablePanel(template, variables, onConfirm) {
    // 1. 如果页面已存在模态框，先移除旧的，防止重复渲染
    document.getElementById('prompt-ms-variable-host')?.remove();

    // 2. 创建 Shadow Host 宿主元素
    const host = document.createElement('div');
    host.id = 'prompt-ms-variable-host';
    
    // 3. 使用 Shadow DOM (Open 模式)
    // 作用：完全隔离宿主页面的 CSS，防止 AI 网站的原生样式（如 Tailwind/Bootstrap）破坏插件 UI
    const shadow = host.attachShadow({ mode: 'open' });
    document.body.appendChild(host);

    // 4. 注入样式
    const style = document.createElement('style');
    style.textContent = MODAL_STYLES;
    
    // 5. 注入 HTML 结构
    const container = document.createElement('div');
    container.className = 'modal-overlay';
    container.innerHTML = createModalHTML(variables);

    shadow.appendChild(style);
    shadow.appendChild(container);

    // 6. 获取 DOM 引用 (注意：需在 shadow 根节点下查询)
    const previewEl = shadow.getElementById('preview-text');
    const inputs = Array.from(shadow.querySelectorAll('.var-input'));

    /**
     * 更新预览区域的内容
     * 监听每个 input 的输入变化，实时合成带有高亮样式的预览文本
     */
    const updatePreview = () => {
        previewEl.innerHTML = getPreviewHTML(template, inputs);
    };

    // 绑定输入事件：实现实时动态预览
    inputs.forEach(input => input.oninput = updatePreview);
    updatePreview(); // 初始化显示一次

    // 7. 绑定按钮逻辑
    // 确认注入按钮
    shadow.querySelector('.btn-confirm').onclick = () => {
        // 调用 injector 生成不带 HTML 标签的纯文本，并执行回调
        onConfirm(generateFinalText(template, inputs));
        // 任务完成后移除弹窗
        host.remove();
    };

    // 取消按钮
    shadow.querySelector('.btn-cancel').onclick = () => host.remove();
}

/**
 * 监听来自 background.js 或 SidePanel.vue 的消息
 * action: "INJECT_PROMPT" - 注入提示词指令
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "INJECT_PROMPT") {
        const { content } = request;
        
        // 1. 获取当前页面对应的适配器 (确定输入框的选择器和注入方式)
        const adapter = getAdapter();
        const inputEl = document.querySelector(adapter.inputSelector);

        // 2. 健壮性检查：如果页面结构变了找不到输入框，通知前端
        if (!inputEl) {
            sendResponse({ status: "error", message: "未找到输入框，请检查页面或尝试刷新" });
            return;
        }

        // 3. 变量识别逻辑
        // 正则解释：匹配 {{ 任意字符 }}，g 代表全局匹配
        const varRegex = /\{\{(.+?)\}\}/g;
        // 提取所有变量并去重（Set），例如 {{code}} {{code}} 只会出现一个输入框
        const variables = [...new Set(content.match(varRegex) || [])];

        // 4. 根据是否有变量采取不同策略
        if (variables.length > 0) {
            // 有变量：弹出 Shadow DOM 面板让用户填写
            renderVariablePanel(content, variables, (finalText) => {
                // 用户点击确定后，通过适配器将最终文本注入到 AI 网站的输入框中
                adapter.inject(inputEl, finalText);
            });
        } else {
            // 无变量：直接通过适配器注入原始文本
            adapter.inject(inputEl, content);
        }

        // 5. 异步响应，告知发送方消息已收到并开始处理
        sendResponse({ status: "success" });
    }
    
    // 返回 true 以支持异步 sendResponse
    return true;
});