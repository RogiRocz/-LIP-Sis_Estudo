import { supabase } from '@/config/supabase'
import { Disciplina, Revisao, Tema } from '@/utils/apiTypes'
import { syncArray, syncMap } from '@/utils/SyncSupabase'
import { acceptHMRUpdate, defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAprendizadoStore = defineStore('aprendizadoStore', () => {
	const disciplinas = ref<Disciplina[] | null>([])
	const temas = ref<Map<number, Tema[]> | null>(new Map())
	const revisoes = ref<Map<number, Revisao[]> | null>(new Map())

	const currPage = ref(1)
	const itensPerPage = ref(12)
	const totalItems = ref(0)
	const loading = ref(true)

	const disciplinas_quantity = computed(() => disciplinas.value?.length || 0)

	const totalPages = computed(() => {
		const pages = Math.ceil(totalItems.value / itensPerPage.value)
		return pages > 0 ? pages : 1
	})

	const temas_quantity = (disciplina_id: number) => {
		const temasDaDisciplina = temas.value?.get(disciplina_id)
		return temasDaDisciplina?.length || 0
	}

	const setDisciplinas = (data: Disciplina[] | null) => {
		disciplinas.value = data
	}

	const setTemas = (data: Map<number, Tema[]> | null) => {
		temas.value = data
	}

	const setRevisoes = (data: Map<number, Revisao[]> | null) => {
		revisoes.value = data
	}

	const setPage = (page: number, itens: number) => {
		if (
			page > 0 &&
			itens > 0 &&
			page <= totalPages.value &&
			itens <= itensPerPage.value
		) {
			currPage.value = page
			itensPerPage.value = itens
		}
	}

	const reset = () => {
		disciplinas.value = null
		temas.value = null
		revisoes.value = null
	}

	const setupRealtime = async () => {
		const {
			data: { session },
		} = await supabase.auth.getSession()

		if (!session) {
			console.warn('Sem sessão ativa, não é possível criar canal realtime.')
			return
		}

		if (activeChannel) {
			await supabase.removeChannel(activeChannel)
			activeChannel = null
		}

		activeChannel = supabase
			.channel('db-public-changes')
			.on(
				'postgres_changes',
				{ event: '*', schema: 'public', table: 'Disciplina' },
				(payload) => {
					disciplinas.value = syncArray(disciplinas.value, payload)

					if (payload.eventType === 'INSERT') {
						totalItems.value++
					} else if (payload.eventType === 'DELETE') {
						totalItems.value--
					}
				},
			)
			.on(
				'postgres_changes',
				{ event: '*', schema: 'public', table: 'Tema' },
				(payload) => {
					temas.value = syncMap(temas.value, payload, 'disciplina_id')
				},
			)
			.on(
				'postgres_changes',
				{ event: '*', schema: 'public', table: 'Revisao' },
				(payload) => {
					revisoes.value = syncMap(revisoes.value, payload, 'tema_id')
				},
			)
			.subscribe((status, err) => {
				console.log('Status do Canal:', status)
				if (status === 'CLOSED' || status === 'TIMED_OUT') {
					console.log('Canal fechado ou temporariamente fora do ar.')
				} else if (err) {
					console.error('Erro ao se conectar ao canal:', err)
				}
			})

		return activeChannel
	}

	const cleanupRealtime = async () => {
		if (activeChannel) {
			await supabase.removeChannel(activeChannel)
			activeChannel = null
		}
	}

	supabase.auth.onAuthStateChange((event) => {
		if (event === 'SIGNED_OUT') {
			cleanupRealtime()
			reset()
		}
	})

	return {
		disciplinas,
		temas,
		revisoes,
		currPage,
		itensPerPage,
		totalItems,
		loading,
		disciplinas_quantity,
		temas_quantity,
		setDisciplinas,
		setTemas,
		setRevisoes,
		reset,
		setupRealtime,
		cleanupRealtime,
		setPage,
		totalPages,
	}
}, {
	persist: {
		pick: ['disciplinas', 'temas', 'revisoes', 'currPage', 'itensPerPage', 'totalItems', 'loading']
	}
})

let activeChannel: any = null

if (import.meta.hot) {
	import.meta.hot.dispose(async () => {
		await supabase.removeAllChannels()
		console.log('HMR: Canais do Supabase limpos para evitar duplicidade.')
	})

	import.meta.hot.accept(acceptHMRUpdate(useAprendizadoStore, import.meta.hot))
}
