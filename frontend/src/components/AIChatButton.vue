<template>
  <div class="ai-chat-wrapper">
    <el-button
      v-if="!isOpen"
      class="chat-toggle-btn"
      type="primary"
      circle
      size="large"
      @click="isOpen = true"
    >
      <el-icon :size="24"><ChatDotRound /></el-icon>
    </el-button>
    
    <div v-else class="chat-panel">
      <div class="chat-header">
        <span class="chat-title">
          <el-icon><ChatDotRound /></el-icon>
          AI 古文助手
        </span>
        <el-button type="text" @click="isOpen = false">
          <el-icon><Close /></el-icon>
        </el-button>
      </div>
      
      <div class="chat-messages" ref="messagesRef">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="message"
          :class="msg.role"
        >
          <div class="message-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="message-content">
            <el-icon class="loading-icon"><Loading /></el-icon>
            思考中...
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="2"
          placeholder="输入你想了解的内容，比如：推荐几篇关于山水的古文"
          @keyup.enter.ctrl="sendMessage"
        />
        <el-button
          type="primary"
          :loading="loading"
          @click="sendMessage"
          class="send-btn"
        >
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue'
import { aiApi } from '@/api'
import type { ChatMessage } from '@/types'

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref<ChatMessage[]>([
  {
    role: 'assistant',
    content: '你好！我是你的古文助手。告诉我你想读什么类型的文章，我来帮你推荐！'
  }
])
const loading = ref(false)
const messagesRef = ref<HTMLDivElement>()

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

watch(messages, scrollToBottom, { deep: true })

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return
  
  const userMessage = inputMessage.value.trim()
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  
  try {
    const response = await aiApi.chat([
      {
        role: 'system',
        content: '你是一个古文专家，熟悉中国历代文学作品。请根据用户的需求，推荐合适的古文，并解释推荐原因。回答要简洁明了。'
      },
      ...messages.value.slice(-6).map(m => ({ role: m.role, content: m.content }))
    ])
    
    messages.value.push({ role: 'assistant', content: response })
  } catch (error) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，服务暂时不可用，请稍后重试。'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.ai-chat-wrapper {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 999;
}

.chat-toggle-btn {
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.chat-panel {
  width: 380px;
  height: 500px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #ebeef5;
  background: linear-gradient(135deg, #409eff, #67c23a);
  color: #fff;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f7fa;
}

.message {
  margin-bottom: 12px;
  display: flex;
  
  &.user {
    justify-content: flex-end;
    
    .message-content {
      background: #409eff;
      color: #fff;
      border-radius: 12px 12px 2px 12px;
    }
  }
  
  &.assistant {
    justify-content: flex-start;
    
    .message-content {
      background: #fff;
      color: #333;
      border-radius: 12px 12px 12px 2px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
  }
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.loading-icon {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #ebeef5;
  background: #fff;
  
  .send-btn {
    margin-top: 8px;
    width: 100%;
  }
}
</style>
