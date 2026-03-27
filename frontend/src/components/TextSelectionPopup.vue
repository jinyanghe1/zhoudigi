<template>
  <div
    v-if="visible"
    class="text-popup"
    :style="{ left: position.x + 'px', top: position.y + 'px' }"
  >
    <div class="popup-header">
      <span class="selected-text">{{ selectedText }}</span>
      <el-button
        v-if="explanation"
        type="primary"
        size="small"
        @click="addToVocabulary"
        :loading="adding"
      >
        <el-icon><Plus /></el-icon>
        加入生词库
      </el-button>
    </div>
    
    <div v-if="loading" class="popup-loading">
      <el-icon class="loading-icon"><Loading /></el-icon>
      正在解释...
    </div>
    
    <div v-else-if="explanation" class="popup-content">
      <div v-if="explanation.pinyin" class="info-row">
        <span class="label">拼音：</span>
        <span class="pinyin">{{ explanation.pinyin }}</span>
      </div>
      <div v-if="explanation.explanation" class="info-row">
        <span class="label">释义：</span>
        <span class="explanation">{{ explanation.explanation }}</span>
      </div>
      <div v-if="explanation.translation" class="info-row">
        <span class="label">翻译：</span>
        <span class="translation">{{ explanation.translation }}</span>
      </div>
      <div v-if="explanation.background" class="info-row">
        <span class="label">背景：</span>
        <span class="background">{{ explanation.background }}</span>
      </div>
    </div>
    
    <div v-else class="popup-error">
      <el-text type="info">选中文字查看释义</el-text>
    </div>
    
    <!-- 问 AI 按钮 -->
    <div class="popup-footer">
      <el-button type="primary" size="small" @click="askAI">
        <el-icon><ChatDotRound /></el-icon>
        问 AI
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Loading, ChatDotRound } from '@element-plus/icons-vue'
import { vocabularyApi } from '@/api/vocabulary'
import type { TextExplanation } from '@/api/vocabulary'

interface Props {
  visible: boolean
  position: { x: number; y: number }
  selectedText: string
  contextText?: string
  articleId: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:visible': [value: boolean]
  'ask-ai': [text: string]
}>()

const loading = ref(false)
const adding = ref(false)
const explanation = ref<TextExplanation | null>(null)

// 监听选中文本变化，自动获取解释
watch(() => props.selectedText, async (newText) => {
  if (!newText || newText.length > 50) {
    explanation.value = null
    return
  }
  
  loading.value = true
  try {
    const res = await vocabularyApi.explain(newText, props.contextText)
    explanation.value = res
  } catch (error) {
    console.error('获取解释失败:', error)
    explanation.value = null
  } finally {
    loading.value = false
  }
}, { immediate: true })

const addToVocabulary = async () => {
  if (!explanation.value) return
  
  adding.value = true
  try {
    await vocabularyApi.create({
      word: props.selectedText,
      pinyin: explanation.value.pinyin,
      explanation: explanation.value.explanation,
      source_text: props.contextText,
      article_id: props.articleId
    })
    ElMessage.success('已加入生词库')
    emit('update:visible', false)
  } catch (error: any) {
    if (error.response?.status === 409) {
      ElMessage.warning('该生词已存在')
    } else {
      ElMessage.error('添加失败')
    }
  } finally {
    adding.value = false
  }
}

const askAI = () => {
  emit('ask-ai', props.selectedText)
  emit('update:visible', false)
}
</script>

<style scoped lang="scss">
.text-popup {
  position: fixed;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  padding: 16px;
  min-width: 280px;
  max-width: 400px;
  z-index: 1000;
  
  &::before {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 8px solid #fff;
  }
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ebeef5;
}

.selected-text {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  font-family: 'Noto Serif SC', serif;
}

.popup-loading {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  padding: 20px 0;
  justify-content: center;
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.popup-content {
  .info-row {
    margin-bottom: 12px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .label {
    font-weight: 500;
    color: #606266;
  }
  
  .pinyin {
    color: #409eff;
    font-family: monospace;
  }
  
  .explanation,
  .translation,
  .background {
    color: #303133;
    line-height: 1.6;
  }
}

.popup-error {
  padding: 20px 0;
  text-align: center;
}

.popup-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
}
</style>
