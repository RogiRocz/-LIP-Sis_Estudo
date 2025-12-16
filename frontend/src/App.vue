<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import Navbar from './components/Navbar.vue'

</script>

<template>
  <!-- <RouterView /> -->
  <Navbar/>
  <RouterView />
</template>

<style scoped></style>
