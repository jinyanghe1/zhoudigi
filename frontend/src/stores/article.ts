import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { articleApi } from '@/api'
import type { Article, ArticleDetail } from '@/types'

export const useArticleStore = defineStore('article', () => {
  // State
  const articles = ref<Article[]>([])
  const currentArticle = ref<ArticleDetail | null>(null)
  const loading = ref(false)
  const favorites = ref<number[]>([])
  
  // Getters
  const favoriteArticles = computed(() => {
    return articles.value.filter(a => favorites.value.includes(a.id))
  })
  
  // Actions
  const loadArticles = async (params = {}) => {
    loading.value = true
    try {
      const res = await articleApi.getArticles(params)
      articles.value = res.items
      return res
    } finally {
      loading.value = false
    }
  }
  
  const loadArticle = async (id: number) => {
    loading.value = true
    try {
      currentArticle.value = await articleApi.getArticle(id)
      return currentArticle.value
    } finally {
      loading.value = false
    }
  }
  
  const toggleFavorite = (id: number) => {
    const index = favorites.value.indexOf(id)
    if (index > -1) {
      favorites.value.splice(index, 1)
    } else {
      favorites.value.push(id)
    }
    // 持久化到 localStorage
    localStorage.setItem('favorites', JSON.stringify(favorites.value))
  }
  
  const isFavorite = (id: number) => {
    return favorites.value.includes(id)
  }
  
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
  
  return {
    articles,
    currentArticle,
    loading,
    favorites,
    favoriteArticles,
    loadArticles,
    loadArticle,
    toggleFavorite,
    isFavorite,
    loadFavorites
  }
})
