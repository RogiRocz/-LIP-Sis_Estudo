<!-- GoalToday.vue -->
<template>
  <div class="goal-card">
    <div class="header">
      <span class="dot"></span>
      <span>Meta de Hoje</span>
      <span class="minutes">0 / 60 minutos</span>
    </div>

    <div class="bar-wrapper">
      <div class="bar"></div>
    </div>

    <p class="remaining">Faltam 60 minutos para atingir sua meta</p>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.goal-card {
  background: #f4f7fb;
  padding: 20px;
  border-radius: 12px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: #6c7cff;
  margin-right: 6px;
}
.bar-wrapper {
  width: 100%; height: 6px;
  background: #e4e8ff;
  border-radius: 6px;
  overflow: hidden;
}
.bar {
  width: 0%; height: 100%;
  background: #6c7cff;
}
.remaining {
  margin-top: 10px;
  color: #556;
  font-size: 14px;
}
</style>

