import { Usuario } from '@/utils/apiTypes'
import api from './apiConnect'
import axios from 'axios'
import { useUserStore } from '@/stores/useUserStore'

const userApi = axios.create({
	baseURL: `${api.defaults.baseURL}/usuario`,
})

async function getProfile(): Promise<Usuario> {
	try {
		const userStore = useUserStore()
		const token = userStore.token
		const response = await userApi.get<Usuario>('/perfil', {
			headers: {
				Authorization: `Bearer ${token}`,
			},
		})
		return response.data
	} catch (error) {
		console.error('Erro ao buscar perfil do usuário:', error)
		throw error
	}
}

export { getProfile }
