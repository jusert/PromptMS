<template>
  <div class="category-item" @click="$emit('select', category)" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="icon-box">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="#FFCA28">
        <path d="M10 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2h-8l-2-2z"/>
      </svg>
    </div>
    <div class="category-info">
      <span class="category-name">{{ category.name }}</span>
    </div>
    
    <div class="actions" v-if="isHover && !isSystemCategory">
      <button class="mini-btn edit" @click.stop="$emit('edit', category)">编辑</button>
      <button class="mini-btn delete" @click.stop="$emit('delete', category.id)">删除</button>
    </div>
    <div v-else class="arrow">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="#ccc">
        <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({ 
  category: { type: Object, required: true } 
});
defineEmits(['select', 'edit', 'delete']);

const isHover = ref(false);

// 核心逻辑：定义哪些文件夹不能被动
const isSystemCategory = computed(() => {
  // 建议通过 ID 判断（更准确），比如未分类 ID 通常是 0 
  // 或者通过名称判断
  return props.category.id === 0 || props.category.name === '未分类';
});
</script>

<style scoped>
.category-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #fff;
  border: 1px solid #efefef;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.category-item:hover {
  background: #f9f9f9;
  border-color: #dcdcdc;
}
.icon-box { margin-right: 12px; display: flex; align-items: center; }
.category-info { flex: 1; }
.category-name { font-size: 14px; font-weight: 500; color: #333; }
.actions { display: flex; gap: 4px; }
.mini-btn { font-size: 11px; padding: 2px 6px; border-radius: 4px; border: 1px solid #ddd; background: #fff; cursor: pointer; color: #666; }
.mini-btn:hover { background: #f0f0f0; }
.mini-btn.delete:hover { background: #f56c6c; color: white; border-color: #f56c6c; }
</style>