<template>
  <div class="selection-popup" :style="popupStyle">
    <div class="popup-header">
      <div class="popup-title">划词释义</div>
      <el-button text @click="$emit('close')">
        <el-icon><Close /></el-icon>
      </el-button>
    </div>

    <div class="selected-text">{{ text }}</div>

    <div v-if="loading" class="popup-loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>正在生成释义…</span>
    </div>

    <div v-else-if="result" class="popup-body">
      <div v-if="result.pinyin" class="info-block">
        <div class="label">拼音</div>
        <div class="value">{{ result.pinyin }}</div>
      </div>

      <div class="info-block">
        <div class="label">释义</div>
        <div class="value">{{ result.explanation }}</div>
      </div>

      <div v-if="result.translation" class="info-block">
        <div class="label">译文</div>
        <div class="value">{{ result.translation }}</div>
      </div>

      <div v-if="result.background" class="info-block">
        <div class="label">背景</div>
        <div class="value">{{ result.background }}</div>
      </div>

      <div v-if="sourceText" class="info-block">
        <div class="label">原文</div>
        <div class="value source-text">{{ sourceText }}</div>
      </div>
    </div>

    <div class="popup-footer">
      <el-button
        type="primary"
        size="small"
        :loading="saving"
        :disabled="loading || !result"
        @click="$emit('add')"
      >
        加入生词库
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Close, Loading } from '@element-plus/icons-vue'
import type { ExplainResult } from '@/types'

const props = defineProps<{
  x: number
  y: number
  text: string
  sourceText?: string
  result: ExplainResult | null
  loading: boolean
  saving: boolean
}>()

defineEmits<{
  close: []
  add: []
}>()

const popupStyle = computed(() => ({
  left: `${props.x}px`,
  top: `${props.y}px`
}))
</script>

<style scoped lang="scss">
.selection-popup {
  position: fixed;
  z-index: 300;
  width: min(360px, calc(100vw - 24px));
  max-height: min(480px, calc(100vh - 24px));
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(229, 231, 235, 0.9);
  border-radius: 16px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.16);
  backdrop-filter: blur(12px);
}

.popup-header,
.popup-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
}

.popup-header {
  border-bottom: 1px solid #ebeef5;
}

.popup-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.selected-text {
  margin: 16px 16px 0;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 10px;
  color: #111827;
  font-size: 16px;
  font-weight: 600;
}

.popup-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  color: #606266;
}

.popup-body {
  padding: 12px 16px 4px;
}

.info-block {
  margin-bottom: 12px;
}

.label {
  margin-bottom: 4px;
  font-size: 12px;
  color: #909399;
}

.value {
  color: #303133;
  line-height: 1.7;
  white-space: pre-wrap;
}

.source-text {
  font-size: 14px;
  color: #606266;
}

.popup-footer {
  justify-content: flex-end;
  border-top: 1px solid #ebeef5;
}
</style>
