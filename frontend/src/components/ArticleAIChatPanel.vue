<template>
  <aside class="article-ai-panel">
    <div class="panel-header">
      <div>
        <h3>问 AI</h3>
        <p>{{ contextHint }}</p>
      </div>
    </div>

    <div class="quick-prompts">
      <el-button
        v-for="prompt in quickPrompts"
        :key="prompt"
        text
        class="prompt-button"
        @click="sendMessage(prompt)"
      >
        {{ prompt }}
      </el-button>
    </div>

    <div class="messages-container" ref="messagesRef">
      <div v-if="booting" class="loading-state">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在恢复问答记录…</span>
      </div>

      <el-empty
        v-else-if="visibleMessages.length === 0"
        description="现在就问 AI，回答会和这篇文章一起保存在当前设备会话里"
      />

      <template v-else>
        <div
          v-for="message in visibleMessages"
          :key="message.id"
          class="message"
          :class="message.role"
        >
          <div class="message-content" v-html="formatMessage(message.content)"></div>
        </div>
      </template>

      <div v-if="sending" class="message assistant">
        <div class="message-content">
          <el-icon class="is-loading"><Loading /></el-icon>
          <span>正在思考…</span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <div v-if="selectedText" class="selection-chip">
        当前选中：{{ selectedText }}
      </div>

      <el-input
        v-model="inputMessage"
        type="textarea"
        :rows="4"
        resize="none"
        placeholder="结合当前文章向 AI 提问，例如：这段想表达什么？"
        @keyup.enter.ctrl="sendMessage()"
      />

      <el-button
        type="primary"
        :loading="sending"
        :disabled="booting || !article"
        class="send-button"
        @click="sendMessage()"
      >
        发送
      </el-button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { aiChatApi } from '@/api'
import type { AIChatMessage, AIChatSession, ArticleDetail } from '@/types'

const props = defineProps<{
  article: ArticleDetail | null
  selectedText?: string
  selectedContext?: string
}>()

const currentSession = ref<AIChatSession | null>(null)
const messages = ref<AIChatMessage[]>([])
const inputMessage = ref('')
const booting = ref(false)
const sending = ref(false)
const messagesRef = ref<HTMLDivElement>()

const quickPrompts = computed(() => (
  props.selectedText
    ? ['这句是什么意思？', '这里用了什么典故？', '帮我翻译这句']
    : ['概括这篇文章主旨', '这篇文章的写作特点是什么？', '作者为何这样写？']
))

const visibleMessages = computed(() => {
  return messages.value.filter(message => message.role !== 'system')
})

const contextHint = computed(() => {
  if (props.selectedText) {
    return `会优先结合当前选中的内容：${truncate(props.selectedText, 18)}`
  }

  return 'AI 会自动参考当前文章内容，聊天记录会持久化保存'
})

const truncate = (text: string, length: number) => {
  return text.length > length ? `${text.slice(0, length)}…` : text
}

const formatMessage = (content: string) => {
  return content
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

const loadSession = async (articleId: number) => {
  booting.value = true

  try {
    currentSession.value = await aiChatApi.getArticleSession(articleId)
    messages.value = await aiChatApi.getMessages(currentSession.value.id)
  } catch (error) {
    console.error('加载 AI 会话失败:', error)
    ElMessage.error('恢复问答记录失败')
  } finally {
    booting.value = false
    await scrollToBottom()
  }
}

const sendMessage = async (presetMessage?: string) => {
  const content = (presetMessage ?? inputMessage.value).trim()
  if (!content || sending.value || !currentSession.value) {
    return
  }

  sending.value = true

  try {
    const responseMessages = await aiChatApi.sendMessage(currentSession.value.id, {
      content,
      selected_text: props.selectedText?.trim() || undefined,
      selected_text_context: props.selectedContext?.trim() || undefined
    })

    messages.value.push(...responseMessages)
    inputMessage.value = ''
  } catch (error) {
    console.error('发送消息失败:', error)
    ElMessage.error('发送失败，请稍后重试')
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}

watch(messages, () => {
  void scrollToBottom()
}, { deep: true })

watch(() => props.article?.id, (articleId) => {
  messages.value = []
  currentSession.value = null
  inputMessage.value = ''

  if (articleId) {
    void loadSession(articleId)
  }
}, { immediate: true })
</script>

<style scoped lang="scss">
.article-ai-panel {
  width: 420px;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #ebeef5;
  background: #fff;
}

.panel-header {
  padding: 20px 20px 12px;
  border-bottom: 1px solid #ebeef5;

  h3 {
    margin: 0 0 6px;
    font-size: 18px;
  }

  p {
    margin: 0;
    color: #909399;
    line-height: 1.6;
    font-size: 13px;
  }
}

.quick-prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.prompt-button {
  padding: 6px 10px;
  border-radius: 999px;
  background: #f5f7fa;
  color: #606266;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #fafafa;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 120px;
  color: #606266;
}

.message {
  display: flex;
  margin-bottom: 14px;

  &.user {
    justify-content: flex-end;
  }

  &.user .message-content {
    background: #409eff;
    color: #fff;
    border-radius: 14px 14px 4px 14px;
  }

  &.assistant .message-content {
    background: #fff;
    color: #303133;
    border-radius: 14px 14px 14px 4px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
  }
}

.message-content {
  max-width: 88%;
  padding: 12px 14px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
}

.input-area {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  background: #fff;
}

.selection-chip {
  margin-bottom: 12px;
  padding: 8px 10px;
  border-radius: 10px;
  background: #f5f7fa;
  color: #606266;
  font-size: 13px;
}

.send-button {
  width: 100%;
  margin-top: 12px;
}
</style>
