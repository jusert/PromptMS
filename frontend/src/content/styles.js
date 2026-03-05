/**
 * 模态框样式
 */
export const MODAL_STYLES =  `
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