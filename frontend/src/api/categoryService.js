import apiClient from './request';

export const categoryService = {
  // 创建分类
  create(data) {
    return apiClient.post('/categories', data);
  },

  // 删除分类
  delete(id) {
    return apiClient.delete(`/categories/${id}`);
  },

  // 更新内容（生成新版本）
  update(id, data) {
    return apiClient.put(`/categories/${id}`, data);
  },

  // 获取全部分类（分页）
  list(page = 1, limit = 10) {
    return apiClient.get('/categories', { params: { page, limit } });
  },

  // 获取分类详情（钻取查询：含子分类和提示词）
  getDetail(id, page = 1, size = 10) {
    return apiClient.get(`/categories/${id}`, { params: { page, size } });
  }
};