<script setup lang="ts">
import AppBar from '@/components/AppBar.vue'
import NavigationDrawer from '@/components/NavigationDrawer.vue'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useRoute, useRouter } from 'vue-router'
import { watch, onMounted, ref } from 'vue'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { supabase } from '@/config/supabase'
import { syncAprendizadoCompleto } from '@/services/AprendizadoService'

let isRealtimeStarted = false;

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

watch(isAuthenticated, async (val) => {
    if (val && !isRealtimeStarted) {
        isRealtimeStarted = true;
        useAprendizadoStore().setupRealtime();

		try {
            await syncAprendizadoCompleto(1, 12);
        } catch (e) {
            console.error("Falha na carga inicial de aprendizado completo.");
        }
    } else if (!val) {
        isRealtimeStarted = false;
        supabase.removeAllChannels();
    }
}, { immediate: true });

onMounted(async () => {
	router.isReady().then(() => {
		isRouterReady.value = true
	})

	supabase.auth.onAuthStateChange(async (event, session) => {
		console.log('Supabase session: ', session)
		console.log(`Supabase Auth Event: ${event}`)
	})

	if (isAuthenticated.value) {
		await fetchUser()
	}
})
</script>

<template>
	<v-app>
		<NavigationDrawer />
		<AppBar v-if="isRouterReady && !drawerAuth" />
		<v-main v-if="isRouterReady" :class="{ 'drawer-auth': drawerAuth }">
			<router-view v-if="isRouterReady" v-slot="{ Component, route }">
				<v-slide-x-transition mode="out-in">
					<KeepAlive :max="10">
						<component :is="Component" :key="route.path" />
					</KeepAlive>
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

.drawer-auth {
	margin: 0;
}
</style>
