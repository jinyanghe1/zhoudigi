<template>
  <aside class="side-menu">
    <el-menu
      :default-active="activeMenu"
      router
      class="menu"
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        <span>首页推荐</span>
      </el-menu-item>
      
      <el-sub-menu index="/library">
        <template #title>
          <el-icon><Collection /></el-icon>
          <span>书库浏览</span>
        </template>
        <el-menu-item index="/library/dynasty">
          <el-icon><Histogram /></el-icon>
          <span>按朝代</span>
        </el-menu-item>
        <el-menu-item index="/library/author">
          <el-icon><UserFilled /></el-icon>
          <span>按作者</span>
        </el-menu-item>
      </el-sub-menu>
      
      <el-menu-item index="/graph">
        <el-icon><Share /></el-icon>
        <span>知识图谱</span>
      </el-menu-item>
      
      <el-menu-item index="/favorites">
        <el-icon><StarFilled /></el-icon>
        <span>我的收藏</span>
      </el-menu-item>
      
      <el-divider />
      
      <div class="menu-section-title">精选文章</div>
      <el-menu-item 
        v-for="article in featuredArticles" 
        :key="article.id"
        :index="`/article/${article.id}`"
      >
        <span class="featured-title">{{ article.title }}</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { articleApi } from '@/api'
import type { Article } from '@/types'

const route = useRoute()
const featuredArticles = ref<Article[]>([])

const activeMenu = computed(() => route.path)

const loadFeaturedArticles = async () => {
  try {
    const res = await articleApi.getArticles({ 
      is_selected: true, 
      page_size: 5 
    })
    featuredArticles.value = res.items
  } catch (error) {
    console.error('加载精选文章失败:', error)
  }
}

onMounted(loadFeaturedArticles)
</script>

<style scoped lang="scss">
.side-menu {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  width: 220px;
  background: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.menu {
  border-right: none;
  padding: 16px 0;
}

.menu-section-title {
  padding: 8px 20px;
  font-size: 12px;
  color: #909399;
  font-weight: 500;
}

.featured-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
