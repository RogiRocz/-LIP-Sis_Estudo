<template>
	<v-app-bar app class="gradient-app-bar" color="transparent" flat>
		<template v-slot:prepend>
			<v-container class="pa-0">
				<v-row align="center">
					<v-col cols="auto" class="app-bar-titulo">
						<v-icon icon="book_ribbon" class="mr-2"></v-icon>
						<div>
							<v-app-bar-title>StudyFlow</v-app-bar-title>
							<span>Aprenda no momento certo</span>
						</div>
					</v-col>
				</v-row>
			</v-container>
		</template>
		<template v-slot:append>
			<v-spacer></v-spacer>
			<div v-if="nameDisplay === 'xs'">
				<v-app-bar-nav-icon
					@click="appBarStore.toggleDrawer"
				></v-app-bar-nav-icon>
			</div>
			<div v-else>
				<v-tabs :v-model="route.name">
					<v-tab
						v-for="(tab, i) in tabsNavigation"
						:key="i"
						:to="{ name: tab.routeName }"
					>
						<v-icon :icon="tab.iconName" class="mr-2"></v-icon>
						{{ tab.name }}
					</v-tab>
				</v-tabs>
			</div>
		</template>
	</v-app-bar>
</template>

<script setup lang="ts">
import { useAppBarStore } from '@/stores/useAppBarStore'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'


const appBarStore = useAppBarStore()
const { nameDisplay } = storeToRefs(appBarStore)

const route = useRoute()
</script>

<style scoped>
.gradient-app-bar {
	background: linear-gradient(
		to right,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
}

.app-bar-titulo {
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.app-bar-titulo > * {
	margin: auto 1vw;
}
</style>
