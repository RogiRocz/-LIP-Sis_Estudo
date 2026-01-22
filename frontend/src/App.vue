<script setup lang="ts">
import AppBar from '@/components/AppBar.vue'
import NavigationDrawer from '@/components/NavigationDrawer.vue'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { watch, onMounted, ref, nextTick, computed } from 'vue'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { supabase } from '@/config/supabase'
import { syncAprendizadoCompleto } from '@/services/AprendizadoService'
import { onBeforeUnmount } from 'vue'
import { useTheme } from 'vuetify'

const userStore = useUserStore()
const { drawerAuth, isAuthenticated, currentThemeName } = storeToRefs(userStore)
const { fetchUser } = userStore

const snackbarStore = useSnackbarStore()
const { messages } = storeToRefs(snackbarStore)

const aprendizadoStore = useAprendizadoStore()
const { isRealtimeConnected } = storeToRefs(aprendizadoStore)

const theme = useTheme()
const route = useRoute()
const router = useRouter()
const isRouterReady = ref(false)

const routesWithoutAppBar = ref(['login', 'cadastro', 'not-found'])

const noAppBarRoutes = computed(() => {
	return route.name && routesWithoutAppBar.value.includes(route.name as string)
})

watch(
	() => route.name,
	(name) => {
		drawerAuth.value = routesWithoutAppBar.value.includes(name as string)
	},
	{ immediate: true },
)

watch(route, (newVal) => {
	if (
		newVal &&
		typeof newVal.name === 'string' &&
		routesWithoutAppBar.value.includes(newVal.name)
	) {
		drawerAuth.value = true
	} else {
		drawerAuth.value = false
	}
})

watch(
	[isAuthenticated, isRealtimeConnected],
	async ([auth, connected]) => {
		if (auth && !connected) {
			useAprendizadoStore().setupRealtime()

			try {
				await syncAprendizadoCompleto(1, 12)
			} catch (e) {
				console.error('Falha na carga inicial de aprendizado completo.')
			}
		} else if (!auth) {
			aprendizadoStore.cleanupRealtime()
			aprendizadoStore.reset()
		}
	},
	{ immediate: true },
)

watch(
	currentThemeName,
	(newName) => {
		if (theme.global) {
			theme.global.name.value = newName
		}
	},
	{ immediate: true },
)

onMounted(async () => {
	router.isReady().then(() => {
		isRouterReady.value = true
	})

	if (isAuthenticated.value) {
		await fetchUser()
		useAprendizadoStore().setupRealtime()
	}
})

onBeforeUnmount(() => supabase.removeAllChannels())
</script>

<template>
	<v-app>
		<template v-if="!noAppBarRoutes">
			<NavigationDrawer />
			<AppBar />
		</template>
		<v-main :class="{ 'drawer-auth': noAppBarRoutes }">
			<router-view v-slot="{ Component, route }">
				<KeepAlive :max="10">
					<component :is="Component" :key="route.fullPath" />
				</KeepAlive>
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

.drawer-auth {
	margin: 0;
}
</style>
