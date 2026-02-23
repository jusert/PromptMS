import apiClient from './request';

export const promptService = {
  // 创建提示词
  create(data) {
    return apiClient.post('/prompts', data);
  },

  // 删除提示词
  delete(id) {
    return apiClient.delete(`/prompts/${id}`);
  },

  // 更新内容（生成新版本）
  update(id, data) {
    return apiClient.put(`/prompts/${id}`, data);
  },

  // 获取列表
  list(params = { page: 1, size: 10, category_id: null }) {
    return apiClient.get('/prompts', { params });
  },

  // 回滚版本
  rollback(id, version) {
    return apiClient.post(`/prompts/${id}/rollback/${version}`);
  },

  //   // 获取详情
  // getDetail(id) {
  //   return apiClient.get(`/prompts/${id}`);
  // },

  // // 获取历史版本列表
  // getHistory(id) {
  //   return apiClient.get(`/prompts/${id}/versions`);
  // }
};