<template>
  <div class="graph-view">
    <h1 class="page-title">知识图谱</h1>
    
    <div class="graph-tabs">
      <el-radio-group v-model="graphType" size="large" @change="loadGraphData">
        <el-radio-button label="dynasty">朝代脉络</el-radio-button>
        <el-radio-button label="style">风格分类</el-radio-button>
      </el-radio-group>
    </div>
    
    <div class="graph-container">
      <div v-if="loading" class="loading-wrapper">
        <el-skeleton :rows="10" animated />
      </div>
      <div v-else ref="chartRef" class="chart"></div>
    </div>
    
    <div class="graph-info">
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span>图谱说明</span>
          </div>
        </template>
        <div class="info-content">
          <p v-if="graphType === 'dynasty'">
            <strong>朝代脉络图</strong>展示了各朝代、作者和文章之间的层级关系。<br>
            <span class="legend-dot blue"></span> 蓝色节点：朝代<br>
            <span class="legend-dot green"></span> 绿色节点：作者<br>
            <span class="legend-dot orange"></span> 橙色节点：文章
          </p>
          <p v-else>
            <strong>风格分类图</strong>展示了不同文学风格及其代表人物。<br>
            <span class="legend-dot blue"></span> 蓝色节点：风格流派<br>
            <span class="legend-dot green"></span> 绿色节点：代表人物
          </p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLDivElement>()
const chart = ref<echarts.ECharts>()
const graphType = ref('dynasty')
const loading = ref(false)

const initChart = () => {
  if (!chartRef.value) return
  
  chart.value = echarts.init(chartRef.value)
  
  window.addEventListener('resize', handleResize)
}

const handleResize = () => {
  chart.value?.resize()
}

const loadGraphData = async () => {
  if (!chart.value) return
  
  loading.value = true
  
  try {
    // 模拟加载数据 - 实际项目中应该从后端 API 获取
    // const res = await api.get(`/graph/${graphType.value}`)
    
    // 使用模拟数据
    const data = generateMockData()
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}'
      },
      legend: {
        data: data.categories.map((a: any) => a.name),
        bottom: 20
      },
      series: [{
        type: 'graph',
        layout: 'force',
        data: data.nodes,
        links: data.links,
        categories: data.categories,
        roam: true,
        label: {
          show: true,
          position: 'bottom'
        },
        force: {
          repulsion: 300,
          edgeLength: 120
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }]
    }
    
    chart.value.setOption(option, true)
  } catch (error) {
    console.error('加载图谱失败:', error)
  } finally {
    loading.value = false
  }
}

// 模拟数据生成
const generateMockData = () => {
  if (graphType.value === 'dynasty') {
    return {
      nodes: [
        { id: '1', name: '先秦', symbolSize: 50, category: 0, value: '先秦' },
        { id: '2', name: '汉朝', symbolSize: 50, category: 0, value: '汉朝' },
        { id: '3', name: '魏晋南北朝', symbolSize: 50, category: 0, value: '魏晋南北朝' },
        { id: '4', name: '唐朝', symbolSize: 50, category: 0, value: '唐朝' },
        { id: '5', name: '宋朝', symbolSize: 50, category: 0, value: '宋朝' },
        { id: '6', name: '孔子', symbolSize: 30, category: 1, value: '孔子' },
        { id: '7', name: '孟子', symbolSize: 30, category: 1, value: '孟子' },
        { id: '8', name: '庄子', symbolSize: 30, category: 1, value: '庄子' },
        { id: '9', name: '陶渊明', symbolSize: 30, category: 1, value: '陶渊明' },
        { id: '10', name: '韩愈', symbolSize: 30, category: 1, value: '韩愈' },
        { id: '11', name: '苏轼', symbolSize: 30, category: 1, value: '苏轼' },
        { id: '12', name: '范仲淹', symbolSize: 30, category: 1, value: '范仲淹' },
        { id: '13', name: '论语', symbolSize: 20, category: 2, value: '论语' },
        { id: '14', name: '赤壁赋', symbolSize: 20, category: 2, value: '赤壁赋' },
        { id: '15', name: '岳阳楼记', symbolSize: 20, category: 2, value: '岳阳楼记' },
      ],
      links: [
        { source: '1', target: '6' },
        { source: '1', target: '7' },
        { source: '1', target: '8' },
        { source: '3', target: '9' },
        { source: '4', target: '10' },
        { source: '5', target: '11' },
        { source: '5', target: '12' },
        { source: '6', target: '13' },
        { source: '11', target: '14' },
        { source: '12', target: '15' },
      ],
      categories: [
        { name: '朝代' },
        { name: '作者' },
        { name: '文章' }
      ]
    }
  } else {
    return {
      nodes: [
        { id: '1', name: '豪放派', symbolSize: 50, category: 0, value: '豪放派' },
        { id: '2', name: '婉约派', symbolSize: 50, category: 0, value: '婉约派' },
        { id: '3', name: '哲理派', symbolSize: 50, category: 0, value: '哲理派' },
        { id: '4', name: '田园派', symbolSize: 50, category: 0, value: '田园派' },
        { id: '5', name: '苏轼', symbolSize: 30, category: 1, value: '苏轼' },
        { id: '6', name: '韩愈', symbolSize: 30, category: 1, value: '韩愈' },
        { id: '7', name: '欧阳修', symbolSize: 30, category: 1, value: '欧阳修' },
        { id: '8', name: '庄子', symbolSize: 30, category: 1, value: '庄子' },
        { id: '9', name: '孔子', symbolSize: 30, category: 1, value: '孔子' },
        { id: '10', name: '陶渊明', symbolSize: 30, category: 1, value: '陶渊明' },
      ],
      links: [
        { source: '1', target: '5' },
        { source: '1', target: '6' },
        { source: '2', target: '7' },
        { source: '3', target: '8' },
        { source: '3', target: '9' },
        { source: '4', target: '10' },
      ],
      categories: [
        { name: '风格流派' },
        { name: '代表人物' }
      ]
    }
  }
}

onMounted(() => {
  initChart()
  loadGraphData()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart.value?.dispose()
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
  margin-bottom: 24px;
}

.loading-wrapper {
  height: 600px;
  padding: 40px;
}

.chart {
  width: 100%;
  height: 600px;
}

.graph-info {
  margin-bottom: 40px;
}

.info-card {
  .card-header {
    font-weight: 600;
  }
}

.info-content {
  line-height: 2;
  
  p {
    margin: 0;
  }
}

.legend-dot {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 6px;
  
  &.blue { background: #409eff; }
  &.green { background: #67c23a; }
  &.orange { background: #e6a23c; }
}
</style>
