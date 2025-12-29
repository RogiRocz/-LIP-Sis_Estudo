import { AuthResponse } from '@/utils/apiTypes'
import api from './apiConnect'

const resourceUrl = '/auth'

async function register(userData: any): Promise<AuthResponse> {
	try {
		const response = await api.post<AuthResponse>(`${resourceUrl}/register`, userData)
		return response.data
	} catch (error) {
		console.error('Erro ao criar usuário: ', error)
		throw error
	}
}

async function login(userData: any): Promise<AuthResponse> {
	try {
		const response = await api.post<AuthResponse>(`${resourceUrl}/login`, userData)
		return response.data
	} catch (error) {
		console.error('Erro ao logar usuário: ', error)
		throw error
	}
}

export { register, login }
