<script setup lang="ts">
import AppBar from './components/AppBar.vue'
import { tabsNavigation } from './utils/tabsNavigation'
import { useAppBarStore } from './stores/useAppBarStore'
import { storeToRefs } from 'pinia'

const appBarStore = useAppBarStore()
const { drawer } = storeToRefs(appBarStore)
</script>

<template>
	<v-app>
		<v-navigation-drawer temporary v-model="drawer">
			<v-list-item-title id="titulo">
				<v-icon icon="book_ribbon" class="mr-2"></v-icon>
				StudyFlow
			</v-list-item-title>
			<v-divider></v-divider>
			<v-list-item
				v-for="(tab, i) in tabsNavigation"
				:key="i"
				:prepend-icon="tab.iconName"
				:title="tab.name"
				:to="{ name: tab.routeName }"
			></v-list-item>
		</v-navigation-drawer>
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

<style scoped>
.v-main {
	margin: 1vh 1vw;
}

.v-list-item-title {
	line-height: 3.5;
}

#titulo {
	display: flex;
	justify-content: center;
	align-items: center;
}
</style>
