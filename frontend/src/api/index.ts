import axios from 'axios'
import type { AxiosResponse } from 'axios'
import type { Response, ListResponse, Article, ArticleDetail, Dynasty, Author, AuthorWithDynasty, KnowledgePoint } from '@/types'

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
api.interceptors.response.use(
  (response: AxiosResponse<Response<any>>) => {
    if (response.data.code !== 200) {
      throw new Error(response.data.message)
    }
    return response.data.data
  },
  (error) => {
    console.error('API Error:', error)
    throw error
  }
)

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

// 导出相关 API
export const exportApi = {
  // 导出 PDF
  exportPDF(articleIds: number[], includeTranslation = true, includeKnowledge = true) {
    return api.post('/export/pdf', {
      article_ids: articleIds,
      include_translation: includeTranslation,
      include_knowledge: includeKnowledge
    }, {
      responseType: 'blob'
    })
  }
}

export default api
