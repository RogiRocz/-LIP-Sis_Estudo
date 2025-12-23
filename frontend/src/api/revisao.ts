import api from './apiConnect'
import type { PageParams, Revisao } from '@/utils/apiTypes'

const resourceUrl = '/revisoes'


async function getRevisoes(p?: PageParams) {
  try {
    const response = await api.get(resourceUrl, {
      data: {
        page: p?.page,
        size: p?.size
      }
    })
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar as revisões. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function updateRevisao(id: number, revisao: Revisao) {
  try {
    const response = await api.put(`${resourceUrl}/${id}`, revisao)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao atualizar a revisão. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function concluirRevisao(id: number, revisao: Revisao) {
  try {
    const response = await api.put(`${resourceUrl}/${id}/concluir`, revisao)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao concluir a revisão. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function getCronograma(p?: PageParams) {
  try {
    const response = await api.get(`${resourceUrl}/cronograma`, {
      data: {
        page: p?.page,
        size: p?.size
      }
    })
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar o cronograma. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function reagendarRevisao(id: number, nova_data: Date) {
  try {
    const response = await api.put(`${resourceUrl}/${id}/reagendar`, {
		nova_data: nova_data
	})
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao reagendar a revisão. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

export {
  getRevisoes,
  updateRevisao,
  concluirRevisao,
  getCronograma,
  reagendarRevisao
}
