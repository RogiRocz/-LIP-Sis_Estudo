import { Usuario } from '@/utils/apiTypes'
import api from './apiConnect'

const resourceUrl = '/usuario'

async function getProfile(): Promise<Usuario> {
	try {
		const response = await api.get<Usuario>(`${resourceUrl}/perfil`)
		return response.data
	} catch (error) {
		console.error('Erro ao buscar perfil do usuário:', error)
		throw error
	}
}

export { getProfile }
