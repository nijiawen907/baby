<template>
  <view class="chart-container">
    <qiun-data-charts 
       type="bar"  
      :opts="opts"
      :chartData="formatChartData"
    />
  </view>
</template>

<script setup>
import { computed, defineProps } from 'vue';

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  }
});

// 格式化图表数据
const formatChartData = computed(() => ({
  categories: props.chartData.categories,
  
  series: props.chartData.series
}));

const opts = {
  color: ["#B8860B"],  // 线条的颜色
  enableScroll: true,   // 允许横向滚动
  legend: {
    show: true  // 隐藏图例
  },
  xAxis: {
    disableGrid: true,  // 禁用网格线
    fontColor: "#999999",  // X轴字体颜色
  },
  yAxis: {
    gridType: "dash",  // 虚线样式的网格
    dashLength: 2,     // 网格线长度
    data: []  // 可以根据需要配置 Y 轴的标签
  },
  extra: {
    line: {
      type: "smooth",   // 设置线条为平滑曲线（可选：'straight' 或 'smooth'）
      width: 2          // 线条宽度
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 300rpx;  /* 你可以根据需要调整图表的高度 */
}
</style>
