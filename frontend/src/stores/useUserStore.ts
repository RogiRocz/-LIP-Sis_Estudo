import { Usuario } from '@/utils/apiTypes'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getProfile } from '@/api/user'
import router from '@/router'
import { useTheme } from 'vuetify'

const ThemeMap = {
	claro: 'light',
	escuro: 'dark',
} as const

export const useUserStore = defineStore('userStore', () => {
	// State
	const drawerAuth = ref(false)
	const loading = ref(false)
	const token = ref(localStorage.getItem('authToken') || null)
	const refresh_token = ref(localStorage.getItem('refreshToken') || null)
	const expires_at = ref(localStorage.getItem('expiresAt') || null)
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

	const setTokens = (
		newToken: string | null,
		newRefreshToken: string | null,
		newExpiresAt: string | null,
	) => {
		token.value = newToken
		refresh_token.value = newRefreshToken
		expires_at.value = newExpiresAt

		if (newToken) {
			localStorage.setItem('authToken', newToken)
			if (newRefreshToken) localStorage.setItem('refreshToken', newRefreshToken)
			if (newExpiresAt) localStorage.setItem('expiresAt', newExpiresAt)
		} else {
			logout()
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
		localStorage.removeItem('refreshToken')
		localStorage.removeItem('expiresAt')

		token.value = null
		refresh_token.value = null
		expires_at.value = null
		user.value = null

		router.replace({ name: 'login' })
	}

	const fetchUser = async () => {
		if (token.value) {
			try {
				const userData = await getProfile()
				setUser(userData)

				if (userData?.ui_theme) {
					const theme = ThemeMap[userData.ui_theme]
					console.log('tema passado no fetch user: ', theme)

					theme.global.name.value = theme
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
		setTokens,
		refresh_token,
		expires_at,
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
