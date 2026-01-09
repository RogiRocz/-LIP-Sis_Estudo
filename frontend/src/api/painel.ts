import type { AxiosInstance } from 'axios'
import api from './apiConnect'

export const painelApi = (apiClient: AxiosInstance = api) => ({
  getEstatisticas: async () => {
    const response = await apiClient.get('/painel/estatisticas')
    return response.data
  },

  getEvolucaoSemanal: async () => {
    const response = await apiClient.get('/painel/evolucao-semanal')
    return response.data
  },

  getRevisoesDoDia: async () => {
    const response = await apiClient.get('/painel/revisoes-do-dia')
    return response.data
  },
})
