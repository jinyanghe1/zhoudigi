<template>
  <div class="ai-chat-sidebar" :class="{ 'collapsed': collapsed }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <div class="header-title">
        <el-icon><ChatDotRound /></el-icon>
        <span>问 AI</span>
      </div>
      <div class="header-actions">
        <el-button type="text" @click="createNewSession" title="新对话">
          <el-icon><Plus /></el-icon>
        </el-button>
        <el-button type="text" @click="toggleCollapse" title="收起/展开">
          <el-icon><ArrowRight v-if="collapsed" /><ArrowLeft v-else /></el-icon>
        </el-button>
      </div>
    </div>
    
    <!-- 会话列表（展开时显示） -->
    <div v-if="!collapsed" class="session-list">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="session-item"
        :class="{ active: currentSession?.id === session.id }"
        @click="switchSession(session)"
      >
        <div class="session-title">{{ session.title }}</div>
        <div class="session-meta">{{ session.message_count }} 条消息</div>
        <el-button
          class="delete-btn"
          type="text"
          size="small"
          @click.stop="deleteSession(session.id)"
        >
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
    </div>
    
    <!-- 聊天区域 -->
    <div v-if="!collapsed" class="chat-area">
      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesRef">
        <div v-if="messages.length === 0" class="empty-chat">
          <el-empty description="开始对话吧">
            <template #description>
              <p>选中文字可以针对特定内容提问</p>
              <p>也可以自由讨论文章内容</p>
            </template>
          </el-empty>
        </div>
        
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="message"
          :class="msg.role"
        >
          <div class="message-avatar">
            <el-avatar
              :size="32"
              :icon="msg.role === 'user' ? UserFilled : ChatDotRound"
              :class="msg.role"
            />
          </div>
          <div class="message-content">
            <div v-if="msg.selected_text" class="selected-context">
              引用：{{ msg.selected_text.slice(0, 50) }}...
            </div>
            <div class="message-text">{{ msg.content }}</div>
          </div>
        </div>
        
        <div v-if="loading" class="message assistant">
          <div class="message-avatar">
            <el-avatar :size="32" :icon="ChatDotRound" class="assistant" />
          </div>
          <div class="message-content">
            <el-icon class="loading-icon"><Loading /></el-icon>
            思考中...
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-area">
        <div v-if="selectedText" class="selected-hint">
          针对选中的文字提问：{{ selectedText.slice(0, 30) }}...
          <el-button type="text" size="small" @click="clearSelection">清除</el-button>
        </div>
        <div class="input-row">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="2"
            placeholder="输入你的问题..."
            @keyup.enter.ctrl="sendMessage"
          />
          <el-button
            type="primary"
            :loading="loading"
            @click="sendMessage"
            class="send-btn"
          >
            <el-icon><Promotion /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
    
    <!-- 收起时的按钮 -->
    <div v-else class="collapsed-btn" @click="toggleCollapse">
      <el-icon><ChatDotRound /></el-icon>
      <span>问 AI</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ChatDotRound,
  Plus,
  ArrowRight,
  ArrowLeft,
  Close,
  UserFilled,
  Loading,
  Promotion
} from '@element-plus/icons-vue'
import { aiChatApi } from '@/api/aiChat'
import type { ChatSession, ChatMessage } from '@/api/aiChat'

interface Props {
  articleId: number
  articleTitle?: string
  selectedText?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'clear-selection': []
}>()

const collapsed = ref(false)
const sessions = ref<ChatSession[]>([])
const currentSession = ref<ChatSession | null>(null)
const messages = ref<ChatMessage[]>([])
const inputMessage = ref('')
const loading = ref(false)
const messagesRef = ref<HTMLDivElement>()

// 切换折叠状态
const toggleCollapse = () => {
  collapsed.value = !collapsed.value
}

// 加载会话列表
const loadSessions = async () => {
  try {
    const res = await aiChatApi.getSessions()
    sessions.value = res
    
    // 如果有会话，默认选中第一个
    if (res.length > 0 && !currentSession.value) {
      await switchSession(res[0])
    }
  } catch (error) {
    console.error('加载会话失败:', error)
  }
}

// 创建新会话
const createNewSession = async () => {
  try {
    const res = await aiChatApi.createSession({
      session_type: 'reading',
      article_id: props.articleId,
      title: `关于《${props.articleTitle || '古文'}》的讨论`
    })
    sessions.value.unshift(res)
    await switchSession(res)
    ElMessage.success('创建新对话')
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

// 切换会话
const switchSession = async (session: ChatSession) => {
  currentSession.value = session
  try {
    const res = await aiChatApi.getMessages(session.id)
    messages.value = res
    scrollToBottom()
  } catch (error) {
    console.error('加载消息失败:', error)
  }
}

// 删除会话
const deleteSession = async (sessionId: number) => {
  try {
    await ElMessageBox.confirm('确定删除这个对话吗？', '提示', {
      type: 'warning'
    })
    await aiChatApi.deleteSession(sessionId)
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
    if (currentSession.value?.id === sessionId) {
      currentSession.value = null
      messages.value = []
    }
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  if (!currentSession.value) {
    // 如果没有会话，先创建一个
    await createNewSession()
  }
  
  loading.value = true
  try {
    const res = await aiChatApi.sendMessage(
      currentSession.value!.id,
      {
        content: inputMessage.value,
        selected_text: props.selectedText,
        selected_text_context: props.selectedText
      }
    )
    messages.value.push(...res)
    inputMessage.value = ''
    clearSelection()
    scrollToBottom()
    
    // 更新当前会话的消息数
    currentSession.value!.message_count += 2
  } catch (error) {
    ElMessage.error('发送失败')
  } finally {
    loading.value = false
  }
}

// 清除选中的文字
const clearSelection = () => {
  emit('clear-selection')
}

// 滚动到底部
const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

onMounted(() => {
  loadSessions()
})
</script>

<style scoped lang="scss">
.ai-chat-sidebar {
  width: 380px;
  background: #fff;
  border-left: 1px solid #ebeef5;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  
  &.collapsed {
    width: 60px;
  }
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.header-actions {
  display: flex;
  gap: 4px;
}

.session-list {
  max-height: 150px;
  overflow-y: auto;
  border-bottom: 1px solid #ebeef5;
  padding: 8px 0;
}

.session-item {
  padding: 10px 16px;
  cursor: pointer;
  position: relative;
  
  &:hover,
  &.active {
    background: #f5f7fa;
  }
  
  &:hover .delete-btn {
    display: block;
  }
}

.session-title {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 24px;
}

.session-meta {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.delete-btn {
  display: none;
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.empty-chat {
  padding: 40px 0;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  
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
      background: #f5f7fa;
      border-radius: 12px 12px 12px 2px;
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
  max-width: 80%;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.6;
}

.selected-context {
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px dashed rgba(255,255,255,0.3);
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.input-area {
  padding: 16px;
  border-top: 1px solid #ebeef5;
}

.selected-hint {
  font-size: 12px;
  color: #409eff;
  margin-bottom: 8px;
  padding: 8px;
  background: #ecf5ff;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.input-row {
  display: flex;
  gap: 8px;
}

.send-btn {
  flex-shrink: 0;
}

.collapsed-btn {
  writing-mode: vertical-lr;
  text-orientation: upright;
  padding: 16px 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #409eff;
  font-weight: 500;
  
  &:hover {
    background: #f5f7fa;
  }
}
</style>
