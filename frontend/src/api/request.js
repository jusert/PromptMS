import axios from 'axios';
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8787/';
const apiClient = axios.create({
  // 替换为你的后端实际地址
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
});

// 响应拦截器：统一处理错误提示
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const msg = error.response?.data?.detail || '服务器开小差了';
    console.error('API Error:', msg);
    return Promise.reject(msg);
  }
);

export default apiClient;