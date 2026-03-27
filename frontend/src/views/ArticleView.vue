<template>
  <div class="article-view">
    <div class="reader-header" :class="{ hidden: isReading }">
      <div class="header-left">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        <span class="article-title-small">{{ article?.title }}</span>
      </div>

      <div class="header-right">
        <el-button text @click="toggleAIPanel">
          <el-icon><ChatDotRound /></el-icon>
          问AI
        </el-button>
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

    <div class="reader-container" :class="{ fullscreen: isFullscreen, 'no-header': isReading }">
      <div class="reader-content" @scroll="closeSelectionPopup(false)">
        <article class="article-body">
          <h1 class="article-title">{{ article?.title }}</h1>

          <div v-if="article?.author" class="article-author">
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
            <div v-if="viewMode !== 'translation'" class="original-text">
              <div
                v-for="(paragraph, index) in contentParagraphs"
                :key="`orig-${index}`"
                class="paragraph"
                @mouseup="handleParagraphSelection(paragraph)"
              >
                {{ paragraph }}
              </div>
            </div>

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

        <ReadingSelectionPopup
          v-if="selectionPopup.visible"
          :x="selectionPopup.x"
          :y="selectionPopup.y"
          :text="selectionPopup.text"
          :source-text="selectionPopup.sourceText"
          :result="selectionPopup.result"
          :loading="selectionPopup.loading"
          :saving="selectionPopup.saving"
          @close="closeSelectionPopup()"
          @add="addSelectionToWordbook"
        />
      </div>

      <transition name="slide">
        <aside v-if="activePanel === 'knowledge'" class="knowledge-panel">
          <div class="panel-header">
            <h3>知识点</h3>
            <el-button text @click="activePanel = null">
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

      <transition name="slide">
        <ArticleAIChatPanel
          v-if="activePanel === 'ai'"
          :article="article"
          :selected-text="selectionPopup.visible ? selectionPopup.text : ''"
          :selected-context="selectionPopup.visible ? selectionPopup.sourceText : ''"
        />
      </transition>
    </div>

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
        <el-button type="primary" :loading="exporting" @click="handleExport">
          导出 PDF
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { articleApi, exportApi, wordbookApi } from '@/api'
import ReadingSelectionPopup from '@/components/ReadingSelectionPopup.vue'
import ArticleAIChatPanel from '@/components/ArticleAIChatPanel.vue'
import type { ArticleDetail, ExplainResult, KnowledgePoint } from '@/types'

type ViewMode = 'original' | 'translation' | 'bilingual'
type SidePanel = 'knowledge' | 'ai' | null

interface SelectionPopupState {
  visible: boolean
  text: string
  sourceText: string
  x: number
  y: number
  result: ExplainResult | null
  loading: boolean
  saving: boolean
}

const route = useRoute()
const router = useRouter()

const article = ref<ArticleDetail | null>(null)
const knowledgePoints = ref<KnowledgePoint[]>([])
const viewMode = ref<ViewMode>('original')
const activePanel = ref<SidePanel>(null)
const isFullscreen = ref(false)
const isReading = ref(false)
const showExportDialog = ref(false)
const exporting = ref(false)
const createDefaultSelectionPopup = (): SelectionPopupState => ({
  visible: false,
  text: '',
  sourceText: '',
  x: 16,
  y: 16,
  result: null,
  loading: false,
  saving: false
})

const selectionPopup = ref<SelectionPopupState>(createDefaultSelectionPopup())

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
  return article.value?.content?.split('\n').filter(paragraph => paragraph.trim()) || []
})

const translationParagraphs = computed(() => {
  return article.value?.translation?.split('\n').filter(paragraph => paragraph.trim()) || []
})

const buildWordbookExplanation = (result: ExplainResult) => {
  return [
    result.explanation,
    result.translation ? `译文：${result.translation}` : '',
    result.background ? `背景：${result.background}` : ''
  ].filter(Boolean).join('\n\n')
}

const closeSelectionPopup = (clearSelection = true) => {
  selectionPopup.value = createDefaultSelectionPopup()

  if (clearSelection) {
    window.getSelection()?.removeAllRanges()
  }
}

const loadArticle = async () => {
  const articleId = Number(route.params.id)
  if (!articleId) {
    return
  }

  try {
    article.value = await articleApi.getArticle(articleId)
    knowledgePoints.value = article.value?.knowledge_points || []
    closeSelectionPopup(false)
  } catch (error) {
    console.error('加载文章失败:', error)
    ElMessage.error('加载文章失败')
  }
}

