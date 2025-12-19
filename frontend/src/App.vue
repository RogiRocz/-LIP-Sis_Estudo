<script setup lang="ts">
import AppBar from '@/components/AppBar.vue'
import NavigationDrawer from '@/components/NavigationDrawer.vue';
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { watch, onMounted, ref } from 'vue'

const userStore = useUserStore()
const { drawerAuth, isAuthenticated } = storeToRefs(userStore)
const { fetchUser } = userStore

const snackbarStore = useSnackbarStore()
const { messages } = storeToRefs(snackbarStore)

const route = useRoute()
const router = useRouter()
const isRouterReady = ref(false)

const routesWithoutAppBar = ref(['login', 'cadastro', 'not-found'])

watch(route, (newVal) => {
	if (newVal && typeof newVal.name === 'string' && routesWithoutAppBar.value.includes(newVal.name)) {
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
		<NavigationDrawer />
		<AppBar v-if="isRouterReady && !drawerAuth" />
		<v-main :class="{ 'v-main-cadastro': drawerAuth }">
			<router-view v-if="isRouterReady" v-slot="{ Component, route }">
				<v-slide-x-transition mode="out-in">
					<component :is="Component" :key="route.path"/>
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
</style>