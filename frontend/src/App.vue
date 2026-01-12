<script setup lang="ts">
import AppBar from '@/components/AppBar.vue'
import NavigationDrawer from '@/components/NavigationDrawer.vue'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { watch, onMounted, ref, nextTick } from 'vue'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { supabase } from '@/config/supabase'
import { syncAprendizadoCompleto } from '@/services/AprendizadoService'
import { useTheme } from 'vuetify'
import { onBeforeUnmount } from 'vue'

let isRealtimeStarted = false

const userStore = useUserStore()
const { drawerAuth, isAuthenticated, user } = storeToRefs(userStore)
const { fetchUser } = userStore

const snackbarStore = useSnackbarStore()
const { messages } = storeToRefs(snackbarStore)

const route = useRoute()
const router = useRouter()
const isRouterReady = ref(false)

const routesWithoutAppBar = ref(['login', 'cadastro', 'not-found'])

const theme = useTheme()
const isThemeReady = ref(false)

nextTick(() => {
	isThemeReady.value = true
})

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
	isAuthenticated,
	async (val) => {
		if (val && !isRealtimeStarted && isThemeReady.value) {
			isRealtimeStarted = true
			setTimeout(() => {
				useAprendizadoStore().setupRealtime()
			}, 1000)

			try {
				await syncAprendizadoCompleto(1, 12)
			} catch (e) {
				console.error('Falha na carga inicial de aprendizado completo.')
			}
		} else if (!val) {
			isRealtimeStarted = false
			supabase.removeAllChannels()
		}
	},
	{ immediate: true },
)

onMounted(async () => {
	router.isReady().then(() => {
		isRouterReady.value = true
	})

	supabase.auth.onAuthStateChange((event, session) => {
		if (event === 'SIGNED_IN' && session) {
			const aprendizadoStore = useAprendizadoStore()
			aprendizadoStore.setupRealtime()
		}
		if (event === 'SIGNED_OUT') {
			userStore.logout()
		}
	})

	if (isAuthenticated.value) {
		await fetchUser()
	}
})

onBeforeUnmount(() => supabase.removeAllChannels())
</script>

<template>
	<v-app v-if="isThemeReady">
		<NavigationDrawer />
		<AppBar v-if="isRouterReady && !drawerAuth" />
		<v-main v-if="isRouterReady" :class="{ 'drawer-auth': drawerAuth }">
			<router-view v-if="isRouterReady" v-slot="{ Component, route }">
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
