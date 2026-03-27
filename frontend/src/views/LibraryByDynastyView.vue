<template>
  <div class="library-dynasty-view">
    <h1 class="page-title">按朝代浏览</h1>
    
    <!-- 调试信息（开发时显示） -->
    <div v-if="debug" class="debug-info">
      <p>加载状态: {{ loading }}</p>
      <p>朝代数量: {{ dynasties.length }}</p>
      <p>作者数量: {{ authors.length }}</p>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 空状态 -->
    <div v-else-if="dynasties.length === 0" class="empty-container">
      <el-empty description="暂无朝代数据">
        <el-button type="primary" @click="loadData">重新加载</el-button>
      </el-empty>
    </div>
    
    <!-- 数据展示 -->
    <div v-else class="dynasties-list">
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
        
        <div v-if="getAuthorsByDynasty(dynasty.id).length > 0" class="authors-grid">
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
        <div v-else class="no-authors">
          <el-text type="info">暂无作者数据</el-text>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { dynastyApi, authorApi } from '@/api'
import type { Dynasty, Author } from '@/types'

const router = useRouter()
const dynasties = ref<Dynasty[]>([])
const authors = ref<Author[]>([])
const loading = ref(false)
const debug = ref(false) // 开发调试模式

// 计算属性：按朝代分组的作者
const authorsByDynasty = computed(() => {
  const map: Record<number, Author[]> = {}
  for (const author of authors.value) {
    if (author.dynasty_id) {
      if (!map[author.dynasty_id]) {
        map[author.dynasty_id] = []
      }
      map[author.dynasty_id].push(author)
    }
  }
  return map
})

const loadData = async () => {
  loading.value = true
  console.log('[LibraryByDynasty] 开始加载数据...')
  
  try {
    // 分别调用API，便于调试
    console.log('[LibraryByDynasty] 调用朝代API...')
    const dynastyRes = await dynastyApi.getDynasties()
    console.log('[LibraryByDynasty] 朝代API响应:', dynastyRes)
    
    console.log('[LibraryByDynasty] 调用作者API...')
    const authorRes = await authorApi.getAuthors({ page_size: 100 })
    console.log('[LibraryByDynasty] 作者API响应:', authorRes)
    
    // 确保数据是数组
    dynasties.value = Array.isArray(dynastyRes) ? dynastyRes : []
    authors.value = authorRes?.items || []
    
    console.log('[LibraryByDynasty] 数据加载完成:', {
      dynastiesCount: dynasties.value.length,
      authorsCount: authors.value.length
    })
    
    if (dynasties.value.length === 0) {
      ElMessage.warning('未获取到朝代数据')
    }
  } catch (error: any) {
    console.error('[LibraryByDynasty] 加载数据失败:', error)
    ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
    console.log('[LibraryByDynasty] loading状态:', loading.value)
  }
}

const getAuthorsByDynasty = (dynastyId: number) => {
  const list = authorsByDynasty.value[dynastyId] || []
  return list.slice(0, 6)
}

const goToAuthor = (id: number) => {
  router.push(`/author/${id}`)
}

// 组件挂载时加载数据
onMounted(() => {
  console.log('[LibraryByDynasty] 组件挂载，准备加载数据')
  loadData()
})
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

.debug-info {
  background: #f0f9ff;
  border: 1px solid #91caff;
  padding: 12px;
  margin-bottom: 20px;
  border-radius: 8px;
  font-size: 14px;
  color: #0958d9;
}

.loading-container,
.empty-container {
  padding: 60px 40px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
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

.no-authors {
  padding: 20px;
  text-align: center;
  color: #909399;
}
</style>
