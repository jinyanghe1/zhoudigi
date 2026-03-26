<template>
  <div class="app-container">
    <AppHeader />
    <div class="main-content">
      <SideMenu v-if="showMenu" />
      <div class="page-content" :class="{ 'full-width': !showMenu }">
        <router-view />
      </div>
    </div>
    <AIChatButton />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import SideMenu from './components/SideMenu.vue'
import AIChatButton from './components/AIChatButton.vue'

const route = useRoute()

// 阅读页面不显示侧边菜单
const showMenu = computed(() => {
  return !route.path.startsWith('/article/')
})
</script>

<style scoped lang="scss">
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.main-content {
  flex: 1;
  display: flex;
  padding-top: 60px;
}

.page-content {
  flex: 1;
  padding: 24px;
  margin-left: 220px;
  transition: margin-left 0.3s;
  
  &.full-width {
    margin-left: 0;
    padding: 0;
  }
}
</style>
