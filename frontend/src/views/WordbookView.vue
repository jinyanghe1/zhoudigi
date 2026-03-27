<template>
  <div class="wordbook-view">
    <div class="page-header">
      <div>
        <h1 class="page-title">生词库</h1>
        <p class="page-desc">保存你在阅读中划出的词语、句子与释义。</p>
      </div>

      <el-button :loading="loading" @click="loadEntries">刷新</el-button>
    </div>

    <div class="toolbar">
      <el-input
        v-model="searchKeyword"
        clearable
        placeholder="搜索词语、释义或篇名"
        class="search-input"
      />
      <el-tag type="info">共 {{ filteredEntries.length }} 条</el-tag>
    </div>

    <el-empty
      v-if="!loading && filteredEntries.length === 0"
      description="还没有生词，去阅读页划词加入吧"
    />

    <div v-else class="wordbook-grid">
      <el-card
        v-for="entry in filteredEntries"
        :key="entry.id"
        class="word-card"
        shadow="hover"
      >
        <div class="card-header">
          <div>
            <div class="word">{{ entry.word }}</div>
            <div v-if="entry.pinyin" class="pinyin">{{ entry.pinyin }}</div>
          </div>

          <el-button text type="danger" @click="removeEntry(entry.id)">删除</el-button>
        </div>

        <div class="meta-row">
          <el-tag size="small">{{ entry.dynasty_name || '未标注朝代' }}</el-tag>
          <span class="article-title">{{ entry.article_title || '未知篇目' }}</span>
        </div>

        <div class="explanation">{{ entry.explanation }}</div>

        <blockquote v-if="entry.source_text" class="source-text">
          {{ entry.source_text }}
        </blockquote>

        <div class="card-footer">
          <span>{{ formatDate(entry.created_at) }}</span>
          <el-button link type="primary" @click="goToArticle(entry.article_id)">
            回到原文
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { wordbookApi } from '@/api'
import type { VocabularyEntry } from '@/types'

const router = useRouter()
const loading = ref(false)
const searchKeyword = ref('')
const entries = ref<VocabularyEntry[]>([])

const filteredEntries = computed(() => {
  const keyword = searchKeyword.value.trim().toLowerCase()
  if (!keyword) {
    return entries.value
  }

  return entries.value.filter(entry => {
    return [
      entry.word,
      entry.pinyin,
      entry.explanation,
      entry.article_title,
      entry.source_text
    ]
      .filter(Boolean)
      .some(value => value!.toLowerCase().includes(keyword))
  })
})

const loadEntries = async () => {
  loading.value = true

  try {
    const response = await wordbookApi.getEntries({ page_size: 100 })
    entries.value = response.items
  } catch (error) {
    console.error('加载生词库失败:', error)
    ElMessage.error('加载生词库失败')
  } finally {
    loading.value = false
  }
}

const removeEntry = async (id: number) => {
  try {
    await wordbookApi.deleteEntry(id)
    entries.value = entries.value.filter(entry => entry.id !== id)
    ElMessage.success('已从生词库移除')
  } catch (error) {
    console.error('删除生词失败:', error)
    ElMessage.error('删除失败，请稍后重试')
  }
}

const goToArticle = (articleId: number) => {
  router.push(`/article/${articleId}`)
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  void loadEntries()
})
</script>

<style scoped lang="scss">
.wordbook-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.page-title {
  margin: 0 0 8px;
  font-size: 32px;
}

.page-desc {
  margin: 0;
  color: #909399;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  max-width: 360px;
}

.wordbook-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.word-card {
  border-radius: 16px;
}

.card-header,
.card-footer,
.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.word {
  font-size: 22px;
  font-weight: 700;
  color: #1f2937;
}

.pinyin {
  margin-top: 4px;
  color: #909399;
  font-size: 13px;
}

.meta-row {
  margin: 16px 0 12px;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.article-title {
  color: #606266;
  font-size: 14px;
}

.explanation {
  color: #303133;
  line-height: 1.8;
  white-space: pre-wrap;
}

.source-text {
  margin: 16px 0 0;
  padding: 12px 14px;
  border-left: 3px solid #dcdfe6;
  background: #f8fafc;
  color: #606266;
  line-height: 1.7;
}

.card-footer {
  margin-top: 16px;
  color: #909399;
  font-size: 13px;
}
</style>
