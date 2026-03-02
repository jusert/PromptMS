<template>
  <div class="side-panel">
    <header class="panel-header">
      <div class="header-top">
        <div class="view-tabs">
          <button :class="['tab-btn', viewMode === 'list' ? 'active' : '']" @click="toggleView('list')">列表</button>
          <button :class="['tab-btn', viewMode === 'category' ? 'active' : '']" @click="toggleView('category')">文件夹</button>
        </div>
        
        <button class="icon-btn settings-trigger" @click="showSettings = true" title="模型设置">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </button>
      </div>

      <Breadcrumb 
        v-if="viewMode === 'category'"
        :items="breadcrumbs" 
        @navigate="(item) => loadCategoryContent(item.id, item.name)" 
        class="compact-breadcrumb"
      />
    </header>

    <main class="panel-body">
      <div v-if="loading" class="state-msg">数据传输中...</div>
      
      <template v-else>
        <div v-if="viewMode === 'category'">
          <div v-if="categoryData.sub_categories.length > 0" class="group">
            <label class="group-label">文件夹</label>
            <CategoryItem 
              v-for="cat in categoryData.sub_categories" 
              :key="cat.id" 
              :category="cat"
              @edit="openEditCategory"
              @delete="handleDeleteCategory"
              @select="(c) => loadCategoryContent(c.id, c.name)"
            />
          </div>

          <div v-if="categoryData.prompts.length > 0" class="group">
            <label class="group-label">提示词</label>
            <PromptItem 
              v-for="p in categoryData.prompts" 
              :key="p.id" 
              :prompt="p"
              @edit="openEditPrompt"
              @delete="handleDeletePrompt"
              @rollback="handleRollbackPrompt"
            />
          </div>
        </div>

        <div v-else class="group">
          <label class="group-label">全部提示词 ({{ allPrompts.length }})</label>
          <PromptItem 
            v-for="p in allPrompts" 
            :key="'list-' + p.id" 
            :prompt="p"
            @edit="openEditPrompt"
            @delete="handleDeletePrompt"
            @rollback="handleRollbackPrompt"
          />
        </div>

        <div v-if="isEmpty" class="state-msg">此分类下暂无内容</div>
      </template>
    </main>

    <footer class="panel-footer">
      <div class="header-actions">
        <button class="action-btn-text primary flex-1" @click="openCreatePrompt">
          <span class="plus">+</span> 提示词
        </button>
        <button class="action-btn-text secondary" @click="openCreateCategory" title="新建文件夹">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="#FFCA28">
            <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
          </svg>
          文件夹
        </button>
      </div>
    </footer>

    <PromptEditor 
      v-if="showPromptEditor"
      :is-edit="promptEditorConfig.isEdit"
      :initial-data="promptEditorConfig.initialData"
      :categories="allCategories"
      :loading="promptEditorConfig.loading"
      @close="showPromptEditor = false"
      @save="handleSavePrompt"
    />

    <CategoryEditor 
      v-if="showCategoryEditor"
      :is-edit="categoryEditorConfig.isEdit"
      :initial-data="categoryEditorConfig.initialData"
      :loading="categoryEditorConfig.loading"
      @close="showCategoryEditor = false"
      @save="handleSaveCategory"
    />

    <SettingsView v-if="showSettings" @close="showSettings = false" />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { categoryService } from '@/api/categoryService';
import { promptService } from '@/api/promptService';

import Breadcrumb from './components/Breadcrumb.vue';
import CategoryItem from './components/CategoryItem.vue';
import CategoryEditor from './components/CategoryEditor.vue';
import PromptItem from './components/PromptItem.vue';
import PromptEditor from './components/PromptEditor.vue';
import SettingsView from './components/SettingsView.vue';

// --- 状态管理 ---
const loading = ref(false);
const viewMode = ref('list'); 
const currentCategoryId = ref(null);
const categoryData = ref({ sub_categories: [], prompts: [], name: '根目录' });
const allPrompts = ref([]); 
const allCategories = ref([]); 
const breadcrumbs = ref([{ id: null, name: '全部' }]);

const showCategoryEditor = ref(false);
const categoryEditorConfig = reactive({ isEdit: false, initialData: {}, loading: false });
const showPromptEditor = ref(false);
const promptEditorConfig = reactive({ isEdit: false, initialData: {}, loading: false });
const showSettings = ref(false);

// --- API 交互逻辑 ---
const fetchCategories = async () => {
  try { allCategories.value = await categoryService.list(1, 100); } catch (err) { console.error('获取分类失败'); }
};

const loadCategoryContent = async (id, name = '根目录') => {
  loading.value = true;
  try {
    if (id === null) {
      const res = await categoryService.list(1, 50);
      categoryData.value = { sub_categories: res, prompts: [], name: '根目录' };
      breadcrumbs.value = [{ id: null, name: '全部' }];
    } else {
      categoryData.value = await categoryService.getDetail(id);
      updateBreadcrumbs(id, name);
    }
    currentCategoryId.value = id;
  } finally { loading.value = false; }
};

const loadAllPrompts = async () => {
  loading.value = true;
  try { allPrompts.value = await promptService.list({ page: 1, size: 100 }); } finally { loading.value = false; }
};

const handleDeletePrompt = async (id) => {
  if (!confirm('确定要删除此提示词吗？')) return;
  try { await promptService.delete(id); refreshData(); } catch (err) { alert('删除失败: ' + err); }
};

