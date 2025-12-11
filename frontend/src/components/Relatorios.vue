<template>
  <section class="dashboard">
    <!-- Meta de Hoje -->
    <GoalToday />

    <!-- Charts Row -->
    <div class="row">
      <div class="col">
        <Last7DaysChart />
      </div>

      <div class="col">
        <TimeBySubject />
      </div>
    </div>

  </section>
</template>

<script>
import GoalToday from "@/components/GoalToday.vue";
import Last7DaysChart from "@/components/Last7DaysChart.vue";
import TimeBySubject from "@/components/TimeBySubject.vue";
import RecentHistory from "@/components/RecentHistory.vue";

export default {
  components: {
    GoalToday,
    Last7DaysChart,
    TimeBySubject,
    RecentHistory
  }
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  background: #f4f7fb;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.col {
  flex: 1;
  min-width: 350px;
}
</style>

