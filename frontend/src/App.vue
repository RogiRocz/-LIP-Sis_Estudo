<script setup lang="ts">
import AppBar from '@/components/AppBar.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { watch, onMounted, ref } from 'vue'

const appBarStore = useAppBarStore()
const { drawer } = storeToRefs(appBarStore)

const userStore = useUserStore()
const { drawerAuth, isAuthenticated } = storeToRefs(userStore)
const { fetchUser } = userStore

const snackbarStore = useSnackbarStore()
const { messages } = storeToRefs(snackbarStore)

const route = useRoute()
const router = useRouter()
const isRouterReady = ref(false)

watch(route, (newVal) => {
	if (newVal && (newVal.name === 'cadastro' || newVal.name === 'login')) {
		drawerAuth.value = true
	} else {
		drawerAuth.value = false
	}
})

onMounted(() => {
	router.isReady().then(() => {
		isRouterReady.value = true
	})
	if (isAuthenticated.value) {
		fetchUser()
	}
})
</script>

<template>
	<v-app>
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
		</v-navigation-drawer>
		<AppBar v-if="isRouterReady && !drawerAuth" />
		<v-main :class="{ 'v-main-cadastro': drawerAuth }">
			<router-view v-if="isRouterReady" v-slot="{ Component }">
				<v-slide-x-transition mode="out-in">
					<component :is="Component" />
				</v-slide-x-transition>
			</router-view>
		</v-main>

		<v-snackbar-queue
			closeable
			v-model="messages"
			timeout="3000"
		></v-snackbar-queue>
	</v-app>
</template>

<style scoped>
.v-main {
	margin: 1vh 1vw;
}

.v-main-cadastro {
	margin: 0;
	padding: 0;
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
