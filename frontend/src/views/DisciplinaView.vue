<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader :pageTitle="name" :pageDescription="description">
				<template #page-header-actions>
					<v-btn prepend-icon="add" class="botao-gradient"
						>Nova disciplina</v-btn
					>
				</template>
			</PageHeader>
			<MainContainer v-if="!loading">
				<template #main-content>
					<v-row>
						<v-col v-for="d in disciplinas" :key="d.ID" cols="12" sm="6" md="4">
							<CardDataDisciplina
								:name_disciplina="d.nome"
								:description="d.descricao"
								:color="d.cor"
								:tema_quantity="temas_quantity(d.ID)"
								:temas="temas?.get(d.ID) || null"
							/>
						</v-col>
					</v-row>
					<v-pagination
						prev-icon="chevron_left"
						next-icon="chevron_right"
						v-model="page"
						:length="total_pages"
					></v-pagination>
				</template>
			</MainContainer>
			<div class="page-loading" v-if="loading">
				<v-progress-circular
					color="secondary"
					:indeterminate="loading"
					:size="100"
					:width="15"
				>
				</v-progress-circular>
			</div>
		</template>
	</ViewContainer>
</template>

<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import CardDataDisciplina from '@/components/CardDataDisciplina.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { computed, onMounted, ref } from 'vue'

import { getDisciplinas } from '@/api/disciplina'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { Disciplina, Revisao, Tema } from '@/utils/apiTypes'
import { getTemas } from '@/api/tema'
import { getRevisoes } from '@/api/revisao'

const ITENS_PER_PAGE = 10

const aprendizadoStore = useAprendizadoStore()
const { disciplinas_quantity, loading, disciplinas, temas, revisoes } =
	storeToRefs(aprendizadoStore)
const { temas_quantity, reset } = aprendizadoStore

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const page = ref(1)
const total_pages = computed(() =>
	Math.ceil(disciplinas_quantity.value / ITENS_PER_PAGE),
)

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'disciplina'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')

async function fetchAprendizado() {
	try {
		loading.value = true

		if (!alreadyFetched()) {
			switch (whoFetch()) {
				case 'all':
					await fetchDisciplinas()
					await fetchTemas()
					await fetchRevisoes()
					break
				case 'temas':
					await fetchTemas()
					break
				case 'revisoes':
					await fetchRevisoes()
					break
				default:
					addMessage({ text: 'Erro ao carregar os dados.', color: 'error' })
					reset()
					break
			}
		}

		console.log('fora do if')
	} catch (error) {
		console.log('Erro ao carregar os dados.', error)
		addMessage({ text: 'Erro ao carregar os dados.', color: 'error' })
		loading.value = false
		reset()
	} finally {
		loading.value = false
	}
}

function alreadyFetched() {
	const hasDisciplinas = disciplinas.value && disciplinas.value.length > 0
	const hasTemas = temas.value && temas.value.size > 0
	const hasRevisoes = revisoes.value && revisoes.value.size > 0

	return !!hasDisciplinas && !!hasTemas && !!hasRevisoes
}

function whoFetch() {
	if (!disciplinas.value || disciplinas.value.length === 0) return 'all'
	if (!temas.value || temas.value.size === 0) return 'temas'
	if (!revisoes.value || revisoes.value.size === 0) return 'revisoes'
	return 'none'
}

async function fetchDisciplinas() {
	try {
		const disciplinasData = await getDisciplinas({ page: page.value })

		if (disciplinasData.total === 0) {
			addMessage({ text: 'Nenhuma disciplina encontrada', color: 'warning' })
			return
		}

		aprendizadoStore.setDisciplinas(disciplinasData.items.flat())
	} catch (error) {
		console.log('Erro ao carregar os dados das disciplinas. ', error)
	}
}

async function fetchTemas() {
	try {
		const ids_disciplinas = disciplinas.value.map((d: Disciplina) => d.ID)
		const temas_map = new Map<number, Tema[]>()

		for (const id of ids_disciplinas) {
			const temasData = await getTemas(id)

			temas_map.set(id, temasData.items.flat())
		}

		aprendizadoStore.setTemas(temas_map)
	} catch (error) {
		console.log('Erro ao carregar os dados dos temas.', error)
	}
}

async function fetchRevisoes() {
	try {
		const ids_temas: number[] = []
		for (const temas_array of Array.from(temas.value.values())) {
			temas_array.forEach((tema: Tema) => ids_temas.push(tema.ID))
		}

		const revisoes_map = new Map<number, Revisao[]>()

		for (const id of ids_temas) {
			const arrayRevisoes = await getRevisoes()

			if (arrayRevisoes && arrayRevisoes.items.length > 0) {
				revisoes_map.set(id, arrayRevisoes.items.flat())
			}
		}

		aprendizadoStore.setRevisoes(revisoes_map)
	} catch (error) {
		console.log('Erro ao carregar os dados das revisões.', error)
	}
}
onMounted(async () => {
	if (alreadyFetched()) {
		loading.value = false
		return
	}

	await fetchAprendizado()
})
</script>

<style scoped>
.botao-gradient {
	background: linear-gradient(
		to right,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
	color: white;
	margin: auto 0;
	border-radius: 8px;
}

.page-loading {
	display: grid;
	place-items: center;
	height: 100%;
}
</style>
