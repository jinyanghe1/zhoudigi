<template>
  <div class="library-author-view">
    <h1 class="page-title">按作者浏览</h1>
    
    <div class="authors-list">
      <el-card
        v-for="author in authors"
        :key="author.id"
        class="author-item"
        shadow="hover"
      >
        <div class="author-header">
          <h3 class="author-name">{{ author.name }}</h3>
          <el-tag v-if="author.dynasty" size="small">{{ author.dynasty.name }}</el-tag>
        </div>
        
        <p class="author-bio">{{ author.bio || '暂无简介' }}</p>
        
        <div class="author-tags" v-if="author.style">
          <el-tag type="info" size="small">{{ author.style }}</el-tag>
        </div>
        
        <div class="author-footer">
          <el-button type="primary" text @click="goToAuthor(author.id)">
            查看作品
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </el-card>
    </div>
    
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authorApi } from '@/api'
import type { AuthorWithDynasty } from '@/types'

const router = useRouter()
const authors = ref<AuthorWithDynasty[]>([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const loadAuthors = async () => {
  try {
    const res = await authorApi.getAuthors({
      page: currentPage.value,
      page_size: pageSize.value
    })
    authors.value = res.items
    total.value = res.pagination.total
  } catch (error) {
    console.error('加载作者失败:', error)
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  loadAuthors()
}

const goToAuthor = (id: number) => {
  router.push(`/author/${id}`)
}

onMounted(loadAuthors)
</script>

<style scoped lang="scss">
.library-author-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 32px;
}

.authors-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.author-item {
  cursor: pointer;
  
  &:hover {
    transform: translateY(-2px);
  }
}

.author-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.author-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.author-bio {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.author-tags {
  margin-bottom: 12px;
}

.author-footer {
  display: flex;
  justify-content: flex-end;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}
</style>
