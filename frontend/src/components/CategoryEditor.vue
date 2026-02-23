<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <header class="modal-header">
        <h2>{{ isEdit ? '编辑文件夹' : '新建文件夹' }}</h2>
        <button class="close-icon" @click="$emit('close')">&times;</button>
      </header>
      
      <main class="modal-body">
        <div class="form-item">
          <label>文件夹名称</label>
          <input v-model="form.name" placeholder="请输入文件夹名称..." @keyup.enter="handleSave" />
        </div>
      </main>

      <footer class="modal-footer">
        <button class="btn-secondary" @click="$emit('close')">取消</button>
        <button class="btn-primary" :disabled="loading" @click="handleSave">
          {{ loading ? '保存中...' : '确定' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const props = defineProps({
  initialData: { type: Object, default: () => ({ name: '' }) },
  isEdit: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['close', 'save']);

const form = reactive({
  name: props.initialData.name || ''
});

const handleSave = () => {
  if (!form.name.trim()) return alert('名称不能为空');
  emit('save', { ...form });
};
</script>

<style scoped>
/* 样式复用 PromptEditor 的即可，建议提取公共 CSS */
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: #fff; width: 320px; border-radius: 12px; overflow: hidden; }
.modal-header { padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.modal-header h2 { margin: 0; font-size: 16px; }
.modal-body { padding: 15px; }
.form-item label { display: block; font-size: 13px; margin-bottom: 5px; color: #666; }
.form-item input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
.modal-footer { padding: 12px; background: #f9f9f9; text-align: right; }
.btn-primary { background: #007aff; color: #fff; border: none; padding: 6px 16px; border-radius: 6px; cursor: pointer; }
.btn-secondary { background: none; border: none; color: #666; margin-right: 8px; cursor: pointer; }
.close-icon { background: none; border: none; font-size: 20px; cursor: pointer; color: #999; }
</style>