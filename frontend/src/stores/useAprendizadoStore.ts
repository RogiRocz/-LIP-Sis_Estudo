import { supabase } from '@/config/supabase'
import { Disciplina, Revisao, Tema } from '@/utils/apiTypes'
import { syncArray, syncMap } from '@/utils/SyncSupabase'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAprendizadoStore = defineStore('aprendizadoStore', () => {
	const disciplinas = ref<Disciplina[] | null>(null)
	const temas = ref<Map<number, Tema[]> | null>(null)
	const revisoes = ref<Map<number, Revisao[]> | null>(null)
	const loading = ref(true)

	const disciplinas_quantity = computed(() => disciplinas.value?.length || 0)

	const temas_quantity = (disciplina_id: number) => {
		const temasDaDisciplina = temas.value?.get(disciplina_id)
		return temasDaDisciplina?.length || 0
	}

	const setDisciplinas = (data: Disciplina[] | null) => {
		disciplinas.value = null
		disciplinas.value = data
	}

	const setTemas = (data: Map<number, Tema[]> | null) => {
		temas.value = null
		temas.value = data
	}

	const setRevisoes = (data: Map<number, Revisao[]> | null) => {
		revisoes.value = null
		revisoes.value = data
	}

	const reset = () => {
		disciplinas.value = null
		temas.value = null
		revisoes.value = null
	}

	const setupRealtime = () => {
		const channel = supabase
			.channel('schema-db-changes')
			.on(
				'postgres_changes',
				{ event: '*', schema: 'public', table: 'Disciplina' },
				(payload) => {
					syncArray(disciplinas.value, payload)
				},
			)
			.on(
				'postgres_changes',
				{ event: 'INSERT', schema: 'public', table: 'Tema' },
				(payload) => {
					syncMap(temas.value, payload, 'disciplina_id')
				},
			)
			.on(
				'postgres_changes',
				{ event: 'INSERT', schema: 'public', table: 'Revisao' },
				(payload) => {
					syncMap(revisoes.value, payload, 'tema_id')
				},
			)
			.subscribe()

		return channel
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
		setupRealtime,
	}
})