const handleDeleteCategory = async (id) => {
  const cat = categoryData.value.sub_categories.find(c => c.id === id);
  if (cat && (cat.id === 0 || cat.name === '未分类')) return alert('系统默认文件夹不能删除');
  if (!confirm('确定删除文件夹吗？')) return;
  try { await categoryService.delete(id); refreshData(); } catch (err) { alert('删除失败: ' + err); }
};

const handleRollbackPrompt = async ({ id, version }) => {
  try { await promptService.rollback(id, version); refreshData(); alert('已回滚至 v' + version); } catch (err) { alert('回滚失败: ' + err); }
};

const handleSavePrompt = async (formData) => {
  promptEditorConfig.loading = true;
  try {
    if (promptEditorConfig.isEdit) await promptService.update(promptEditorConfig.initialData.id, formData);
    else await promptService.create(formData);
    showPromptEditor.value = false;
    refreshData();
  } catch (err) { alert('操作失败: ' + err); } finally { promptEditorConfig.loading = false; }
};

const handleSaveCategory = async (formData) => {
  categoryEditorConfig.loading = true;
  try {
    if (categoryEditorConfig.isEdit) await categoryService.update(categoryEditorConfig.initialData.id, formData);
    else await categoryService.create(formData);
    showCategoryEditor.value = false;
    refreshData();
  } catch (err) { alert('操作失败: ' + err); } finally { categoryEditorConfig.loading = false; }
};

// --- 辅助逻辑 ---
const refreshData = () => {
  fetchCategories();
  viewMode.value === 'list' ? loadAllPrompts() : loadCategoryContent(currentCategoryId.value);
};

const toggleView = (mode) => {
  viewMode.value = mode;
  refreshData();
};

const openCreatePrompt = () => {
  promptEditorConfig.isEdit = false;
  promptEditorConfig.initialData = { category_id: currentCategoryId.value };
  showPromptEditor.value = true;
};

const openCreateCategory = () => {
  categoryEditorConfig.isEdit = false;
  categoryEditorConfig.initialData = { name: '' };
  showCategoryEditor.value = true;
};

const openEditPrompt = (prompt) => {
  promptEditorConfig.isEdit = true;
  promptEditorConfig.initialData = { ...prompt };
  showPromptEditor.value = true;
};

const openEditCategory = (category) => {
  if (category.id === 0 || category.name === '未分类') return alert('系统默认文件夹不能编辑');
  categoryEditorConfig.isEdit = true;
  categoryEditorConfig.initialData = { ...category };
  showCategoryEditor.value = true;
};

const updateBreadcrumbs = (id, name) => {
  const index = breadcrumbs.value.findIndex(b => b.id === id);
  if (index !== -1) breadcrumbs.value = breadcrumbs.value.slice(0, index + 1);
  else breadcrumbs.value.push({ id, name });
};

const isEmpty = computed(() => {
  return viewMode.value === 'category' 
    ? (categoryData.value.sub_categories.length === 0 && categoryData.value.prompts.length === 0)
    : allPrompts.value.length === 0;
});

onMounted(() => {
  loadAllPrompts();
  loadCategoryContent(null);
  fetchCategories();
});
</script>

<style scoped>
.side-panel {
  display: flex; flex-direction: column; width: 100%; height: 100vh;
  background-color: #f6f6f8; color: #333;
}

/* 头部修改：移除 actions 的间距 */
.panel-header {
  background: #fff; padding: 10px 14px; border-bottom: 1px solid #e0e0e0;
  z-index: 10;
}

.header-top {
  display: flex; justify-content: space-between; align-items: center;
}

/* 底部操作区 */
.panel-footer {
  background: #fff;
  padding: 12px 14px;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.03);
}

.header-actions {
  display: flex; gap: 8px;
}

/* 其余样式保持一致 */
.view-tabs { display: flex; background: #f0f0f2; padding: 2px; border-radius: 8px; }
.tab-btn {
  padding: 4px 12px; font-size: 11px; border: none; background: transparent;
  cursor: pointer; border-radius: 6px; color: #777; transition: all 0.2s;
}
.tab-btn.active {
  background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.08); color: #007aff; font-weight: 600;
}

.icon-btn {
  background: none; border: none; color: #999; cursor: pointer;
  padding: 4px; border-radius: 50%; display: flex; align-items: center;
}
.icon-btn:hover { background: #f0f0f0; color: #007aff; }

.action-btn-text {
  display: flex; align-items: center; justify-content: center; height: 32px;
  border-radius: 8px; font-size: 12px; font-weight: 600;
  cursor: pointer; border: 1px solid transparent; transition: all 0.2s;
}
.flex-1 { flex: 1; }
.action-btn-text.primary { background: #007aff; color: white; }
.action-btn-text.secondary { background: #fff; color: #555; border-color: #ddd; padding: 0 12px; }
.action-btn-text:active { transform: scale(0.98); opacity: 0.9; }

.compact-breadcrumb { margin-top: 8px; padding-top: 8px; border-top: 1px dashed #f0f0f0; }

.panel-body { flex: 1; overflow-y: auto; padding: 12px 14px; }
.group { margin-bottom: 16px; }
.group-label {
  display: block; font-size: 10px; font-weight: 700; color: #bbb;
  text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.8px;
}
.state-msg { text-align: center; padding: 60px 0; color: #bbb; font-size: 12px; }
.plus { margin-right: 4px; font-size: 14px; }
</style>