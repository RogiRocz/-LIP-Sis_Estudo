import apiClient from './apiClient'

export const getEstatisticas = () => {
  return apiClient.get('/painel/estatisticas')
}
