<!-- TimeBySubject.vue -->
<template>
  <div class="subject-card">
    <div class="title">Tempo por Disciplina</div>
    <p class="empty">Nenhuma sessão de estudo registrada ainda</p>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.subject-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid #e5e9f0;
  min-height: 200px;
}
.title {
  font-weight: 600;
  color: #444;
  margin-bottom: 20px;
}
.empty {
  color: #667;
  font-size: 14px;
}
</style>


