<template>
  <ViewContainer>
    <template #view-content>
      <div class="not-found">
        <h1>404</h1>
        <p>Xiiii será que existe mesmo?</p>
        <router-link to="/">Ir para página inicial</router-link>
      </div>
    </template>
  </ViewContainer>
</template>

<script setup lang="ts">
import ViewContainer from '@/components/ViewContainer.vue'
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
}
h1 {
  font-size: 4em;
}
p {
  font-size: 1.2em;
  margin: 2vh 0;
}
</style>
