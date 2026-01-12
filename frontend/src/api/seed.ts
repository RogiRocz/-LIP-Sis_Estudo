import api from './apiConnect'
import type { SeedRequest } from '@/utils/apiTypes'

const resourceUrl = '/seed'

async function generateMockData(seedRequest?: SeedRequest) {
	try {
		const response = await api.post(
			`${resourceUrl}/mock-data`,
			seedRequest || {},
		)
		return response.data
	} catch (error: any) {
		const errorMessage =
			error.response?.data?.detail ||
			'Erro ao gerar dados mockados. Por favor, tente novamente.'
		throw new Error(errorMessage)
	}
}

export { generateMockData }
