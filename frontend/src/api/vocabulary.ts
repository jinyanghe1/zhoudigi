import api from './index'
import type { ExplainResult, ListResponse, VocabularyEntry } from '@/types'

export interface Vocabulary extends VocabularyEntry {}

export interface VocabularyCreate {
  word: string
  pinyin?: string
  explanation: string
  source_text?: string
  article_id: number
}

export interface VocabularyUpdate {
  pinyin?: string
  explanation?: string
  mastery_level?: number
}

export interface TextExplanation extends ExplainResult {}

export const vocabularyApi = {
  // 获取生词列表
  getList(params: {
    article_id?: number
    page?: number
    page_size?: number
  } = {}) {
    return api.get<ListResponse<Vocabulary>>('/vocabulary', { params })
  },

  // 添加生词
  create(data: VocabularyCreate) {
    return api.post<Vocabulary>('/vocabulary', data)
  },

  // 获取生词详情
  getDetail(id: number) {
    return api.get<Vocabulary>(`/vocabulary/${id}`)
  },

  // 更新生词
  update(id: number, data: VocabularyUpdate) {
    return api.put<Vocabulary>(`/vocabulary/${id}`, data)
  },

  // 删除生词
  delete(id: number) {
    return api.delete<{ message: string }>(`/vocabulary/${id}`)
  },

  // 复习生词
  review(id: number) {
    return api.post<Vocabulary>(`/vocabulary/${id}/review`)
  },

  // 解释选中文本
  explain(text: string, context?: string) {
    return api.post<TextExplanation>('/vocabulary/explain', { text, context })
  }
}
