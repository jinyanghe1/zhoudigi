<template>
  <div class="favorites-view">
    <h1 class="page-title">我的收藏</h1>
    
    <el-empty v-if="!favorites.length" description="还没有收藏任何文章">
      <el-button type="primary" @click="goToLibrary">去浏览文章</el-button>
    </el-empty>
    
    <div v-else class="favorites-list">
      <ArticleCard
        v-for="article in favorites"
        :key="article.id"
        :article="article"
        @click="goToArticle(article.id)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArticleCard from '@/components/ArticleCard.vue'
import type { Article } from '@/types'

const router = useRouter()
const favorites = ref<Article[]>([])

// 从 localStorage 读取收藏
const loadFavorites = () => {
  const stored = localStorage.getItem('favorites')
  if (stored) {
    try {
      favorites.value = JSON.parse(stored)
    } catch (e) {
      console.error('解析收藏失败:', e)
    }
  }
}

const goToLibrary = () => router.push('/library')
const goToArticle = (id: number) => router.push(`/article/${id}`)

onMounted(loadFavorites)
</script>

<style scoped lang="scss">
.favorites-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 32px;
}

.favorites-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>
