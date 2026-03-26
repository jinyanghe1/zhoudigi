// 通用响应类型
export interface Response<T> {
  code: number
  message: string
  data: T
}

export interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

export interface ListResponse<T> {
  items: T[]
  pagination: Pagination
}

// 朝代
export interface Dynasty {
  id: number
  name: string
  period?: string
  description?: string
  created_at: string
}

// 作者
export interface Author {
  id: number
  name: string
  dynasty_id?: number
  bio?: string
  literary_group?: string
  style?: string
  created_at: string
}

export interface AuthorWithDynasty extends Author {
  dynasty?: Dynasty
}

// 标签
export interface Tag {
  id: number
  name: string
  category?: string
  created_at: string
}

// 知识点
export interface KnowledgePoint {
  id: number
  article_id: number
  type: 'vocab' | 'background' | 'analysis'
  content: string
  explanation?: string
  position_start?: number
  position_end?: number
  created_at: string
}

// 文章
export interface Article {
  id: number
  title: string
  author_id?: number
  content: string
  translation?: string
  dynasty_id?: number
  category?: string
  source?: string
  is_selected: boolean
  selection_reason?: string
  read_count: number
  word_count?: number
  created_at: string
  updated_at?: string
}

export interface ArticleDetail extends Article {
  author?: AuthorWithDynasty
  knowledge_points: KnowledgePoint[]
  tags: Tag[]
}

// AI 对话
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}
