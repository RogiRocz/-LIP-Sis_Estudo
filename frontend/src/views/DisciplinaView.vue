<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import CardDataDisciplina from '@/components/CardDataDisciplina.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import DisciplineDialog from '@/components/DisciplineDialog.vue'

import { tabsNavigation } from '@/utils/tabsNavigation'
import { computed, onActivated, onMounted, watch } from 'vue'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { useDisciplinaStore } from '@/stores/useDisciplinaStore'
import { syncAprendizadoCompleto } from '@/services/AprendizadoService'

const aprendizadoStore = useAprendizadoStore()
const {
	loading,
	disciplinas,
	temas,
	totalPages,
	currPage: page,
	itensPerPage,
	totalItems,
} = storeToRefs(aprendizadoStore)
const { temas_quantity } = aprendizadoStore

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const disciplinaStore = useDisciplinaStore()
const { isEditing } = storeToRefs(disciplinaStore)

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'disciplina'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')
const hasContent = computed(() => disciplinas.value.length > 0)

const carregarDados = async (newPage: number) => {
	try {
		loading.value = true
		await syncAprendizadoCompleto(newPage, itensPerPage.value)
	} catch (error) {
		addMessage({ text: 'Erro ao sincronizar dados.', color: 'error' })
	} finally {
		loading.value = false
	}
}

watch(page, async (newPage) => {
	try {
		carregarDados(newPage)
	} catch (error) {
		addMessage({ text: 'Erro ao atualizar os dados página.', color: 'error' })
	}
})

watch(
	() => disciplinas.value?.length,
	(newLen) => {
		if (newLen === undefined) return

		if (newLen > itensPerPage.value) {
			disciplinas.value.splice(itensPerPage.value)
		}

		if (newLen === 0 && page.value > 1) {
			page.value--
		}
	},
)

onMounted(async () => {
	if (!disciplinas.value || disciplinas.value.length === 0) {
		await carregarDados(page.value)
	}
})
</script>
<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader :pageTitle="name" :pageDescription="description">
				<template #page-header-actions>
					<v-btn
						:prepend-icon="isEditing ? 'close' : 'edit'"
						:class="isEditing ? 'bg-error' : 'botao-gradient'"
						@click="isEditing = !isEditing"
					>
						{{ isEditing ? 'Cancelar Edição' : 'Modo Edição' }}
					</v-btn>
					<DisciplineDialog
						:title="'Nova disciplina'"
						:subtitle="'Crie uma nova disciplina para organizar seus estudos'"
						:whichFuncToCall="'create'"
					>
						<template #button="props">
							<v-btn prepend-icon="add" class="botao-gradient" v-bind="props"
								>Nova disciplina</v-btn
							>
						</template>
					</DisciplineDialog>
				</template>
			</PageHeader>
			<MainContainer v-if="!loading">
				<template v-if="hasContent" #main-content>
					<v-row>
						<v-col
							v-for="d in disciplinas.slice(0, itensPerPage)"
							:key="d.ID"
							cols="12"
							sm="6"
							md="4"
						>
							<CardDataDisciplina
								:id_disciplina="d.ID"
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
						:length="totalPages"
					></v-pagination>
				</template>
				<template v-else #main-content>
					<v-alert
						title="Sem disciplinas"
						text="Você não tem nenhuma disciplina para mostrar algum conteúdo"
						type="error"
						variant="tonal"
					></v-alert>
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
