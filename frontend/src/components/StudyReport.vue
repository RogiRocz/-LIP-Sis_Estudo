<template>
  <section class="report-container">
    <h2>Relatório de Estudos</h2>
    <p class="subtitle">Acompanhe seu desempenho e evolução</p>

    <div class="cards">
      <ReportCard title="Tempo Total" value="0h 0m" icon="clock" />
      <ReportCard title="Sessões Completas" value="0" icon="book" />
      <ReportCard title="Dias Seguidos" value="0" icon="medal" />
      <ReportCard title="Revisões Atrasadas" value="0" icon="calendar" />
    </div>
  </section>
  <GoalToday />
</template>

<script>
import ReportCard from './ReportCard.vue'

export default {
  components: { ReportCard },
}
</script>

<style scoped>
.report-container {
  padding: 20px;
  background: #f4f7fb;
}

.subtitle {
  margin-top: -10px;
  margin-bottom: 20px;
  color: #555;
}

.cards {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}
</style>