const toggleKnowledgePanel = () => {
  activePanel.value = activePanel.value === 'knowledge' ? null : 'knowledge'
}

const toggleAIPanel = () => {
  activePanel.value = activePanel.value === 'ai' ? null : 'ai'
}

const toggleFullscreen = () => {
  isFullscreen.value = !isFullscreen.value
  isReading.value = isFullscreen.value
  closeSelectionPopup(false)
}

const goBack = () => {
  router.back()
}

const handleParagraphSelection = async (paragraph: string) => {
  const selection = window.getSelection()
  const selectedText = selection?.toString().trim() || ''
  if (!selectedText) {
    return
  }

  if (selectedText.length > 80) {
    ElMessage.warning('请控制在 80 字以内，便于更准确地解释')
    return
  }

  const range = selection?.rangeCount ? selection.getRangeAt(0) : null
  const rect = range?.getBoundingClientRect()
  if (!rect || (!rect.width && !rect.height)) {
    return
  }

  const popupX = Math.min(Math.max(rect.left, 12), Math.max(12, window.innerWidth - 380))
  const popupY = Math.min(rect.bottom + 12, Math.max(16, window.innerHeight - 520))

  selectionPopup.value = {
    visible: true,
    text: selectedText,
    sourceText: paragraph,
    x: popupX,
    y: popupY,
    result: null,
    loading: true,
    saving: false
  }

  try {
    const result = await wordbookApi.explainSelection(selectedText, paragraph)
    if (selectionPopup.value.text !== selectedText) {
      return
    }
    selectionPopup.value.result = result
  } catch (error) {
    console.error('划词解释失败:', error)
    if (selectionPopup.value.text === selectedText) {
      ElMessage.error('划词解释失败，请稍后重试')
      selectionPopup.value.result = {
        pinyin: '',
        explanation: '暂时无法生成释义，请稍后再试。',
        translation: '',
        background: ''
      }
    }
  } finally {
    if (selectionPopup.value.text === selectedText) {
      selectionPopup.value.loading = false
    }
  }
}

const addSelectionToWordbook = async () => {
  if (!article.value || !selectionPopup.value.result) {
    return
  }

  selectionPopup.value.saving = true

  try {
    await wordbookApi.createEntry({
      word: selectionPopup.value.text,
      pinyin: selectionPopup.value.result.pinyin,
      explanation: buildWordbookExplanation(selectionPopup.value.result),
      source_text: selectionPopup.value.sourceText,
      article_id: article.value.id
    })

    ElMessage.success('已加入生词库')
    closeSelectionPopup()
  } catch (error: any) {
    console.error('加入生词库失败:', error)
    const detail = error?.response?.data?.detail
    if (detail === '该生词已存在') {
      ElMessage.warning('该内容已在生词库中')
    } else {
      ElMessage.error('加入生词库失败，请稍后重试')
    }
  } finally {
    selectionPopup.value.saving = false
  }
}

const handleExport = async () => {
  if (!article.value) {
    return
  }

  exporting.value = true

  try {
    const blob = await exportApi.exportPDF(
      [article.value.id],
      exportOptions.value.translation,
      exportOptions.value.knowledge
    )

    const url = window.URL.createObjectURL(blob as Blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${article.value.title}.pdf`
    link.click()
    window.URL.revokeObjectURL(url)

    showExportDialog.value = false
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请稍后重试')
  } finally {
    exporting.value = false
  }
}

const handleDocumentClick = (event: MouseEvent) => {
  if (!selectionPopup.value.visible) {
    return
  }

  const target = event.target as HTMLElement | null
  if (target?.closest('.selection-popup') || target?.closest('.paragraph')) {
    return
  }

  closeSelectionPopup(false)
}

watch(() => route.params.id, () => {
  void loadArticle()
}, { immediate: true })

onMounted(() => {
  document.addEventListener('click', handleDocumentClick, true)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick, true)
})
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

.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.article-title-small {
  font-weight: 500;
  max-width: 320px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reader-container {
  flex: 1;
  display: flex;
  margin-top: 60px;
  overflow: hidden;

  &.fullscreen,
  &.no-header {
    margin-top: 0;
  }
}

.reader-content {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
  background: #f4ecd8;
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
    user-select: text;
    cursor: text;
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

.knowledge-panel {
  width: 360px;
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

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
