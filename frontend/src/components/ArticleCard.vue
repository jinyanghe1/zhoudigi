<template>
  <div class="article-card" @click="$emit('click')">
    <div class="card-header">
      <h3 class="article-title">{{ article.title }}</h3>
      <span v-if="article.is_selected" class="selected-badge">精选</span>
    </div>
    
    <div class="article-meta">
      <span class="author" v-if="article.author_id">
        <el-icon><User /></el-icon>
        {{ article.author?.name || '未知' }}
      </span>
      <span class="dynasty" v-if="article.dynasty_id">
        <el-icon><Timer /></el-icon>
        {{ article.dynasty?.name || '未知' }}
      </span>
      <span class="word-count" v-if="article.word_count">
        <el-icon><Document /></el-icon>
        {{ article.word_count }} 字
      </span>
    </div>
    
    <p class="article-preview">
      {{ previewText }}
    </p>
    
    <div class="card-footer">
      <span class="read-count">
        <el-icon><View /></el-icon>
        {{ article.read_count }} 次阅读
      </span>
      <el-button type="primary" text size="small">
        阅读全文
        <el-icon><ArrowRight /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Article } from '@/types'

interface Props {
  article: Article
}

const props = defineProps<Props>()
defineEmits(['click'])

const previewText = computed(() => {
  const content = props.article.content || ''
  return content.slice(0, 100).replace(/\n/g, ' ') + (content.length > 100 ? '...' : '')
})
</script>

<style scoped lang="scss">
.article-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
  margin: 0;
  flex: 1;
}

.selected-badge {
  background: linear-gradient(135deg, #f56c6c, #e6a23c);
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 8px;
  flex-shrink: 0;
}

.article-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 13px;
  color: #909399;
  
  span {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.article-preview {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  flex: 1;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.read-count {
  font-size: 13px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
