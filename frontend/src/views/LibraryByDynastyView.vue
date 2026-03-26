<template>
  <div class="library-dynasty-view">
    <h1 class="page-title">按朝代浏览</h1>
    
    <div class="dynasties-list">
      <div
        v-for="dynasty in dynasties"
        :key="dynasty.id"
        class="dynasty-section"
      >
        <div class="dynasty-header">
          <h2 class="dynasty-name">{{ dynasty.name }}</h2>
          <span class="dynasty-period">{{ dynasty.period }}</span>
          <p class="dynasty-desc">{{ dynasty.description }}</p>
        </div>
        
        <div class="authors-grid">
          <el-card
            v-for="author in getAuthorsByDynasty(dynasty.id)"
            :key="author.id"
            class="author-card"
            shadow="hover"
            @click="goToAuthor(author.id)"
          >
            <div class="author-name">{{ author.name }}</div>
            <div class="author-style" v-if="author.style">{{ author.style }}</div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { dynastyApi, authorApi } from '@/api'
import type { Dynasty, Author } from '@/types'

const router = useRouter()
const dynasties = ref<Dynasty[]>([])
const authors = ref<Author[]>([])

const loadData = async () => {
  try {
    const [dynastyRes, authorRes] = await Promise.all([
      dynastyApi.getDynasties(),
      authorApi.getAuthors({ page_size: 1000 })
    ])
    dynasties.value = dynastyRes
    authors.value = authorRes.items
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const getAuthorsByDynasty = (dynastyId: number) => {
  return authors.value.filter(a => a.dynasty_id === dynastyId).slice(0, 6)
}

const goToAuthor = (id: number) => {
  router.push(`/author/${id}`)
}

onMounted(loadData)
</script>

<style scoped lang="scss">
.library-dynasty-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 32px;
}

.dynasties-list {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.dynasty-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.dynasty-header {
  margin-bottom: 20px;
}

.dynasty-name {
  font-size: 24px;
  font-weight: 600;
  display: inline-block;
  margin-right: 12px;
}

.dynasty-period {
  color: #909399;
  font-size: 14px;
}

.dynasty-desc {
  margin-top: 8px;
  color: #606266;
  font-size: 14px;
}

.authors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.author-card {
  cursor: pointer;
  text-align: center;
  
  &:hover {
    transform: translateY(-2px);
  }
}

.author-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 4px;
}

.author-style {
  font-size: 12px;
  color: #909399;
}
</style>
