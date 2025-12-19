<script setup lang="ts">
import { useAppBarStore } from '@/stores/useAppBarStore'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'

const appBarStore = useAppBarStore()
const { drawer } = storeToRefs(appBarStore)

const userStore = useUserStore()
const { logout } = userStore

</script>

<template>
	<v-navigation-drawer temporary v-model="drawer">
		<v-list-item-title id="titulo">
			<v-icon icon="book_ribbon" class="mr-2"></v-icon>
			StudyFlow
		</v-list-item-title>
		<v-divider></v-divider>
		<template v-for="(tab, i) in tabsNavigation" :key="i">
			<v-list-item
				v-if="tab.isVisible"
				:prepend-icon="tab.iconName"
				:title="tab.name"
				:to="{ name: tab.routeName }"
			></v-list-item>
		</template>
		<template #append>
			<div class="pa-2">
				<v-btn @click="logout" block color="error">Sair</v-btn>
			</div>
		</template>
	</v-navigation-drawer>
</template>

<style scoped>
.v-list-item-title {
	line-height: 3.5;
}

#titulo {
	display: flex;
	justify-content: center;
	align-items: center;
}
</style>
