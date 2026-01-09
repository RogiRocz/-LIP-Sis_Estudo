import { getDisciplinas } from '@/api/disciplina'
import { getTemas } from '@/api/tema'
import { getRevisoes } from '@/api/revisao'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { Tema, Revisao } from '@/utils/apiTypes'

export const syncAprendizadoCompleto = async (page = 1, itemsPerPage = 12) => {
	const store = useAprendizadoStore()

	try {
		store.loading = true

		const discData = await getDisciplinas({ page, size: itemsPerPage })
		store.setDisciplinas(discData.items.flat())

		const temas_map = new Map<number, Tema[]>()
		await Promise.all(
			discData.items.flat().map(async (d) => {
				const temasData = await getTemas(d.ID)
				temas_map.set(d.ID, temasData.items.flat())
			}),
		)
		store.setTemas(temas_map)

		const revisoes_map = new Map<number, Revisao[]>()
		const allRevisoes = await getRevisoes()

		if (allRevisoes && allRevisoes.items.length > 0) {
			temas_map.forEach((temasArray) => {
				temasArray.forEach((tema) => {
					const revDoTema = allRevisoes.items
						.flat()
						.filter((r: { tema_id: number }) => r.tema_id === tema.ID)
					revisoes_map.set(tema.ID, revDoTema)
				})
			})
		}
		store.setRevisoes(revisoes_map)

		store.currPage = discData.page
		store.totalItems = discData.total

		return discData.pages
	} finally {
		store.loading = false
	}
}
