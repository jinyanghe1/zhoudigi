import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Article } from '@/api'

export const useArticleStore = defineStore('article', () => {
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const loading = ref(false)

  async function fetchArticles() {
    loading.value = true
    try {
      const { default: api } = await import('@/api')
      const res = await api.get<Article[]>('/articles')
      articles.value = res.data
    } catch (error) {
      console.error('Failed to fetch articles:', error)
    } finally {
      loading.value = false
    }
  }

  async function fetchArticle(id: number) {
    loading.value = true
    try {
      const { default: api } = await import('@/api')
      const res = await api.get<Article>(`/articles/${id}`)
      currentArticle.value = res.data
    } catch (error) {
      console.error('Failed to fetch article:', error)
    } finally {
      loading.value = false
    }
  }

  return {
    articles,
    currentArticle,
    loading,
    fetchArticles,
    fetchArticle
  }
})
