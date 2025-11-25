<!-- Opcoes para cada elemento do form  -->
<!--   name -> nome do campo, vai fazer display emcima do elemento, tbm séra o nome no elemento  -->
<!--   input -> o tipo do input html que será usado -->
<!--   placeholder -> o texto que vai aparecer se usar algum campo de texto -->
<!--   subtitle -> subtitulo que vai aparecer do lado do elemento (feito para inputs do tipo checkbox) -->

<script setup>
const props = defineProps({
  title: String,
  options: [Object],
})
</script>

<template>
  <h1>{{ props.title }}</h1>
  <form action="get">
    <div v-for="option in props.options">
      <h3>{{ option.name }}</h3>
      <input
        :name="option.name"
        :type="option.input"
        :placeholder="option.placeholder"
      />
      <span v-if="option.subtitle">{{ option.subtitle }}</span>
    </div>
    <input type="submit" />
  </form>
</template>
