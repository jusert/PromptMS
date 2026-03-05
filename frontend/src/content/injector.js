/**
 * 格式化预览文本
 */
const formatValuePreview = (text) => {
    if (!text) return "";
    return text.length > 50 ? `${text.slice(0, 20)}...${text.slice(-20)}` : text;
};

/**
 * 获取实时预览 HTML
 */
export const getPreviewHTML = (template, inputEls) => {
    let preview = template;
    inputEls.forEach(input => {
        const varPlaceholder = input.dataset.var;
        const rawValue = input.value;
        
        const displayValue = rawValue 
            ? `<span style="color: #007aff; font-weight: 500;">${formatValuePreview(rawValue)}</span>`
            : `<span style="color: #999;">[等待输入 ${varPlaceholder}]</span>`;
        
        preview = preview.replaceAll(varPlaceholder, displayValue);
    });
    return preview;
};

/**
 * 获取最终生成的纯文本
 */
export const generateFinalText = (template, inputEls) => {
    let finalText = template;
    inputEls.forEach(input => {
        finalText = finalText.replaceAll(input.dataset.var, input.value || "");
    });
    return finalText;
};