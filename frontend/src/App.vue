<script setup>
import { RouterView } from 'vue-router'
import { ref } from 'vue'
import Cadastro from './components/Cadastro.vue'

const props = ref([
  {
    name: 'email',
    input: 'email',
    placeholder: 'E-mail',
  },
  {
    name: 'senha',
    input: 'password',
  },
  {
  name: 'confirmar senhar',
  input: 'password',
  }
])
</script>

<template>
  <!-- <RouterView /> -->
  <Cadastro title="Tema" :options="props" />
</template>

<style scoped></style>
