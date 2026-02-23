<template>
  <div class="side-panel">
    <header class="panel-header">
      <div class="header-top">
        <div class="view-tabs">
          <button :class="['tab-btn', viewMode === 'list' ? 'active' : '']" @click="toggleView('list')">列表</button>
          <button :class="['tab-btn', viewMode === 'category' ? 'active' : '']" @click="toggleView('category')">文件夹</button>
        </div>

        <div class="actions">
          <button class="action-btn-text primary" @click="openCreatePrompt">
            <span class="plus">+</span> 提示词
          </button>
          <button class="action-btn-text secondary" @click="openCreateCategory" title="新建文件夹">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="#FFCA28">
            <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
          </svg>
            文件夹
          </button>
        </div>

        <CategoryEditor 
          v-if="showCategoryEditor"
          :is-edit="categoryEditorConfig.isEdit"
          :initial-data="categoryEditorConfig.initialData"
          :loading="categoryEditorConfig.loading"
          @close="showCategoryEditor = false"
          @save="handleSaveCategory"
        />
      </div>

      <Breadcrumb 
        v-if="viewMode === 'category'"
        :items="breadcrumbs" 
        @navigate="(item) => loadCategoryContent(item.id, item.name)" 
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

    <PromptEditor 
      v-if="showPromptEditor"
      :is-edit="promptEditorConfig.isEdit"
      :initial-data="promptEditorConfig.initialData"
      :categories="allCategories"
      :loading="promptEditorConfig.loading"
      @close="showPromptEditor = false"
      @save="handleSavePrompt"
    />
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

// --- API 交互逻辑 ---
const fetchCategories = async () => {
  try {
    allCategories.value = await categoryService.list(1, 100);
  } catch (err) {
    console.error('获取分类列表失败');
  }
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
  } finally {
    loading.value = false;
  }
};

const loadAllPrompts = async () => {
  loading.value = true;
  try {
    allPrompts.value = await promptService.list({ page: 1, size: 100 });
  } finally {
    loading.value = false;
  }
};

const handleDeletePrompt = async (id) => {
  if (!confirm('确定要删除此提示词吗？此操作不可撤销。')) return;
  try {
    await promptService.delete(id);
    refreshData();
  } catch (err) {
    alert('删除失败: ' + err);
  }
};

const handleDeleteCategory = async (id) => {
  const cat = categoryData.value.sub_categories.find(c => c.id === id);
  if (cat && (cat.id === 0 || cat.name === '未分类')) {
    return alert('系统默认文件夹不能删除');
  }
  if (!confirm('确定删除文件夹吗？文件夹内的提示词可能变为未分类。')) return;
  try {
    await categoryService.delete(id);
    refreshData();
  } catch (err) {
    alert('删除失败: ' + err);
  }
};

const handleRollbackPrompt = async ({ id, version }) => {
  try {
    await promptService.rollback(id, version);
    refreshData();
    alert('已回滚至 v' + version);
  } catch (err) {
    alert('回滚失败: ' + err);
  }
};

const handleSavePrompt = async (formData) => {
  promptEditorConfig.loading = true;
  try {
    if (promptEditorConfig.isEdit) {
      await promptService.update(promptEditorConfig.initialData.id, formData);
    } else {
      await promptService.create(formData);
    }
    showPromptEditor.value = false;
    refreshData();
  } catch (err) {
    alert('操作失败: ' + err);
  } finally {
    promptEditorConfig.loading = false;
  }
};

const handleSaveCategory = async (formData) => {
  categoryEditorConfig.loading = true;
  try {
    if (categoryEditorConfig.isEdit) {
      await categoryService.update(categoryEditorConfig.initialData.id, formData);
    } else {
      await categoryService.create(formData);
    }
    showCategoryEditor.value = false;
    refreshData();
  } catch (err) {
    alert('操作失败: ' + err);
  } finally {
    categoryEditorConfig.loading = false;
  }
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
  if (category.id === 0 || category.name === '未分类') {
    return alert('系统默认文件夹不能编辑');
  }
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
:global(html), :global(body) {
  margin: 0; padding: 0; width: 100%; height: 100vh; overflow: hidden;
}

.side-panel {
  display: flex; flex-direction: column; width: 100%; height: 100vh;
  background-color: #f5f5f7;
}

.panel-header {
  background: #fff; padding: 12px 15px; border-bottom: 1px solid #e5e5e5;
  position: sticky; top: 0; z-index: 10;
}

.header-top {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
}

/* 视图切换 */
.view-tabs {
  display: flex; background: #eee; padding: 2px; border-radius: 6px;
}
.tab-btn {
  padding: 4px 10px; font-size: 11px; border: none; background: transparent;
  cursor: pointer; border-radius: 4px; color: #666;
}
.tab-btn.active {
  background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); color: #007aff; font-weight: 600;
}

/* 方案二：按钮布局样式 */
.actions {
  display: flex; gap: 8px;
}

.action-btn-text {
  display: flex; align-items: center; justify-content: center;
  padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 500;
  cursor: pointer; border: 1px solid transparent; transition: all 0.2s;
  white-space: nowrap;
}

.action-btn-text svg { margin-right: 4px; }
.action-btn-text .plus { font-size: 14px; margin-right: 4px; font-weight: bold; }

.action-btn-text.primary {
  background: #007aff; color: white;
}
.action-btn-text.primary:hover {
  background: #0063cc;
}

.action-btn-text.secondary {
  background: #fff; color: #555; border-color: #dcdcdc;
}
.action-btn-text.secondary:hover {
  background: #f9f9f9; border-color: #ccc;
}

.panel-body {
  flex: 1; overflow-y: auto; padding: 10px 15px;
}

.group { margin-bottom: 20px; }
.group-label {
  display: block; font-size: 11px; font-weight: 700; color: #999;
  text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;
}

.state-msg {
  text-align: center; padding: 40px 0; color: #999; font-size: 13px;
}
</style>