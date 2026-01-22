import { Usuario } from '@/utils/apiTypes'
import { defineStore } from 'pinia'
import { computed, getCurrentInstance, ref } from 'vue'
import { getProfile } from '@/api/user'
import { DEFAULT_THEME } from '@/config/vuetify'
import router from '@/router'
import { supabase } from '@/config/supabase'
import { closeSessionSupabase } from '@/api/auth'

const ThemeMap = {
	claro: 'light',
	escuro: 'dark',
	light: 'light',
	dark: 'dark',
} as const

export const useUserStore = defineStore('userStore', () => {
	// State
	const drawerAuth = ref(false)
	const loading = ref(false)
	const token = ref(localStorage.getItem('authToken') || null)
	const refresh_token = ref(localStorage.getItem('refreshToken') || null)
	const expires_at = ref(localStorage.getItem('expiresAt') || null)
	const user = ref<Usuario | null>(null)
	const currentThemeName = ref('light')

	// Getters
	const isDrawerOpen = computed(() => drawerAuth.value)
	const isAuthenticated = computed(() => !!token.value)
	const getUser = computed(() => user.value)
	const isDarkTheme = computed(() => currentThemeName.value === 'dark')
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
			const userTheme = ThemeMap[user.value.ui_theme]
			updateTheme(userTheme)
		} else {
			user.value = null
			updateTheme(ThemeMap[DEFAULT_THEME])
		}
	}

	const signOutSupabase = async () => {
		try {
			await closeSessionSupabase(token.value)
			await supabase.auth.signOut()
		} catch (error) {
			console.error('Erro ao fazer logout no Supabase:', error)
		}
	}

	const logout = () => {
		signOutSupabase()

		localStorage.removeItem('authToken')
		localStorage.removeItem('refreshToken')
		localStorage.removeItem('expiresAt')

		token.value = null
		refresh_token.value = null
		expires_at.value = null
		user.value = null

		router.replace({ name: 'login' })

		updateTheme(ThemeMap[DEFAULT_THEME])
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

	const updateTheme = (themeName: string) => {
		const formattedTheme = ThemeMap[themeName] || 'light'
		currentThemeName.value = formattedTheme
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
		currentThemeName,
		getUser,
		isDrawerOpen,
		toggleDrawerAuth,
		logout,
		fetchUser,
		isDarkTheme,
		intervalos,
		updateTheme,
	}
})
