<template>
	<v-container no-gutters fluid>
		<v-row id="page-header">
			<v-col id="page-header-info">
				<h2>{{ pageTitle }}</h2>
				<p>{{ pageDescription }}</p>
			</v-col>
			<v-col id="page-header-actions">
				<slot name="page-header-actions"> </slot>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
const props = defineProps<{
	pageTitle: string
	pageDescription: string
}>()
</script>

<style scoped>
h2 {
	font-weight: 400;
}

p {
	color: #64748b;
}

#page-header-actions {
	display: flex;
	align-items: center;
	justify-content: flex-end;
}

#page-header-actions > :deep(.v-btn) {
	margin: 0 .5vw;
}
</style>
