import { Usuario } from '@/utils/apiTypes'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getProfile } from '@/api/user'
import router from '@/router'
import { useTheme } from 'vuetify'

export const useUserStore = defineStore('userStore', () => {
	// State
	const drawerAuth = ref(false)
	const loading = ref(false)
	const token = ref(localStorage.getItem('authToken') || null)
	const user = ref<Usuario | null>(null)
	const theme = useTheme()

	// Getters
	const isDrawerOpen = computed(() => drawerAuth.value)
	const isAuthenticated = computed(() => !!token.value)
	const getUser = computed(() => user.value)
	const isDarkTheme = computed(() => {
		return theme?.global?.name?.value === 'dark'
	})
	const intervalos = computed(() => user.value?.intervalo_revisoes)

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
		router.replace({ name: 'login' })
	}

	const fetchUser = async () => {
		if (token.value) {
			try {
				const userData = await getProfile()
				setUser(userData)

				if (userData?.ui_theme) {
					theme.global.name.value = userData.ui_theme
				}
			} catch (error) {
				console.error(
					'Falha ao buscar usuário. Token pode ser inválido.',
					error,
				)
				logout()
			}
		}
	}

	const updateTheme = (themeName: string) => {
		theme.change(themeName)
	}

	const setTheme = async (isDark: boolean) => {
		const themeName = isDark ? 'dark' : 'light'

		if (theme?.global) {
			theme.global.name.value = themeName
		}

		if (user.value) {
			user.value.ui_theme = themeName
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
		isDarkTheme,
		intervalos,
		setTheme,
		updateTheme,
	}
})
