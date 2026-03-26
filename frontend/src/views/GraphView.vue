<template>
  <div class="graph-view">
    <h1 class="page-title">知识图谱</h1>
    
    <div class="graph-tabs">
      <el-radio-group v-model="graphType" size="large">
        <el-radio-button label="dynasty">朝代脉络</el-radio-button>
        <el-radio-button label="author">文人关系</el-radio-button>
        <el-radio-button label="style">风格分类</el-radio-button>
      </el-radio-group>
    </div>
    
    <div class="graph-container">
      <div ref="chartRef" class="chart"></div>
    </div>
    
    <div class="graph-legend">
      <div class="legend-item">
        <span class="legend-dot dynasty"></span>
        <span>朝代</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot author"></span>
        <span>作者</span>
      </div>
      <div class="legend-item">
        <span class="legend-dot article"></span>
        <span>文章</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { dynastyApi, authorApi, articleApi } from '@/api'

const chartRef = ref<HTMLDivElement>()
const chart = ref<echarts.ECharts>()
const graphType = ref('dynasty')

const initChart = () => {
  if (!chartRef.value) return
  
  chart.value = echarts.init(chartRef.value)
  
  window.addEventListener('resize', () => {
    chart.value?.resize()
  })
}

const loadDynastyGraph = async () => {
  const [dynasties, authors] = await Promise.all([
    dynastyApi.getDynasties(),
    authorApi.getAuthors({ page_size: 100 })
  ])
  
  const nodes: any[] = []
  const links: any[] = []
  
  // 添加朝代节点
  dynasties.forEach((d, i) => {
    nodes.push({
      id: `dynasty-${d.id}`,
      name: d.name,
      symbolSize: 50,
      category: 0,
      itemStyle: { color: '#409eff' }
    })
  })
  
  // 添加作者节点和连接
  authors.items.forEach(a => {
    nodes.push({
      id: `author-${a.id}`,
      name: a.name,
      symbolSize: 30,
      category: 1,
      itemStyle: { color: '#67c23a' }
    })
    
    if (a.dynasty_id) {
      links.push({
        source: `dynasty-${a.dynasty_id}`,
        target: `author-${a.id}`
      })
    }
  })
  
  updateChart(nodes, links)
}

const updateChart = (nodes: any[], links: any[]) => {
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}'
    },
    series: [{
      type: 'graph',
      layout: 'force',
      data: nodes,
      links: links,
      roam: true,
      label: {
        show: true,
        position: 'bottom'
      },
      force: {
        repulsion: 300,
        edgeLength: 100
      },
      emphasis: {
        focus: 'adjacency'
      }
    }]
  }
  
  chart.value?.setOption(option)
}

watch(graphType, async (type) => {
  if (type === 'dynasty') {
    await loadDynastyGraph()
  }
})

onMounted(() => {
  initChart()
  loadDynastyGraph()
})
</script>

<style scoped lang="scss">
.graph-view {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 24px;
}

.graph-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.graph-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 24px;
}

.chart {
  width: 100%;
  height: 600px;
}

.graph-legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 24px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  
  &.dynasty { background: #409eff; }
  &.author { background: #67c23a; }
  &.article { background: #e6a23c; }
}
</style>
