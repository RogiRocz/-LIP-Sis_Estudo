<script setup lang="ts"></script>
<template>
	<v-container fluid class="pa-0 ma-0">
		<slot name="view-content"></slot>
	</v-container>
</template>

<style scoped>
.v-container {
    height: 100%;
}
</style>
