<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">找到古籍</h1>
        <p class="hero-subtitle">AI 时代的《古文观止》</p>
        <p class="hero-desc">
          让 AI 当你的古文老师，从浩如烟海的古籍中提取最相关的章节<br>
          既有高山仰止的名篇，也有被先人忽略的遗珠
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="goToLibrary">
            开始阅读
          </el-button>
          <el-button size="large" @click="goToAIChat">
            <el-icon><ChatDotRound /></el-icon>
            让 AI 推荐
          </el-button>
        </div>
      </div>
      <div class="hero-stats">
        <div class="stat-item">
          <div class="stat-number">300+</div>
          <div class="stat-label">精选文章</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">50+</div>
          <div class="stat-label">历代名家</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">20+</div>
          <div class="stat-label">朝代覆盖</div>
        </div>
      </div>
    </section>

    <!-- Featured Articles -->
    <section class="featured-section">
      <div class="section-header">
        <h2 class="section-title">
          <el-icon><StarFilled /></el-icon>
          今日推荐
        </h2>
        <el-button type="text" @click="goToLibrary">
          查看更多
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      
      <div class="articles-grid">
        <ArticleCard
          v-for="article in featuredArticles"
          :key="article.id"
          :article="article"
          @click="goToArticle(article.id)"
        />
      </div>
    </section>

    <section class="wordbook-section">
      <div class="section-header">
        <h2 class="section-title">
          <el-icon><Notebook /></el-icon>
          最近加入的生词
        </h2>
        <el-button type="text" @click="goToWordbook">
          查看生词库
          <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>

      <div v-if="recentWords.length" class="wordbook-grid">
        <el-card
          v-for="entry in recentWords"
          :key="entry.id"
          class="wordbook-card"
          shadow="hover"
          @click="goToWordbook"
        >
          <div class="wordbook-word">{{ entry.word }}</div>
          <div v-if="entry.pinyin" class="wordbook-pinyin">{{ entry.pinyin }}</div>
          <div class="wordbook-explanation">{{ entry.explanation }}</div>
          <div class="wordbook-source">
            {{ entry.article_title || '未知篇目' }}
          </div>
        </el-card>
      </div>

      <el-empty v-else description="还没有生词，去阅读页划词加入吧" />
    </section>

    <!-- Categories -->
    <section class="categories-section">
      <h2 class="section-title">
        <el-icon><Collection /></el-icon>
        分类浏览
      </h2>
      <div class="categories-grid">
        <div
          v-for="category in categories"
          :key="category.name"
          class="category-card"
          @click="goToCategory(category)"
        >
          <el-icon :size="32" :color="category.color">
            <component :is="category.icon" />
          </el-icon>
          <div class="category-name">{{ category.name }}</div>
          <div class="category-desc">{{ category.desc }}</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { articleApi, wordbookApi } from '@/api'
import ArticleCard from '@/components/ArticleCard.vue'
import type { Article, VocabularyEntry } from '@/types'

const router = useRouter()
const featuredArticles = ref<Article[]>([])
const recentWords = ref<VocabularyEntry[]>([])

const categories = [
  { name: '先秦散文', icon: 'Reading', color: '#409eff', desc: '诸子百家，思想启蒙', path: '/library/dynasty' },
  { name: '汉赋唐诗', icon: 'Document', color: '#67c23a', desc: '辞藻华美，气象万千', path: '/library/dynasty' },
  { name: '宋词元曲', icon: 'Microphone', color: '#e6a23c', desc: '婉约豪放，雅俗共赏', path: '/library/dynasty' },
  { name: '明清小品', icon: 'Coffee', color: '#f56c6c', desc: '性情文字，生活美学', path: '/library/dynasty' },
]

const loadFeaturedArticles = async () => {
  try {
    const res = await articleApi.getArticles({ is_selected: true, page_size: 6 })
    featuredArticles.value = res.items
  } catch (error) {
    console.error('加载推荐文章失败:', error)
  }
}

const loadRecentWords = async () => {
  try {
    const res = await wordbookApi.getEntries({ page_size: 4 })
    recentWords.value = res.items
  } catch (error) {
    console.error('加载生词失败:', error)
    recentWords.value = []
  }
}

const goToLibrary = () => router.push('/library')
const goToAIChat = () => router.push('/ai-chat')
const goToWordbook = () => router.push('/wordbook')
const goToArticle = (id: number) => router.push(`/article/${id}`)
const goToCategory = (category: any) => router.push(category.path)

onMounted(() => {
  void Promise.all([loadFeaturedArticles(), loadRecentWords()])
})
</script>

<style scoped lang="scss">
.home-view {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 60px;
  color: #fff;
  margin-bottom: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hero-content {
  flex: 1;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 8px;
  font-family: 'Noto Serif SC', serif;
}

.hero-subtitle {
  font-size: 24px;
  opacity: 0.9;
  margin-bottom: 16px;
}

.hero-desc {
  font-size: 16px;
  opacity: 0.8;
  line-height: 1.8;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  
  .el-button {
    padding: 12px 32px;
    font-size: 16px;
  }
}

.hero-stats {
  display: flex;
  gap: 40px;
  padding-left: 60px;
  border-left: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.featured-section {
  margin-bottom: 40px;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.wordbook-section {
  margin-bottom: 40px;
}

.wordbook-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.wordbook-card {
  cursor: pointer;
  border-radius: 14px;
}

.wordbook-word {
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.wordbook-pinyin {
  margin-top: 6px;
  color: #909399;
  font-size: 13px;
}

.wordbook-explanation {
  margin-top: 12px;
  color: #4b5563;
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.wordbook-source {
  margin-top: 14px;
  color: #909399;
  font-size: 13px;
}

.categories-section {
  margin-bottom: 40px;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.category-card {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
}

.category-name {
  font-size: 18px;
  font-weight: 600;
  margin: 16px 0 8px;
}

.category-desc {
  font-size: 14px;
  color: #909399;
}
</style>
