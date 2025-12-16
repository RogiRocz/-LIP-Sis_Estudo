<template>
	<v-container no-gutters fluid>
		<v-row id="page-header">
			<v-col id="page-header-info">
				<h2>{{ pageTitle }}</h2>
				<p>{{ pageDescription }}</p>
			</v-col>
			<slot id="page-header-actions"> </slot>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
const props = defineProps<{
	pageTitle: string,
	pageDescription: string,
}>();
</script>

<style scoped>
h2 {
	font-weight: 400;
}

p {
	color: #64748b;
}

</style>
