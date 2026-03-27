import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/library',
    name: 'Library',
    component: () => import('../views/LibraryView.vue'),
    meta: { title: '书库' }
  },
  {
    path: '/library/dynasty',
    name: 'LibraryByDynasty',
    component: () => import('../views/LibraryByDynastyView.vue'),
    meta: { title: '按朝代浏览' }
  },
  {
    path: '/library/author',
    name: 'LibraryByAuthor',
    component: () => import('../views/LibraryByAuthorView.vue'),
    meta: { title: '按作者浏览' }
  },
  {
    path: '/article/:id',
    name: 'Article',
    component: () => import('../views/ArticleView.vue'),
    meta: { title: '文章阅读' }
  },
  {
    path: '/graph',
    name: 'Graph',
    component: () => import('../views/GraphView.vue'),
    meta: { title: '知识图谱' }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('../views/FavoritesView.vue'),
    meta: { title: '我的收藏' }
  },
  {
    path: '/vocabulary',
    redirect: '/wordbook'
  },
  {
    path: '/wordbook',
    name: 'Wordbook',
    component: () => import('../views/WordbookView.vue'),
    meta: { title: '生词库' }
  },
  {
    path: '/ai-chat',
    name: 'AIChat',
    component: () => import('../views/AIChatView.vue'),
    meta: { title: 'AI 助手' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 找到古籍`
  }
  next()
})

export default router
