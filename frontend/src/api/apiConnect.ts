import axios from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { isTokenExpired, shouldRefreshToken } from '@/utils/tokens'
import { refresh_token } from './auth'

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
	headers: {
		'Content-Type': 'application/json',
	},
	withCredentials: true,
})

api.interceptors.request.use(
	(config) => {
		const token = localStorage.getItem('authToken')

		if (token) {
			config.headers.set('Authorization', `Bearer ${token}`)
		}

		// Gambiarra para funcionar no ambiente virtual do google workstations que não suporta o método PUT
		if (config.method === 'put') {
			config.method = 'post'
			config.headers.set('X-HTTP-Method-Override', 'PUT')
		}

		return config
	},
	(error) => {
		return Promise.reject(error)
	},
)

api.interceptors.response.use(
	(response) => response,
	async (error) => {
		const userStore = useUserStore()
		const snackbarStore = useSnackbarStore()
		const originalRequest = error.config

		const isLoginRequest = originalRequest.url.includes('/auth/login')

		if (error.response?.status === 401 && !originalRequest._retry && !isLoginRequest) {
			originalRequest._retry = true

			try {
				const data = await refresh_token(userStore.refresh_token)

				userStore.setTokens(
					data.token,
					data.refresh_token,
					data.expires_at,
				)

				originalRequest.headers['Authorization'] = `Bearer ${data.token}`
				return api(originalRequest)
			} catch (refreshError) {
				userStore.logout()
				snackbarStore.addMessage({
					text: 'Sua sessão expirou. Faça login novamente.',
					color: 'warning',
				})
				router.push({ name: 'Login' })
				return Promise.reject(refreshError)
			}
		}
		return Promise.reject(error)
	},
)

export default api
