import api from './index'

export interface ChatSession {
  id: number
  session_type: string
  article_id?: number
  title?: string
  message_count: number
  created_at: string
  updated_at?: string
}

export interface ChatMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  selected_text?: string
  created_at: string
}

export interface ChatMessageCreate {
  content: string
  selected_text?: string
  selected_text_context?: string
}

export const aiChatApi = {
  // 获取会话列表
  getSessions(userId: string = 'anonymous', sessionType?: string) {
    return api.get<ChatSession[]>('/ai-chat/sessions', {
      params: { user_id: userId, session_type: sessionType }
    })
  },

  // 创建会话
  createSession(data: {
    session_type?: string
    article_id?: number
    title?: string
  }, userId: string = 'anonymous') {
    return api.post<ChatSession>('/ai-chat/sessions', data, {
      params: { user_id: userId }
    })
  },

  // 获取会话详情
  getSession(sessionId: number, userId: string = 'anonymous') {
    return api.get<ChatSession>(`/ai-chat/sessions/${sessionId}`, {
      params: { user_id: userId }
    })
  },

  // 删除会话
  deleteSession(sessionId: number, userId: string = 'anonymous') {
    return api.delete<{ message: string }>(`/ai-chat/sessions/${sessionId}`, {
      params: { user_id: userId }
    })
  },

  // 获取消息列表
  getMessages(sessionId: number, userId: string = 'anonymous') {
    return api.get<ChatMessage[]>(`/ai-chat/sessions/${sessionId}/messages`, {
      params: { user_id: userId }
    })
  },

  // 发送消息
  sendMessage(sessionId: number, data: ChatMessageCreate, userId: string = 'anonymous') {
    return api.post<ChatMessage[]>(`/ai-chat/sessions/${sessionId}/messages`, data, {
      params: { user_id: userId }
    })
  },

  // 快速提问（不保存会话）
  quickAsk(question: string, articleId?: number, selectedText?: string) {
    return api.post<{ answer: string; selected_text?: string }>('/ai-chat/quick-ask', {
      question,
      article_id: articleId,
      selected_text: selectedText
    })
  }
}
