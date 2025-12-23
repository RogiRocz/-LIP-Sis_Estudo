import api from './apiConnect'
import type { Disciplina, Page, PageParams } from '@/utils/apiTypes'

const resourceUrl = '/disciplinas'

async function createDisciplina(disciplina: Disciplina) {
  try {
    const response = await api.post(resourceUrl, disciplina)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao criar a disciplina. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function getDisciplinas(p?: PageParams) : Promise <Page<Disciplina[]>> {
  try {
    const response = await api.get(resourceUrl, {
      data: {
        page: p?.page,
        size: p?.size
      }
    })
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar as disciplinas. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function getDisciplina(id: number) {
  try {
    const response = await api.get(`${resourceUrl}/${id}`)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar a disciplina. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function updateDisciplina(id: number, disciplina: Disciplina) {
  try {
    const response = await api.put(`${resourceUrl}/${id}`, disciplina)
    return response.data
  } catch (error: any)
  {
    const errorMessage = error.response?.data?.detail || 'Erro ao atualizar a disciplina. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

async function deleteDisciplina(id: number) {
  try {
    const response = await api.delete(`${resourceUrl}/${id}`)
    return response.data
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao deletar a disciplina. Por favor, tente novamente.'
    throw new Error(errorMessage)
  }
}

export {
  createDisciplina,
  getDisciplinas,
  getDisciplina,
  updateDisciplina,
  deleteDisciplina
}
