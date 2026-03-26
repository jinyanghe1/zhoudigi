<template>
  <div class="library-view">
    <div class="library-header">
      <h1 class="page-title">书库</h1>
      
      <div class="filter-bar">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="全部" name="all" />
          <el-tab-pane label="精选" name="selected" />
        </el-tabs>
        
        <el-input
          v-model="searchQuery"
          placeholder="搜索文章、作者..."
          class="search-input"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>
    
    <div class="articles-grid">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
        @click="goToArticle(article.id)"
      />
    </div>
    
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { articleApi } from '@/api'
import ArticleCard from '@/components/ArticleCard.vue'
import type { Article } from '@/types'

const route = useRoute()
const router = useRouter()

const articles = ref<Article[]>([])
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const searchQuery = ref('')
const activeTab = ref('all')
const loading = ref(false)

const loadArticles = async () => {
  loading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (activeTab.value === 'selected') {
      params.is_selected = true
    }
    
    if (searchQuery.value) {
      const res = await articleApi.searchArticles(
        searchQuery.value,
        currentPage.value,
        pageSize.value
      )
      articles.value = res.items
      total.value = res.pagination.total
    } else {
      const res = await articleApi.getArticles(params)
      articles.value = res.items
      total.value = res.pagination.total
    }
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const handleTabChange = () => {
  currentPage.value = 1
  loadArticles()
}

const handleSearch = () => {
  currentPage.value = 1
  loadArticles()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadArticles()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadArticles()
}

const goToArticle = (id: number) => {
  router.push(`/article/${id}`)
}

// 监听路由查询参数
watch(() => route.query.search, (val) => {
  if (val) {
    searchQuery.value = val as string
    loadArticles()
  }
}, { immediate: true })

onMounted(loadArticles)
</script>

<style scoped lang="scss">
.library-view {
  max-width: 1200px;
  margin: 0 auto;
}

.library-header {
  margin-bottom: 32px;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 24px;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 24px;
  
  .el-tabs {
    flex-shrink: 0;
  }
  
  .search-input {
    max-width: 300px;
  }
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0;
}
</style>
