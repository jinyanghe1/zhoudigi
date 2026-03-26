<template>
  <div class="article-view">
    <!-- 阅读器头部 -->
    <div class="reader-header" :class="{ 'hidden': isReading }">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <span class="article-title-small">{{ article?.title }}</span>
      </div>
      <div class="header-right">
        <el-button text @click="toggleKnowledgePanel">
          <el-icon><Notebook /></el-icon>
          知识点
        </el-button>
        <el-button text @click="showExportDialog = true">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
        <el-button text @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
          {{ isFullscreen ? '退出全屏' : '全屏' }}
        </el-button>
      </div>
    </div>
    
    <!-- 阅读器主体 -->
    <div class="reader-container" :class="{ 'fullscreen': isFullscreen, 'no-header': isReading }">
      <div class="reader-content" ref="contentRef">
        <article class="article-body">
          <h1 class="article-title">{{ article?.title }}</h1>
          
          <div class="article-author" v-if="article?.author">
            <span class="dynasty">{{ article.dynasty?.name }}</span>
            <span class="author-name">{{ article.author.name }}</span>
          </div>
          
          <div class="article-tabs">
            <el-radio-group v-model="viewMode" size="small">
              <el-radio-button label="original">原文</el-radio-button>
              <el-radio-button label="translation">译文</el-radio-button>
              <el-radio-button label="bilingual">对照</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="article-text" :class="viewMode">
            <!-- 原文 -->
            <div v-if="viewMode !== 'translation'" class="original-text">
              <div
                v-for="(paragraph, index) in contentParagraphs"
                :key="`orig-${index}`"
                class="paragraph"
                @click="handleTextClick($event, paragraph)"
              >
                {{ paragraph }}
              </div>
            </div>
            
            <!-- 译文 -->
            <div v-if="viewMode !== 'original'" class="translation-text">
              <div
                v-for="(paragraph, index) in translationParagraphs"
                :key="`trans-${index}`"
                class="paragraph"
              >
                {{ paragraph }}
              </div>
            </div>
          </div>
        </article>
      </div>
      
      <!-- 知识点侧边栏 -->
      <transition name="slide">
        <aside v-if="showKnowledgePanel" class="knowledge-panel">
          <div class="panel-header">
            <h3>知识点</h3>
            <el-button text @click="showKnowledgePanel = false">
              <el-icon><Close /></el-icon>
            </el-button>
          </div>
          
          <div class="panel-content">
            <el-empty v-if="!knowledgePoints.length" description="暂无知识点" />
            
            <div v-else class="knowledge-list">
              <div
                v-for="point in knowledgePoints"
                :key="point.id"
                class="knowledge-item"
              >
                <div class="knowledge-type" :class="point.type">
                  {{ typeLabel[point.type] }}
                </div>
                <div class="knowledge-content">{{ point.content }}</div>
                <div v-if="point.explanation" class="knowledge-explanation">
                  {{ point.explanation }}
                </div>
              </div>
            </div>
          </div>
        </aside>
      </transition>
    </div>
    
    <!-- 导出对话框 -->
    <el-dialog
      v-model="showExportDialog"
      title="导出文章"
      width="400px"
    >
      <el-form>
        <el-form-item label="包含内容">
          <el-checkbox v-model="exportOptions.translation">译文</el-checkbox>
          <el-checkbox v-model="exportOptions.knowledge">知识点</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showExportDialog = false">取消</el-button>
        <el-button type="primary" @click="handleExport" :loading="exporting">
          导出 PDF
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { articleApi, exportApi } from '@/api'
import type { ArticleDetail, KnowledgePoint } from '@/types'

const route = useRoute()
const router = useRouter()

const article = ref<ArticleDetail | null>(null)
const knowledgePoints = ref<KnowledgePoint[]>([])
const viewMode = ref<'original' | 'translation' | 'bilingual'>('original')
const showKnowledgePanel = ref(false)
const isFullscreen = ref(false)
const isReading = ref(false)
const showExportDialog = ref(false)
const exporting = ref(false)

