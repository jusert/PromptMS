/**
 * 创建模态框 HTML
 */
export const createModalHTML = (variables) => `
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