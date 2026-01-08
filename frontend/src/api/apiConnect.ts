import axios from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'

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

		if (error.response && error.response.status === 401) {
			userStore.logout()

			snackbarStore.addMessage({
				text: 'Sua sessão expirou. Por favor, faça login novamente.',
				color: 'warning',
			})

			await router.push({ name: 'Login' })
		}

		return Promise.reject(error)
	},
)

export default api