const exportOptions = ref({
  translation: true,
  knowledge: true
})

const typeLabel: Record<string, string> = {
  vocab: '词汇',
  background: '背景',
  analysis: '赏析'
}

const contentParagraphs = computed(() => {
  return article.value?.content?.split('\n').filter(p => p.trim()) || []
})

const translationParagraphs = computed(() => {
  return article.value?.translation?.split('\n').filter(p => p.trim()) || []
})

const loadArticle = async () => {
  const id = Number(route.params.id)
  if (!id) return
  
  try {
    article.value = await articleApi.getArticle(id)
    knowledgePoints.value = article.value?.knowledge_points || []
  } catch (error) {
    console.error('加载文章失败:', error)
  }
}

const toggleKnowledgePanel = () => {
  showKnowledgePanel.value = !showKnowledgePanel.value
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  isReading.value = isFullscreen.value
}

const goBack = () => {
  router.back()
}

const handleTextClick = (event: MouseEvent, text: string) => {
  // 可以在这里实现选词解释功能
  const selection = window.getSelection()?.toString()
  if (selection) {
    console.log('选中:', selection)
  }
}

const handleExport = async () => {
  if (!article.value) return
  
  exporting.value = true
  try {
    const blob = await exportApi.exportPDF(
      [article.value.id],
      exportOptions.value.translation,
      exportOptions.value.knowledge
    )
    
    // 下载文件
    const url = window.URL.createObjectURL(blob as Blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${article.value.title}.pdf`
    link.click()
    window.URL.revokeObjectURL(url)
    
    showExportDialog.value = false
  } catch (error) {
    console.error('导出失败:', error)
  } finally {
    exporting.value = false
  }
}

onMounted(loadArticle)
</script>

<style scoped lang="scss">
.article-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.reader-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 100;
  transition: transform 0.3s;
  
  &.hidden {
    transform: translateY(-100%);
  }
}

.header-left, .header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.article-title-small {
  font-weight: 500;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reader-container {
  flex: 1;
  display: flex;
  margin-top: 60px;
  overflow: hidden;
  
  &.fullscreen {
    margin-top: 0;
  }
  
  &.no-header {
    margin-top: 0;
  }
}

.reader-content {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
  background: #f4ecd8; // 护眼模式背景
}

.article-body {
  max-width: 800px;
  margin: 0 auto;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 16px;
  font-family: 'Noto Serif SC', serif;
}

.article-author {
  text-align: center;
  color: #666;
  margin-bottom: 32px;
  
  .dynasty {
    margin-right: 8px;
  }
  
  .author-name {
    font-weight: 500;
  }
}

.article-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.article-text {
  font-size: 18px;
  line-height: 2;
  font-family: 'Noto Serif SC', 'SimSun', serif;
  
  .paragraph {
    text-indent: 2em;
    margin-bottom: 1em;
  }
  
  &.bilingual {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    
    .original-text,
    .translation-text {
      padding: 20px;
      background: rgba(255, 255, 255, 0.5);
      border-radius: 8px;
    }
  }
}

.translation-text {
  color: #666;
}

// 知识点面板
.knowledge-panel {
  width: 350px;
  background: #fff;
  border-left: 1px solid #ebeef5;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  
  h3 {
    margin: 0;
    font-size: 16px;
  }
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.knowledge-item {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.knowledge-type {
  display: inline-block;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
  
  &.vocab {
    background: #ecf5ff;
    color: #409eff;
  }
  
  &.background {
    background: #f0f9eb;
    color: #67c23a;
  }
  
  &.analysis {
    background: #fdf6ec;
    color: #e6a23c;
  }
}

.knowledge-content {
  font-weight: 500;
  margin-bottom: 8px;
}

.knowledge-explanation {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

// 动画
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
