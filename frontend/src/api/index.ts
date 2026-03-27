import axios from 'axios'
import type { AxiosInstance } from 'axios'
import type {
  Response,
  ListResponse,
  Article,
  ArticleDetail,
  Dynasty,
  Author,
  AuthorWithDynasty,
  KnowledgePoint,
  ExplainResult,
  VocabularyEntry,
  AIChatSession,
  AIChatMessage
} from '@/types'

const CLIENT_ID_STORAGE_KEY = 'guji-client-id'

const getClientId = () => {
  if (typeof window === 'undefined') {
    return 'anonymous'
  }

  const existingId = localStorage.getItem(CLIENT_ID_STORAGE_KEY)
  if (existingId) {
    return existingId
  }

  const generatedId = typeof crypto !== 'undefined' && 'randomUUID' in crypto
    ? crypto.randomUUID()
    : `guji-${Date.now()}-${Math.random().toString(16).slice(2)}`

  localStorage.setItem(CLIENT_ID_STORAGE_KEY, generatedId)
  return generatedId
}

// 创建 axios 实例
const instance: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

instance.interceptors.request.use((config) => {
  const headers = config.headers ?? {}
  headers['X-User-Id'] = getClientId()
  config.headers = headers
  return config
})

// 响应拦截器：解包 {code, message, data} 直接返回 data
instance.interceptors.response.use(
  (response) => {
    const body = response.data as Response<any>
    if (body.code !== 200) {
      throw new Error(body.message)
    }
    return body.data as any
  },
  (error) => {
    console.error('API Error:', error)
    throw error
  }
)

// 类型安全的请求包装
const api = {
  async get<T>(url: string, config?: any): Promise<T> {
    return instance.get(url, config) as any
  },
  async post<T>(url: string, data?: any, config?: any): Promise<T> {
    return instance.post(url, data, config) as any
  },
  async put<T>(url: string, data?: any, config?: any): Promise<T> {
    return instance.put(url, data, config) as any
  },
  async delete<T>(url: string, config?: any): Promise<T> {
    return instance.delete(url, config) as any
  }
}

// 文章相关 API
export const articleApi = {
  // 获取文章列表
  getArticles(params: {
    page?: number
    page_size?: number
    dynasty_id?: number
    author_id?: number
    category?: string
    is_selected?: boolean
  } = {}) {
    return api.get<ListResponse<Article>>('/articles', { params })
  },

  // 搜索文章
  searchArticles(q: string, page = 1, page_size = 20) {
    return api.get<ListResponse<Article>>('/articles/search', {
      params: { q, page, page_size }
    })
  },

  // 获取文章详情
  getArticle(id: number) {
    return api.get<ArticleDetail>(`/articles/${id}`)
  },

  // 获取文章知识点
  getKnowledgePoints(id: number) {
    return api.get<KnowledgePoint[]>(`/articles/${id}/knowledge`)
  }
}

// 朝代相关 API
export const dynastyApi = {
  // 获取所有朝代
  getDynasties() {
    return api.get<Dynasty[]>('/dynasties')
  },

  // 获取朝代详情
  getDynasty(id: number) {
    return api.get<Dynasty>(`/dynasties/${id}`)
  },

  // 获取朝代下的作者
  getDynastyAuthors(id: number) {
    return api.get<Author[]>(`/dynasties/${id}/authors`)
  }
}

// 作者相关 API
export const authorApi = {
  // 获取作者列表
  getAuthors(params: {
    page?: number
    page_size?: number
    dynasty_id?: number
  } = {}) {
    return api.get<ListResponse<AuthorWithDynasty>>('/authors', { params })
  },

  // 获取作者详情
  getAuthor(id: number) {
    return api.get<AuthorWithDynasty>(`/authors/${id}`)
  },

  // 获取作者的文章
  getAuthorArticles(id: number) {
    return api.get<Article[]>(`/authors/${id}/articles`)
  }
}

// AI 相关 API
export const aiApi = {
  // 与 AI 对话
  chat(messages: { role: string; content: string }[], temperature = 0.7) {
    return api.post<string>('/ai/chat', { messages, temperature })
  },

  // 翻译古文
  translate(text: string) {
    return api.post<string>('/ai/translate', { text })
  },

  // 解释词语/句子
  explain(text: string, context?: string) {
    return api.post<string>('/ai/explain', { text, context })
  },

  // AI 推荐文章
  selectArticles(userInput: string) {
    return api.post<{
      recommendations: { article_index: number; reason: string }[]
      summary: string
      raw_response?: string
    }>('/ai/select-articles', { user_input: userInput })
  },

  // 生成知识点
  generateKnowledge(articleId: number) {
    return api.post<Array<{
      type: string
      content: string
      explanation?: string
    }>>(`/ai/generate-knowledge/${articleId}`)
  }
}

export const wordbookApi = {
  getEntries(params: {
    article_id?: number
    page?: number
    page_size?: number
  } = {}) {
    return api.get<ListResponse<VocabularyEntry>>('/vocabulary', { params })
  },

  createEntry(data: {
    word: string
    pinyin?: string
    explanation: string
    source_text?: string
    article_id: number
  }) {
    return api.post<VocabularyEntry>('/vocabulary', data)
  },

  deleteEntry(id: number) {
    return api.delete<{ message: string }>(`/vocabulary/${id}`)
  },

  reviewEntry(id: number) {
    return api.post<VocabularyEntry>(`/vocabulary/${id}/review`)
  },

  explainSelection(text: string, context?: string) {
    return api.post<ExplainResult>('/vocabulary/explain', { text, context })
  }
}

export const aiChatApi = {
  getArticleSession(articleId: number) {
    return api.get<AIChatSession>('/ai-chat/article-session', {
      params: { article_id: articleId }
    })
  },

  getSessions(params: {
    session_type?: string
    article_id?: number
  } = {}) {
    return api.get<AIChatSession[]>('/ai-chat/sessions', { params })
  },

  createSession(data: {
    session_type?: string
    article_id?: number
    title?: string
  }) {
    return api.post<AIChatSession>('/ai-chat/sessions', data)
  },

  getMessages(sessionId: number) {
    return api.get<AIChatMessage[]>(`/ai-chat/sessions/${sessionId}/messages`)
  },

  sendMessage(sessionId: number, data: {
    content: string
    selected_text?: string
    selected_text_context?: string
  }) {
    return api.post<AIChatMessage[]>(`/ai-chat/sessions/${sessionId}/messages`, data)
  }
}

// 导出相关 API
export const exportApi = {
  // 导出 PDF
  async exportPDF(articleIds: number[], includeTranslation = true, includeKnowledge = true): Promise<Blob> {
    const response = await instance.post('/export/pdf', {
      article_ids: articleIds,
      include_translation: includeTranslation,
      include_knowledge: includeKnowledge
    }, {
      responseType: 'blob'
    })
    return response.data as Blob
  }
}

export default api
