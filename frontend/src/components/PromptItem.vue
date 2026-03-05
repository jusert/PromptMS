<template>
  <div class="prompt-item" @mouseenter="isHover = true" @mouseleave="isHover = false">
    <div class="item-header">
      <div class="title-wrapper">
        <h3 class="title" :title="prompt.title">{{ prompt.title }}</h3>
        <span class="version">v{{ prompt.current_version }}</span>
      </div>
      <div class="quick-actions" :class="{ visible: isHover }">
        <button class="mini-btn" @click.stop="$emit('edit', prompt)" title="编辑">编辑</button>
        <button class="mini-btn copy" @click.stop="handleCopy" title="复制内容">复制</button>
      </div>
    </div>

    <p v-if="prompt.description" class="desc">{{ prompt.description }}</p>

    <div class="preview-box">
      {{ prompt.content }}
    </div>

    <div class="item-footer">
      <span class="time">{{ prompt.updated_at}}</span>
      <div class="danger-actions" v-if="isHover">
        <button class="mini-btn rollback" @click.stop="handleRollback">回滚</button>
        <button class="mini-btn delete" @click.stop="$emit('delete', prompt.id)">删除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { SUPPORTED_DOMAINS } from '@/config/domains';

const props = defineProps({
  prompt: { type: Object, required: true }
});
console.log(props.prompt);
// 定义组件向外抛出的事件
const emit = defineEmits(['edit', 'delete', 'rollback']);
const isHover = ref(false);
// 修改 PromptItem.vue 中的 handleCopy 函数
const handleCopy = async () => {
try {
    // 获取当前窗口的活跃标签页
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const tab = tabs[0];
    const isSupported = SUPPORTED_DOMAINS.some(domain => tab?.url?.includes(domain));

    if (!isSupported) {
      alert("请在支持的 AI 页面（Gemini, ChatGPT, Qwen, DeepSeek...）使用此功能");
      return;
    }

    // 2. 发送消息给 content.js
    chrome.tabs.sendMessage(tab.id, {
      action: "INJECT_PROMPT",
      content: props.prompt.content
    }, (response) => {
      if (chrome.runtime.lastError) {
        alert("页面未准备好，请刷新本页面后再试");
      }
    });
  } catch (err) {
    console.error("MVP 注入失败", err);
  }
};

// 回滚通过弹窗获取版本号后，将 ID 和 版本号 发射给父组件
const handleRollback = () => {
  const version = prompt('请输入要回滚到的版本号 (当前 v' + props.prompt.current_version + ')');
  if (version && version.trim()) {
    emit('rollback', { id: props.prompt.id, version: version.trim() });
  }
};

</script>

<style scoped>
/* 样式保持不变 */
.prompt-item { background: #ffffff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 10px; margin-bottom: 8px; transition: all 0.2s ease; cursor: default; }
.prompt-item:hover { border-color: #007aff; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.item-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px; }
.title-wrapper { display: flex; align-items: center; gap: 6px; overflow: hidden; }
.title { font-size: 14px; font-weight: 600; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #333; }
.version { font-size: 10px; background: #f0f0f0; color: #888; padding: 0 4px; border-radius: 3px; flex-shrink: 0; }
.desc { font-size: 12px; color: #999; margin: 0 0 6px 0; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; }
.preview-box { background: #f9f9f9; border-radius: 4px; padding: 6px 8px; font-size: 12px; line-height: 1.4; color: #666; max-height: 40px; display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; }
.item-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; min-height: 20px; }
.time { font-size: 11px; color: #bbb; }
.quick-actions, .danger-actions { display: flex; gap: 4px; opacity: 0; transition: opacity 0.2s; }
.visible, .prompt-item:hover .quick-actions, .prompt-item:hover .danger-actions { opacity: 1; }
.icon-btn { padding: 2px 6px; font-size: 11px; border: 1px solid #dcdfe6; background: #fff; border-radius: 4px; cursor: pointer; }
.icon-btn.copy { background: #007aff; color: white; border-color: #007aff; }
.text-btn { background: none; border: none; font-size: 11px; cursor: pointer; padding: 0 4px; }
.text-btn.rollback { color: #67c23a; }
.text-btn.delete { color: #f56c6c; }
.icon-btn:hover, .text-btn:hover { opacity: 0.7; }

.mini-btn { font-size: 11px; padding: 2px 6px; border-radius: 4px; border: 1px solid #ddd; background: #fff; cursor: pointer; color: #666; }
.mini-btn:hover { background: #f0f0f0; }
.mini-btn.copy:hover { background:#007aff; color: white; border-color: #007aff; }
.mini-btn.rollback:hover { background:#67c23a; color: white; border-color: #67c23a; }
.mini-btn.delete:hover { background: #f56c6c; color: white; border-color: #f56c6c; }
</style>