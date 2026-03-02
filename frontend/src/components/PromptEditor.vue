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
          <input class="compact-input" v-model="form.title" placeholder="输入提示词标题..." />
        </div>
        
        <div class="form-row">
          <div class="form-item flex-1">
            <label>描述 (可选)</label>
            <input class="compact-input small-text" v-model="form.description" placeholder="用途说明..." />
          </div>
          <div class="form-item category-item">
            <label>类别</label>
            <select v-model="form.category_id" class="category-select compact-input small-text">
              <option v-if="!form.category_id" :value="null" disabled>请选择...</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
        </div>

        <div class="form-item">
          <div class="content-header">
            <label>内容</label>
            <button 
              v-if="!showComparison"
              class="mini-btn ai-special" 
              :disabled="isOptimizing || !form.content" 
              @click="handleAIOptimize"
            >
              <span v-if="isOptimizing" class="loading-spinner"></span>
              {{ isOptimizing ? '优化中...' : ' AI 优化' }}
            </button>
          </div>

          <div class="textarea-container">
            <textarea 
              v-model="form.content" 
              rows="8" 
              :class="{'ai-loading': isOptimizing}"
              placeholder="输入提示词主体内容..."
              :disabled="showComparison"
            ></textarea>

            <div v-if="showComparison" class="comparison-overlay">
              <div class="comparison-header">
                <span class="small-text"> AI 建议</span>
                <div class="comp-actions">
                  <button class="mini-btn accept" @click="confirmOptimization">应用</button>
                  <button class="mini-btn cancel" @click="cancelOptimization">取消</button>
                </div>
              </div>
              <div class="comparison-body">
                <div class="diff-section">
                  <div class="diff-tag old">原内容</div>
                  <p class="diff-text">{{ originalContent }}</p>
                </div>
                <div class="diff-section">
                  <div class="diff-tag new">优化后</div>
                  <p class="diff-text highlight">{{ optimizedContent }}</p>
                </div>
              </div>
            </div>
          </div>
          <p class="hint" v-if="isEdit">* 修改内容将生成新版本</p>
        </div>
      </main>

      <footer class="modal-footer">
        <button class="btn-secondary" @click="$emit('close')">取消</button>
        <button class="btn-primary" :disabled="loading || isOptimizing || showComparison" @click="handleSave">
          {{ loading ? '保存中...' : '提交保存' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { categoryService } from '@/api/categoryService';
import { aiService } from '@/api/aiService';

const props = defineProps({
  categories: { type: Array, default: () => [] },
  initialData: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['close', 'save']);

const categories = ref([]);
const isOptimizing = ref(false); 
const showComparison = ref(false);
const originalContent = ref('');
const optimizedContent = ref('');

const form = reactive({
  title: props.initialData.title || '',
  description: props.initialData.description || '',
  content: props.initialData.content || '',
  category_id: props.initialData.category_id || null
});

onMounted(async () => {
  try {
    const res = await categoryService.list(1, 100); 
    categories.value = res;
    if (!props.isEdit && !form.category_id) {
      const defaultCat = res.find(c => c.name === '未分类');
      if (defaultCat) form.category_id = defaultCat.id;
    }
  } catch (err) {
    console.error('加载失败:', err);
  }
});

const handleAIOptimize = async () => {
  if (!form.content.trim()) return;
  originalContent.value = form.content;
  optimizedContent.value = "";
  isOptimizing.value = true;
  try {
    await aiService.optimizeStream(originalContent.value, (chunk) => {
      // 核心拦截逻辑
      if (chunk.startsWith("ERR_AUTH:")) {
        const errorMsg = chunk.replace("ERR_AUTH:", "");
        alert(errorMsg); // 提示用户
        
        // 自动回滚内容，防止错误信息留在 textarea 里
        form.content = originalContent.value;
        
        // 抛出异常以中断 aiService.optimizeStream 的后续执行
        throw new Error("AUTH_FAILED");
      }
      optimizedContent.value += chunk;
      form.content = optimizedContent.value;
    });
    showComparison.value = true;
  } catch (err) {
    if (err.message !== "AUTH_FAILED") {
      alert("优化失败: " + err);
    }
    form.content = originalContent.value;
  } finally {
    isOptimizing.value = false;
  }
};

const confirmOptimization = () => {
  form.content = optimizedContent.value;
  showComparison.value = false;
};

const cancelOptimization = () => {
  form.content = originalContent.value;
  showComparison.value = false;
};

const handleSave = () => {
  if (!form.title || !form.content) return alert('标题和内容不能为空');
  emit('save', { ...form });
};
</script>

<style scoped>
.mini-btn {
  font-size: 11px; padding: 2px 8px; border-radius: 4px;
  border: 1px solid #ddd; background: #fff; cursor: pointer; color: #666;
  display: flex; align-items: center; gap: 4px; transition: all 0.2s;
}
.mini-btn:hover { background: #f0f0f0; border-color: #ccc; }
.mini-btn.accept:hover { background:#67c23a; color: white; border-color: #67c23a; }
.mini-btn.cancel:hover { background: #f56c6c; color: white; border-color: #f56c6c; }
.ai-special { border-color: #007aff; color: #007aff; font-weight: 600; }
.ai-special:hover { background: #007aff; color: white; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: #fff; width: 320px; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }

.modal-header { padding: 10px 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.modal-header h2 { margin: 0; font-size: 16px; font-weight: 600; }

.modal-body { padding: 12px 15px; max-height: 70vh; overflow-y: auto; }
.form-row { display: flex; gap: 10px; }
.flex-1 { flex: 1; }
.category-item { width: 100px; }

.form-item { margin-bottom: 8px; }
.form-item label { display: block; font-size: 11px; font-weight: 600; margin-bottom: 3px; color: #888; }

.compact-input { 
  width: 100%; padding: 4px 8px; border: 1px solid #ddd; border-radius: 4px; 
  font-size: 13px; outline: none; box-sizing: border-box; 
}
.small-text { font-size: 12px; color: #666; }
.compact-input:focus { border-color: #007aff; }

.content-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.textarea-container { position: relative; }
textarea { 
  width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; 
  font-size: 13px; line-height: 1.4; resize: vertical; box-sizing: border-box; 
}

.comparison-overlay {
  position: absolute; inset: 0; background: #fff; border: 1px solid #007aff; 
  border-radius: 4px; display: flex; flex-direction: column; z-index: 10;
}
.comparison-header {
  padding: 4px 8px; background: #f0f7ff; border-bottom: 1px solid #d0e7ff;
  display: flex; justify-content: space-between; align-items: center;
}
.comp-actions { display: flex; gap: 6px; align-items: center; }
.comparison-body { flex: 1; padding: 8px; overflow-y: auto; font-size: 11px; }
.diff-section { margin-bottom: 8px; }
.diff-tag { font-size: 9px; padding: 1px 4px; border-radius: 3px; display: inline-block; margin-bottom: 2px; }
.diff-tag.old { background: #fee2e2; color: #b91c1c; }
.diff-tag.new { background: #dcfce7; color: #15803d; }
.diff-text { margin: 0; line-height: 1.4; color: #777; white-space: pre-wrap; }
.diff-text.highlight { color: #333; font-weight: 500; }

.ai-loading { border-color: #007aff; background-color: #f9fcff; }
.loading-spinner { width: 8px; height: 8px; border: 1.5px solid #007aff; border-top-color: transparent; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.hint { font-size: 10px; color: #f57c00; margin-top: 2px; }
.modal-footer { padding: 10px 15px; background: #fcfcfc; text-align: right; border-top: 1px solid #eee; }
.btn-primary { background: #007aff; color: #fff; border: none; padding: 5px 15px; border-radius: 4px; cursor: pointer; font-size: 12px; }
.btn-primary:disabled { background: #ccc; }
.btn-secondary { background: none; border: none; color: #999; margin-right: 8px; cursor: pointer; font-size: 12px; }
.close-icon { background: none; border: none; font-size: 20px; cursor: pointer; color: #ccc; }
</style>