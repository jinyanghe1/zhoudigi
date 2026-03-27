<template>
  <div class="vocabulary-view">
    <h1 class="page-title">我的生词库</h1>
    
    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-value">{{ totalCount }}</div>
        <div class="stat-label">总生词数</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ masteredCount }}</div>
        <div class="stat-label">已掌握</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ learningCount }}</div>
        <div class="stat-label">学习中</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-value">{{ todayReviewCount }}</div>
        <div class="stat-label">今日复习</div>
      </el-card>
    </div>
    
    <!-- 筛选工具栏 -->
    <div class="toolbar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索生词..."
        class="search-input"
        clearable
        @clear="handleSearch"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <el-select v-model="filterMastery" placeholder="掌握程度" clearable @change="handleSearch">
        <el-option label="未学习" :value="0" />
        <el-option label="初步了解" :value="1" />
        <el-option label="基本掌握" :value="2" />
        <el-option label="熟练掌握" :value="3" />
        <el-option label="精通" :value="4" />
        <el-option label="完全掌握" :value="5" />
      </el-select>
      
      <el-select v-model="sortBy" placeholder="排序方式" @change="handleSearch">
        <el-option label="最近添加" value="newest" />
        <el-option label="掌握程度" value="mastery" />
        <el-option label="复习次数" value="review" />
      </el-select>
    </div>
    
    <!-- 生词列表 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <el-empty v-else-if="vocabularies.length === 0" description="暂无生词，去阅读页面添加吧" />
    
    <div v-else class="vocab-list">
      <el-card
        v-for="item in vocabularies"
        :key="item.id"
        class="vocab-card"
        shadow="hover"
      >
        <div class="vocab-header">
          <div class="vocab-word">
            <span class="word-text">{{ item.word }}</span>
            <span v-if="item.pinyin" class="word-pinyin">{{ item.pinyin }}</span>
          </div>
          <div class="vocab-actions">
            <el-tag :type="getMasteryType(item.mastery_level)">
              {{ getMasteryLabel(item.mastery_level) }}
            </el-tag>
            <el-dropdown trigger="click">
              <el-button type="text">
                <el-icon><More /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="editVocabulary(item)">编辑</el-dropdown-item>
                  <el-dropdown-item @click="reviewVocabulary(item)">标记复习</el-dropdown-item>
                  <el-dropdown-item divided @click="deleteVocabulary(item.id)">删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="vocab-explanation">{{ item.explanation }}</div>
        
        <div v-if="item.source_text" class="vocab-source">
          <div class="source-label">原文：</div>
          <div class="source-text">{{ item.source_text }}</div>
        </div>
        
        <div class="vocab-meta">
          <span v-if="item.article_title" class="meta-item">
            <el-icon><Document /></el-icon>
            {{ item.article_title }}
          </span>
          <span v-if="item.dynasty_name" class="meta-item">
            <el-icon><Timer /></el-icon>
            {{ item.dynasty_name }}
          </span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            复习 {{ item.review_count }} 次
          </span>
        </div>
      </el-card>
    </div>
    
    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSearch"
        @current-change="handleSearch"
      />
    </div>
    
    <!-- 编辑对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑生词" width="500px">
      <el-form :model="editingVocab" label-width="80px">
        <el-form-item label="词语">
          <el-input v-model="editingVocab.word" disabled />
        </el-form-item>
        <el-form-item label="拼音">
          <el-input v-model="editingVocab.pinyin" />
        </el-form-item>
        <el-form-item label="释义">
          <el-input v-model="editingVocab.explanation" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="掌握程度">
          <el-slider v-model="editingVocab.mastery_level" :max="5" show-stops />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveEdit" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, More, Document, Timer, View } from '@element-plus/icons-vue'
import { vocabularyApi } from '@/api/vocabulary'
import type { Vocabulary } from '@/api/vocabulary'

const vocabularies = ref<Vocabulary[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const filterMastery = ref<number | undefined>()
const sortBy = ref('newest')

// 统计
const totalCount = computed(() => total.value)
const masteredCount = computed(() => vocabularies.value.filter(v => v.mastery_level >= 4).length)
const learningCount = computed(() => vocabularies.value.filter(v => v.mastery_level < 4).length)
const todayReviewCount = computed(() => vocabularies.value.filter(v => {
  const today = new Date().toDateString()
  const updated = new Date(v.updated_at || v.created_at).toDateString()
  return today === updated
}).length)

// 加载生词列表
const loadVocabularies = async () => {
  loading.value = true
  try {
    const res = await vocabularyApi.getList({
      page: currentPage.value,
      page_size: pageSize.value
    })
    vocabularies.value = res.items
    total.value = res.pagination.total
  } catch (error) {
    console.error('加载生词失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadVocabularies()
}

// 掌握程度标签
const getMasteryLabel = (level: number) => {
  const labels = ['未学习', '初步了解', '基本掌握', '熟练掌握', '精通', '完全掌握']
  return labels[level] || '未学习'
}

const getMasteryType = (level: number): any => {
  const types = ['info', 'info', 'warning', 'warning', 'success', 'success']
  return types[level] || 'info'
}

// 编辑功能
const showEditDialog = ref(false)
const editingVocab = ref<Partial<Vocabulary>>({})
const saving = ref(false)

const editVocabulary = (item: Vocabulary) => {
  editingVocab.value = { ...item }
  showEditDialog.value = true
}

const saveEdit = async () => {
  if (!editingVocab.value.id) return
  
  saving.value = true
  try {
    await vocabularyApi.update(editingVocab.value.id, {
      pinyin: editingVocab.value.pinyin,
      explanation: editingVocab.value.explanation,
      mastery_level: editingVocab.value.mastery_level
    })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    loadVocabularies()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 复习功能
const reviewVocabulary = async (item: Vocabulary) => {
  try {
    await vocabularyApi.review(item.id)
    ElMessage.success('已标记复习')
    loadVocabularies()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 删除功能
const deleteVocabulary = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除这个生词吗？', '提示', {
      type: 'warning'
    })
    await vocabularyApi.delete(id)
    ElMessage.success('删除成功')
    loadVocabularies()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(loadVocabularies)
</script>

<style scoped lang="scss">
.vocabulary-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 24px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  text-align: center;
  
  .stat-value {
    font-size: 36px;
    font-weight: 700;
    color: #409eff;
    margin-bottom: 8px;
  }
  
  .stat-label {
    font-size: 14px;
    color: #909399;
  }
}

.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  
  .search-input {
    width: 300px;
  }
}

.loading-container {
  padding: 40px;
}

.vocab-list {
  display: grid;
  gap: 16px;
}

.vocab-card {
  .vocab-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;
  }
  
  .vocab-word {
    display: flex;
    align-items: baseline;
    gap: 12px;
    
    .word-text {
      font-size: 20px;
      font-weight: 600;
      font-family: 'Noto Serif SC', serif;
    }
    
    .word-pinyin {
      color: #909399;
      font-size: 14px;
    }
  }
  
  .vocab-actions {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .vocab-explanation {
    font-size: 14px;
    line-height: 1.8;
    color: #303133;
    margin-bottom: 12px;
  }
  
  .vocab-source {
    background: #f5f7fa;
    padding: 12px;
    border-radius: 6px;
    margin-bottom: 12px;
    
    .source-label {
      font-size: 12px;
      color: #909399;
      margin-bottom: 4px;
    }
    
    .source-text {
      font-size: 13px;
      color: #606266;
      font-style: italic;
    }
  }
  
  .vocab-meta {
    display: flex;
    gap: 16px;
    font-size: 13px;
    color: #909399;
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}
</style>
