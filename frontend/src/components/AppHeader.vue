<template>
  <header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo">
        <el-icon :size="28" color="#409eff"><Collection /></el-icon>
        <span class="logo-text">找到古籍</span>
      </router-link>
    </div>
    
    <div class="header-center">
      <el-input
        v-model="searchQuery"
        placeholder="搜索文章、作者..."
        class="search-input"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
    
    <div class="header-right">
      <el-button type="primary" @click="goToAIChat">
        <el-icon><ChatDotRound /></el-icon>
        AI 选书
      </el-button>
      <el-button @click="goToFavorites">
        <el-icon><Star /></el-icon>
        收藏
      </el-button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/library',
      query: { search: searchQuery.value }
    })
  }
}

const goToAIChat = () => {
  router.push('/ai-chat')
}

const goToFavorites = () => {
  router.push('/favorites')
}
</script>

<style scoped lang="scss">
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
}

.header-left {
  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    
    .logo-text {
      font-size: 20px;
      font-weight: 600;
      color: #333;
    }
  }
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 24px;
  
  .search-input {
    :deep(.el-input__wrapper) {
      border-radius: 20px;
    }
  }
}

.header-right {
  display: flex;
  gap: 12px;
}
</style>
