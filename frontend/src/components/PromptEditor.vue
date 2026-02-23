<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <header class="modal-header">
        <h2>{{ isEdit ? '编辑提示词' : '新建提示词' }}</h2>
        <button class="close-icon" @click="$emit('close')">&times;</button>
      </header>
      
      <main class="modal-body">
        <div class="form-item">
          <label>标题</label>
          <input v-model="form.title" placeholder="输入提示词标题..." />
        </div>
        <div class="form-item">
          <label>描述 (可选)</label>
          <input v-model="form.description" placeholder="简单说明用途..." />
        </div>
        <div class="form-item">
          <label>所属类别</label>
          <select v-model="form.category_id" class="category-select">
            <option v-if="!form.category_id" :value="null" disabled>请选择分类...</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>
        <div class="form-item">
          <label>内容</label>
          <textarea v-model="form.content" rows="6" placeholder="输入提示词主体内容...
例：以下是当前代码：{{code}}
当前主要问题：{{problem}}
重构目标：{{goal}}
请给出：
1. 是否有必要重构（明确判断）
2. 推荐的重构方向
3. 分步骤重构建议（避免一次性推翻）
4. 重构后的预期收益
不要建议“全部重写”。"></textarea>
          <p class="hint" v-if="isEdit">* 修改内容将自动生成新的版本号</p>
        </div>
      </main>

      <footer class="modal-footer">
        <button class="btn-secondary" @click="$emit('close')">取消</button>
        <button class="btn-primary" :disabled="loading" @click="handleSave">
          {{ loading ? '保存中...' : '提交保存' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
// 1. 导入分类 API 服务
import { categoryService } from '@/api/categoryService';

const props = defineProps({
  categories: { type: Array, default: () => [] },
  initialData: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['close', 'save']);

// 2. 定义存放分类列表的变量
const categories = ref([]);

const form = reactive({
  title: props.initialData.title || '',
  description: props.initialData.description || '',
  content: props.initialData.content || '',
  // 确保 category_id 被正确初始化
  category_id: props.initialData.category_id || null
});

// 3. 挂载时加载分类列表
onMounted(async () => {
  try {
    // 假设 list 接口返回所有可用分类
    const res = await categoryService.list(1, 100); 
    categories.value = res;
    // 自动定位：如果是新建模式且没指定分类，自动匹配列表中名为“未分类”的 ID
    if (!props.isEdit && !form.category_id) {
      const defaultCat = res.find(c => c.name === '未分类');
      if (defaultCat) form.category_id = defaultCat.id;
    }
  } catch (err) {
    console.error('加载分类失败:', err);
  }
});

const handleSave = () => {
  if (!form.title || !form.content) return alert('标题和内容不能为空');
  // 此时 form 里已经包含了最新的 category_id
  emit('save', { ...form });
};
</script>

<style scoped>
.category-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  background-color: #fff;
  cursor: pointer;
  outline: none;
}

.category-select:focus {
  border-color: #007aff;
}
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
  padding: 20px;
}
.modal-content {
  background: #fff;
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  overflow: hidden;
}
.modal-header { padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.modal-header h2 { margin: 0; font-size: 16px; }
.modal-body { padding: 15px; }
.form-item { margin-bottom: 15px; }
.form-item label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 5px; color: #555; }
.form-item input, .form-item textarea {
  width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; box-sizing: border-box;
}
.hint { font-size: 11px; color: #f57c00; margin-top: 5px; }
.modal-footer { padding: 15px; background: #f9f9f9; text-align: right; }
.btn-primary { background: #007aff; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; }
.btn-secondary { background: none; border: none; color: #666; margin-right: 10px; cursor: pointer; }
.close-icon { background: none; border: none; font-size: 24px; cursor: pointer; color: #999; }
</style>