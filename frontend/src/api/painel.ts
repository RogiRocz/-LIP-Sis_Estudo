import api from './apiConnect';
import type { Estatisticas, EvolucaoSemanal, Revisao } from '@/utils/apiTypes';

const resourceUrl = '/painel';

async function getEstatisticas(): Promise<Estatisticas> {
  try {
    const response = await api.get(`${resourceUrl}/estatisticas`);
    return response.data;
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar as estatísticas. Por favor, tente novamente.';
    throw new Error(errorMessage);
  }
}

async function getEvolucaoSemanal(): Promise<EvolucaoSemanal[]> {
  try {
    const response = await api.get(`${resourceUrl}/evolucao-semanal`);
    return response.data;
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar a evolução semanal. Por favor, tente novamente.';
    throw new Error(errorMessage);
  }
}

async function getRevisoesDoDia(): Promise<Revisao[]> {
  try {
    const response = await api.get(`${resourceUrl}/revisoes-do-dia`);
    return response.data;
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Erro ao buscar as revisões do dia. Por favor, tente novamente.';
    throw new Error(errorMessage);
  }
}

export {
  getEstatisticas,
  getEvolucaoSemanal,
  getRevisoesDoDia,
};
