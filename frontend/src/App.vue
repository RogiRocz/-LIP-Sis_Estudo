<script setup lang="ts">
import AppBar from './components/AppBar.vue'
</script>

<template>
	<v-app>
		<AppBar />
		<v-main>
			<router-view v-slot="{ Component }">
				<v-slide-x-transition mode="out-in">
					<component :is="Component" />
				</v-slide-x-transition>
			</router-view>
		</v-main>
	</v-app>
</template>

<style scoped></style>
