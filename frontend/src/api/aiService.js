import { API_BASE_URL } from './request';

export const aiService = {
  async optimizeStream(prompt, onChunk) {
    // 自动移除末尾斜杠以防拼接出双斜杠 //
    const baseUrl = API_BASE_URL.replace(/\/$/, '');
    
    const response = await fetch(`${baseUrl}/ai/optimize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'AI 优化请求失败');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      if (onChunk) onChunk(chunk);
    }
  }
};