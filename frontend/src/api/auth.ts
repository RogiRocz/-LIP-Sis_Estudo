import { RefreshTokenResponse, TokenResponse } from '@/utils/apiTypes'
import api from './apiConnect'

const resourceUrl = '/auth'

async function register(userData: any): Promise<TokenResponse> {
	try {
		const response = await api.post<TokenResponse>(`${resourceUrl}/register`, userData)
		return response.data
	} catch (error) {
		console.error('Erro ao criar usuário: ', error)
		throw error
	}
}

async function login(userData: any): Promise<TokenResponse> {
	try {
		const response = await api.post<TokenResponse>(`${resourceUrl}/login`, userData)
		return response.data
	} catch (error) {
		console.error('Erro ao logar usuário: ', error)
		throw error
	}
}

async function refresh_token(userData: any): Promise<RefreshTokenResponse> {
	try {
		const response = await api.post(`${resourceUrl}/refresh`, {refresh_token: userData})
		return response.data
	} catch (error) {
		console.error('Erro ao atualizar token: ', error)
		throw error
	}
}

async function closeSessionSupabase(token: string): Promise<void> {
	try {
		await api.post(`${resourceUrl}/logout`, {token: token})
	} catch (error) {
		console.error('Erro ao deslogar da conta: ', error)
		throw error
	}
}

export { register, login, refresh_token, closeSessionSupabase }
