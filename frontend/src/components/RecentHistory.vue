<!-- RecentHistory.vue -->
<template>
  <div class="history-card">
    <div class="title">Histórico Recente</div>
    <p class="empty">Nenhuma sessão de estudo registrada</p>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.history-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e5e9f0;
  min-height: 150px;
}
.title {
  font-weight: 600;
  color: #444;
  margin-bottom: 15px;
}
.empty {
  text-align: center;
  color: #667;
}
</style>
