import api from './apiConnect'
import type { PageParams, Revisao, Tema } from '@/utils/apiTypes'

const resourceUrl = '/temas'
const nestedResourceUrl = '/disciplinas'

async function getRevisoesByTema(tema_id: number) : Promise<Revisao[]>{
  try {
    const response = await api.get(`${resourceUrl}/${tema_id}/revisoes`)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar as revisões por tema. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function createTema(disciplina_id: number, tema: Tema) {
  try {
    const response = await api.post(`${nestedResourceUrl}/${disciplina_id}/temas`, tema)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao criar o tema. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function getTemas(disciplina_id: number, p?: PageParams) {
  try {   
    const response = await api.get(`${nestedResourceUrl}/${disciplina_id}/temas`, {
      data: {
        page: p?.page,
        size: p?.size
      }
    })
    
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar os temas. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function getTema(id: number) {
  try {
    const response = await api.get(`${resourceUrl}/${id}`)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar o tema. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function updateTema(id: number, tema: Tema) {
  try {
    const response = await api.put(`${resourceUrl}/${id}`, tema)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao atualizar o tema. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function deleteTema(id: number) {
  try {
    const response = await api.delete(`${resourceUrl}/${id}`)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao deletar o tema. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

export {
  createTema,
  getTemas,
  getTema,
  updateTema,
  deleteTema,
  getRevisoesByTema
}
