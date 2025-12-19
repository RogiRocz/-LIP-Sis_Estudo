import { AuthResponse } from '@/utils/apiTypes'
import api from './apiConnect'
import axios from 'axios'

const authApi = axios.create({
	baseURL: `${api.defaults.baseURL}/auth`,
})

async function register(userData: any): Promise<AuthResponse> {
	try {
		const response = await authApi.post<AuthResponse>('/register', userData)
		return response.data
	} catch (error) {
		console.error('Erro ao criar usuário: ', error)
		throw error
	}
}

async function login(userData: any): Promise<AuthResponse> {
	try {
		const response = await authApi.post<AuthResponse>('/login', userData)
		return response.data
	} catch (error) {
		console.error('Erro ao logar usuário: ', error)
		throw error
	}
}

export { register, login }
