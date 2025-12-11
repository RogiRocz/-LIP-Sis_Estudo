
<!-- ReportCard.vue -->
<template>
  <div class="card" :class="icon">
    <div class="info">
      <h3>{{ title }}</h3>
      <p>{{ value }}</p>
    </div>
    <div class="icon-box">
      <span :class="`icon-${icon}`"></span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    value: String,
    icon: String
  }
}
</script>

<style scoped>
.card {
  flex: 1;
  min-width: 200px;
  padding: 18px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #eef2ff, #fafbff);
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.card.book {
  background: linear-gradient(135deg, #d7f5f5, #f0fbfb);
}
.card.clock {
  background: linear-gradient(135deg, #e7eaff, #f4f6ff);
}
.card.medal {
  background: linear-gradient(135deg, #f4eaff, #f9f5ff);
}
.card.calendar {
  background: linear-gradient(135deg, #dff8f3, #f1fdf9);
}

.info h3 {
  font-size: 14px;
  margin: 0;
  color: #555;
}

.info p {
  font-size: 20px;
  font-weight: bold;
  margin: 5px 0 0;
  color: #4a63e7;
}

.icon-box {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
  background: rgba(255,255,255,0.6);
}

.icon-clock::before,
.icon-book::before,
.icon-medal::before,
.icon-calendar::before {
  font-size: 22px;
  color: #666;
}
</style>

