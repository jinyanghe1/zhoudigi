<template>
  <div class="ai-chat-view">
    <div class="chat-container">
      <div class="chat-sidebar">
        <h2 class="sidebar-title">AI 古文助手</h2>
        <p class="sidebar-desc">
          告诉 AI 你想读什么类型的古文，它会为你推荐合适的文章
        </p>
        
        <div class="quick-prompts">
          <div class="prompt-title">快速提问</div>
          <el-button
            v-for="prompt in quickPrompts"
            :key="prompt"
            text
            class="prompt-btn"
            @click="usePrompt(prompt)"
          >
            {{ prompt }}
          </el-button>
        </div>
      </div>
      
      <div class="chat-main">
        <div class="messages-container" ref="messagesRef">
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message"
            :class="msg.role"
          >
            <div class="message-avatar">
              <el-avatar
                :size="40"
                :icon="msg.role === 'user' ? UserFilled : ChatDotRound"
                :class="msg.role"
              />
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(msg.content)"></div>
              
              <!-- 推荐结果 -->
              <div v-if="msg.recommendations" class="recommendations">
                <div
                  v-for="rec in msg.recommendations"
                  :key="rec.article_id"
                  class="rec-item"
                  @click="goToArticle(rec.article_id)"
                >
                  <div class="rec-title">{{ rec.title }}</div>
                  <div class="rec-reason">{{ rec.reason }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="loading" class="message assistant">
            <div class="message-avatar">
              <el-avatar :size="40" :icon="ChatDotRound" class="assistant" />
            </div>
            <div class="message-content">
              <el-icon class="loading-icon"><Loading /></el-icon>
              正在思考...
            </div>
          </div>
        </div>
        
        <div class="chat-input-area">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="输入你想了解的内容，比如：推荐几篇关于山水的古文"
            @keyup.enter.ctrl="sendMessage"
          />
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="sendMessage"
            class="send-btn"
          >
            <el-icon><Promotion /></el-icon>
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { aiApi } from '@/api'
import { UserFilled, ChatDotRound, Loading, Promotion } from '@element-plus/icons-vue'

const router = useRouter()

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  recommendations?: Array<{
    article_id: number
    title: string
    reason: string
  }>
}

const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '你好！我是你的古文助手。告诉我你想读什么类型的文章，我来帮你推荐！比如你可以说：\n\n• "推荐几篇关于山水的古文"\n• "我想读一些励志的文章"\n• "介绍几篇先秦散文"'
  }
])

const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref<HTMLDivElement>()

const quickPrompts = [
  '推荐几篇关于友情的文章',
  '我想读一些描写秋天的古文',
  '介绍几位唐宋八大家的代表作',
  '推荐几篇励志的文章',
  '我想了解一些关于学习的古文'
]

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

const usePrompt = (prompt: string) => {
  inputMessage.value = prompt
}

const formatMessage = (content: string) => {
  // 简单的 Markdown 格式化
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return
  
  const userMessage = inputMessage.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  await scrollToBottom()
  
  try {
    // 调用 AI 选文接口
    const result = await aiApi.selectArticles(userMessage)
    
    let responseText = result.summary || ''
    let recommendations = undefined
    
    // 解析推荐结果
    if (result.recommendations && result.recommendations.length > 0) {
      recommendations = result.recommendations.map((rec: any) => ({
        article_id: rec.article_id || rec.article_index,
        title: `推荐文章 ${rec.article_index}`,
        reason: rec.reason
      }))
      
      responseText += '\n\n我为你推荐以下文章：'
    }
    
    messages.value.push({
      role: 'assistant',
      content: responseText,
      recommendations
    })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，服务暂时不可用，请稍后重试。'
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

const goToArticle = (id: number) => {
  router.push(`/article/${id}`)
}
</script>

<style scoped lang="scss">
.ai-chat-view {
  height: calc(100vh - 84px);
  display: flex;
  flex-direction: column;
}

.chat-container {
  flex: 1;
  display: flex;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.chat-sidebar {
  width: 300px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 32px;
  display: flex;
  flex-direction: column;
}

.sidebar-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
}

.sidebar-desc {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.6;
  margin-bottom: 32px;
}

.quick-prompts {
  flex: 1;
}

.prompt-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.7;
  margin-bottom: 12px;
}

.prompt-btn {
  display: block;
  width: 100%;
  text-align: left;
  color: #fff;
  margin-bottom: 8px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f5f7fa;
}

.message {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  
  &.user {
    flex-direction: row-reverse;
    
    .message-content {
      background: #409eff;
      color: #fff;
      border-radius: 12px 12px 2px 12px;
    }
  }
  
  &.assistant {
    .message-content {
      background: #fff;
      border-radius: 12px 12px 12px 2px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
  }
}

.message-avatar {
  .el-avatar {
    &.user {
      background: #409eff;
    }
    
    &.assistant {
      background: #67c23a;
    }
  }
}

.message-content {
  max-width: 70%;
  padding: 16px 20px;
  font-size: 15px;
  line-height: 1.7;
}

.message-text {
  white-space: pre-wrap;
}

.recommendations {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rec-item {
  background: #f5f7fa;
  padding: 12px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: #ecf5ff;
  }
}

.rec-title {
  font-weight: 600;
  color: #409eff;
  margin-bottom: 4px;
}

.rec-reason {
  font-size: 13px;
  color: #666;
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.chat-input-area {
  padding: 20px 24px;
  border-top: 1px solid #ebeef5;
  background: #fff;
  display: flex;
  gap: 16px;
  align-items: flex-end;
}

.send-btn {
  flex-shrink: 0;
}
</style>
