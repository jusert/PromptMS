<template>
  <nav class="breadcrumb-container">
    <div 
      v-for="(item, index) in items" 
      :key="index"
      class="breadcrumb-item"
    >
      <span 
        :class="['breadcrumb-label', { 'is-last': index === items.length - 1 }]"
        @click="$emit('navigate', item)"
      >
        {{ item.name }}
      </span>
      <span v-if="index < items.length - 1" class="separator">/</span>
    </div>
  </nav>
</template>

<script setup>
defineProps({
  items: { type: Array, required: true } // 格式: [{id: 1, name: '分类A'}, ...]
});
defineEmits(['navigate']);
</script>

<style scoped>
.breadcrumb-container {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  padding: 8px 0;
  font-size: 13px;
}
.breadcrumb-item {
  display: flex;
  align-items: center;
}
.breadcrumb-label {
  color: #007aff;
  cursor: pointer;
}
.breadcrumb-label:hover {
  text-decoration: underline;
}
.breadcrumb-label.is-last {
  color: #666;
  cursor: default;
  text-decoration: none;
}
.separator {
  margin: 0 6px;
  color: #ccc;
}
</style>