<script setup lang="ts">
// Script logic here
</script>

<template>
	<div class="not-found">
		<h1>404</h1>
		<p>Xiiii será que existe mesmo?</p>
		<router-link to="/">Ir para página inicial</router-link>
	</div>
</template>

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
