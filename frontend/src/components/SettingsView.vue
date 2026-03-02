<template>
  <div class="settings-overlay">
    <div class="settings-content">
      <header class="settings-header">
        <h3>API 设置</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </header>

      <main class="settings-body">
        <section class="settings-section">
          <label>模型提供商</label>
          <select v-model="config.provider" class="config-input">
            <option value="deepseek">DeepSeek</option>
            <option value="openai">OpenAI</option>
          </select>
        </section>

        <section class="settings-section">
          <label>API 密钥 (API Key)</label>
          <input 
            type="password" 
            v-model="config.api_key" 
            class="config-input" 
            placeholder="输入您的 sk-..."
          />
        </section>

        <section class="settings-section">
          <label>接口地址 (Base URL)</label>
          <input 
            type="text" 
            v-model="config.base_url" 
            class="config-input" 
            placeholder="https://api.example.com/v1"
          />
        </section>
      </main>

      <footer class="settings-footer">
        <button class="save-btn" :disabled="saving" @click="handleSave">
          {{ saving ? '同步中...' : '保存并应用' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['close']);
const saving = ref(false);

const config = reactive({
  api_key: '',
  provider: 'deepseek',
  base_url: 'https://api.deepseek.com'
});

const handleSave = async () => {
  saving.value = true;
  try {
    await axios.post('http://localhost:8787/ai/update-settings', config);
    alert('配置已生效');
    emit('close');
  } catch (err) {
    alert('同步失败: ' + err.message);
  } finally {
    saving.value = false;
  }
};
</script>

<style scoped>
.settings-overlay {
  position: absolute; inset: 0; background: rgba(255,255,255,0.8);
  backdrop-filter: blur(10px); z-index: 100; display: flex; flex-direction: column;
}
.settings-content { height: 100%; display: flex; flex-direction: column; }
.settings-header {
  padding: 15px; border-bottom: 1px solid #eee; display: flex; 
  justify-content: space-between; align-items: center;
}
.settings-header h3 { margin: 0; font-size: 15px; color: #333; }
.close-btn { background: none; border: none; font-size: 22px; cursor: pointer; color: #999; }

.settings-body { padding: 20px; flex: 1; }
.settings-section { margin-bottom: 15px; }
.settings-section label { display: block; font-size: 12px; font-weight: 600; color: #666; margin-bottom: 6px; }

.config-input {
  width: 100%; padding: 8px 10px; border: 1px solid #ddd; border-radius: 6px;
  font-size: 13px; outline: none; box-sizing: border-box;
}
.config-input:focus { border-color: #007aff; }

.settings-footer { padding: 15px; border-top: 1px solid #eee; }
.save-btn {
  width: 100%; padding: 10px; background: #007aff; color: #fff; border: none;
  border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer;
}
.save-btn:disabled { background: #ccc; }
</style>