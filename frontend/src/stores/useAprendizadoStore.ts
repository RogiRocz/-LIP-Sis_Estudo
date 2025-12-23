import { Disciplina, Revisao, Tema } from '@/utils/apiTypes'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAprendizadoStore = defineStore('aprendizadoStore', () => {
	const disciplinas = ref<Disciplina[] | null>(null)
	const temas = ref<Map<number, Tema[]> | null>(null)
	const revisoes = ref<Map<number, Revisao[]> | null>(null)
	const loading = ref(true)

	const disciplinas_quantity = computed(() => disciplinas.value?.length || 0)

	const setDisciplinas = (data: Disciplina[] | null) => {
		disciplinas.value = data
	}

	const setTemas = (data: Map<number, Tema[]> | null) => {
		temas.value = data
	}

	const setRevisoes = (data: Map<number, Revisao[]> | null) => {
		revisoes.value = data
	}

	const temas_quantity = (disciplina_id: number) => {
		const temasDaDisciplina = temas.value?.get(disciplina_id)
		return temasDaDisciplina?.length || 0
	}

	const reset = () => {
		disciplinas.value = null
		temas.value = null
		revisoes.value = null
	}

	return {
		disciplinas,
		temas,
		revisoes,
		loading,
		disciplinas_quantity,
		temas_quantity,
		setDisciplinas,
		setTemas,
		setRevisoes,
		reset,
	}
})