<!-- Last7DaysChart.vue -->
<template>
  <div class="chart-card">
    <div class="title"><span class="icon">📈</span> Últimos 7 Dias</div>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
// import { Chart } from 'chart.js/auto'
//
// export default {
//   mounted() {
//     new Chart(this.$refs.chart, {
//       type: 'line',
//       data: {
//         labels: ['sex', 'sáb', 'dom', 'seg', 'ter', 'qua', 'qui'],
//         datasets: [{ data: [0,0,0,0,0,0,0], borderWidth: 2 }]
//       }
//     })
//   }
// }
</script>

<style scoped>
.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e5e9f0;
}
.title {
  margin-bottom: 10px;
  font-weight: 600;
  color: #444;
}
</style>

