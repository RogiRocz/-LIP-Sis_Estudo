<template>
	<v-container id="gradiente-background">
		<v-row class="logo">
			<div class="icon-background">
				<v-icon icon="book_ribbon" color="secondary" size="30"></v-icon>
			</div>
			<h2>StudyFlow</h2>
			<h4>Organize seus estudos com eficiência</h4>
		</v-row>
		<v-row>
			<v-card color="card" variant="flat" class="rounded-xl">
				<v-card-title align="center">{{ title }}</v-card-title>
				<v-card-subtitle align="center">{{ subtitle }}</v-card-subtitle>
				<v-form>
					<div v-for="(input, i) in inputs" :key="i">
						<span>{{ capitalize(input.name) }}</span>
						<v-text-field
							:glow="true"
							variant="filled"
							class="input"
							:type="input.type"
							:prepend-inner-icon="input.icon"
							:placeholder="input.placeholder"
							v-model="input.model.value"
							:rules="input.rules"
						>
						</v-text-field>
					</div>
					<slot name="submit-form"></slot>
				</v-form>
				<slot name="actions"></slot>
			</v-card>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { AuthInput } from '@/utils/authInputs'

defineProps<{
	title: string
	subtitle: string
	inputs: AuthInput[]
}>()

function capitalize(str: string) {
	return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped>
.v-container {
	display: grid;
	place-items: center;
	height: 100%;
	max-width: 100vw;
	background: linear-gradient(
		150deg,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
}

.logo {
	display: flex;
	flex-direction: column;
	align-items: center;
	color: white;
	margin: 5vh 0;
}

.logo + .v-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	margin: 0 !important;
	padding: 0;
}

.logo > h2 + h4 {
	margin-bottom: 2vh;
}

h4 {
	font-weight: lighter;
}

.icon-background {
	display: inline-flex;
	justify-content: center;
	align-items: center;
	width: 80px;
	height: 80px;
	background-color: rgb(var(--v-theme-background));
	border-radius: 100px;
	margin: 2vh 0;
	padding: 0;
}

.v-card {
	width: 40vw;
	padding: 2vw;
}

.v-card > * {
	margin: 10px 0;
	font-size: medium;
}

.v-card-title {
	font-size: 1.5em;
	font-weight: bold;
}

:deep(.v-btn[type='submit']) {
	display: flex;
	margin: 0 auto;
	margin-top: 10px;
	width: 80%;
	color: white;
	background: linear-gradient(
		150deg,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
}

:deep(p) {
	margin: 20px 0;
}
</style>
