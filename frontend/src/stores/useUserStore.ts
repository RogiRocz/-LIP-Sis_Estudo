import { Usuario } from '@/utils/apiTypes'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getProfile } from '@/api/user'
import router from '@/router'

export const useUserStore = defineStore('userStore', () => {
	// State
	const drawerAuth = ref(false)
	const loading = ref(false)
	const token = ref(localStorage.getItem('authToken') || null)
	const user = ref<Usuario | null>(null)

	// Getters
	const isDrawerOpen = computed(() => drawerAuth.value)
	const isAuthenticated = computed(() => !!token.value)
	const getUser = computed(() => user.value)

	// Actions
	const toggleDrawerAuth = () => {
		drawerAuth.value = !drawerAuth.value
	}

	const setToken = (newToken: string | null) => {
		token.value = newToken
		if (newToken) {
			localStorage.setItem('authToken', newToken)
		} else {
			localStorage.removeItem('authToken')
		}
	}

	const setUser = (newUser: Usuario | null) => {
		if (newUser) {
			user.value = newUser
		} else {
			user.value = null
		}
	}

	const logout = () => {
		localStorage.removeItem('authToken')
		token.value = null
		user.value = null
		router.replace({name: 'login'})
	}

	const fetchUser = async () => {
		if (token.value) {
			try {
				const userData = await getProfile()
				setUser(userData)
			} catch (error) {
				console.error(
					'Falha ao buscar usuário. Token pode ser inválido.',
					error,
				)
				logout()
			}
		}
	}

	return {
		drawerAuth,
		loading,
		token,
		user,
		setToken,
		setUser,
		isAuthenticated,
		getUser,
		isDrawerOpen,
		toggleDrawerAuth,
		logout,
		fetchUser,
	}
})
