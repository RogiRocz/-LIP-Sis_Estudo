<script setup lang="ts">
import ConfirmDialog from './ConfirmDialog.vue'
import DisciplineDialog from './DisciplineDialog.vue'
import TemaDialog from '@/components/TemaDialog.vue'
import RevisoesDialog from '@/components/RevisoesDialog.vue'

import { Revisao, Tema } from '@/utils/apiTypes'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { deleteDisciplina } from '@/api/disciplina'
import { deleteTema } from '@/api/tema'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useDisciplinaStore } from '@/stores/useDisciplinaStore'
import { formatarData } from '@/utils/brDateFormat'
import { useTheme } from 'vuetify'

const aprendizadoStore = useAprendizadoStore()
const { revisoes } = storeToRefs(aprendizadoStore)
const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore
const disciplinaStore = useDisciplinaStore()
const { isEditing } = storeToRefs(disciplinaStore)
const userStore = useUserStore()
const { isDarkTheme } = storeToRefs(userStore)

const theme = useTheme()

const isThemesExpanded = ref(false)
const confirmDialogRef = ref<InstanceType<typeof ConfirmDialog> | null>(null)

const props = defineProps<{
	id_disciplina: number
	name_disciplina: string
	description: string
	color: string
	tema_quantity: number
	temas: Array<Tema> | null
}>()

function getStatus(tema_id: number): string[] {
	const revisoes_tema = revisoes.value?.get(tema_id) || []

	if (revisoes_tema.length === 0) return ['Nenhuma revisão agendada.']

	const realizadas = revisoes_tema.filter((r) => r.status === 'REALIZADA')
	const atrasadas = revisoes_tema.filter((r) => r.status === 'ATRASADA')
	const pendentes = revisoes_tema.filter((r) => r.status === 'PENDENTE')

	const ordenarPorData = (a: Revisao, b: Revisao) =>
		new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime()

	atrasadas.sort(ordenarPorData)
	pendentes.sort(ordenarPorData)

	if (
		atrasadas.length === 0 &&
		pendentes.length === 0 &&
		realizadas.length > 0
	) {
		return ['Todas as revisões concluídas.']
	}

	let mensagens: string[] = []

	atrasadas.forEach((rev) => {
		mensagens.push(`ATRASADA: ${formatarData(rev.data_prevista)}`)
	})

	pendentes.forEach((rev) => {
		mensagens.push(`PENDENTE: ${formatarData(rev.data_prevista)}`)
	})

	return mensagens
}

const temasVisiveis = computed(() => {
	if (!props.temas || !revisoes.value) return []

	return props.temas.filter((tema) => {
		const lista = revisoes.value.get(tema.ID) || []
		const temAlgoPraFazer = lista.some(
			(r) => r.status === 'ATRASADA' || r.status === 'PENDENTE',
		)

		return temAlgoPraFazer
	})
})

const cardColor = computed(() => {
	return isDarkTheme.value
		? '#' + theme.global.current.value.colors.primary
		: '#' + theme.global.current.value.colors.secondary
})

async function handleDeleteDisciplina(id: number) {
	const confirmed = await confirmDialogRef.value?.open(
		'Excluir Disciplina',
		'Tem certeza? Todos os temas e revisões vinculados serão perdidos.',
	)

	if (confirmed) {
		try {
			await deleteDisciplina(id)
			addMessage({ text: 'Disciplina excluída com sucesso.', color: 'success' })
		} catch (error) {
			addMessage({ text: 'Erro ao excluir a disciplina.', color: 'error' })
		}
	}
}

async function handleDeleteTheme(id: number) {
	console.log('id tema: ', id)

	const confirmed = await confirmDialogRef.value?.open(
		'Excluir Tema',
		'Tem certeza? Todas as revisões vinculadas serão perdidas.',
	)

	if (confirmed) {
		try {
			await deleteTema(id)
			addMessage({ text: 'Tema excluído com sucesso.', color: 'success' })
		} catch (error) {
			console.error(error)
			addMessage({ text: 'Erro ao excluir o tema.', color: 'error' })
		}
	}
}

const getStatusColorClass = (status: string) => {
	if (status.includes('ATRASADA')) return 'text-red-accent-4'
	if (status.includes('REALIZADA')) return 'text-success'
	if (status.includes('PENDENTE')) return 'text-purple-darken-3'
	return 'text-grey'
}
</script>

<template>
	<v-card class="card-main" variant="outlined">
		<v-card-item
			class="discipline-card-header"
			@click="isThemesExpanded = !isThemesExpanded"
		>
			<template #prepend>
				<v-divider
					v-if="!isThemesExpanded"
					vertical
					thickness="3"
					length="4vh"
					class="border-opacity-100"
					:color="props.color"
				></v-divider>
				<v-sheet
					v-if="isThemesExpanded"
					:color="props.color"
					rounded="circle"
					width="10"
					height="10"
				></v-sheet>
			</template>

			<v-card-title class="discipline-name pa-0">{{
				name_disciplina
			}}</v-card-title>
			<v-card-subtitle class="theme-count pa-0"
				>{{ tema_quantity }} temas</v-card-subtitle
			>

			<template #append>
				<DisciplineDialog
					:title="'Editar disciplina'"
					:subtitle="'Altere os dados da disciplina'"
					:whichFuncToCall="'update'"
					:initialData="{
						ID: props.id_disciplina,
						nome: props.name_disciplina,
						descricao: props.description,
						cor: props.color,
					}"
				>
					<template #button="activatorProps">
						<v-btn
							v-show="isEditing"
							icon="edit"
							variant="text"
							size="small"
							v-bind="activatorProps"
							@click.stop=""
						></v-btn>
					</template>
				</DisciplineDialog>
				<v-btn
					v-show="isEditing"
					icon="delete"
					variant="text"
					size="small"
					@click.stop="handleDeleteDisciplina(props.id_disciplina)"
				></v-btn>
				<v-icon
					:icon="isThemesExpanded ? 'expand_less' : 'expand_more'"
					size="small"
					class="expand-icon"
					color="inherit"
				></v-icon>
			</template>
		</v-card-item>

		<v-expand-transition>
			<div v-show="isThemesExpanded">
				<v-divider></v-divider>
				<v-list v-if="temasVisiveis.length > 0" lines="two" class="theme-list">
					<template v-for="t in temasVisiveis" :key="t.ID">
						<v-hover v-slot="{ isHovering, props }">
							<v-list-item class="theme-item" v-bind="props">
								<v-list-item-title class="theme-name">{{
									t.nome
								}}</v-list-item-title>
								<v-list-item-subtitle
									class="theme-card-status"
									:class="{ 'on-hover': isHovering }"
								>
									<span
										v-for="(r, i) in getStatus(t.ID)"
										:key="i"
										class="theme-card-status-item"
										:class="getStatusColorClass(r)"
									>
										{{ r }}
									</span>
								</v-list-item-subtitle>

								<template #append>
									<RevisoesDialog :tema="t" :revisoes="revisoes.get(t.ID)">
										<template #button="activatorProps">
											<v-btn
												v-show="!isEditing"
												v-bind="activatorProps"
												icon="play_arrow"
												variant="text"
												size="small"
												@click.stop
											></v-btn>
										</template>
									</RevisoesDialog>

									<div v-show="isEditing">
										<TemaDialog
											:title="'Editar Tema'"
											:subtitle="'Preencha com as novas informações do tema'"
											:whichFuncToCall="'update'"
											:initialData="{
												id_disciplina: t.disciplina_id,
												ID: t.ID,
												nome: t.nome,
												descricao: t.descricao,
												revisoes: revisoes?.get(t.ID),
											}"
										>
											<template #button="activatorProps">
												<v-btn
													icon="edit_square"
													variant="text"
													size="small"
													@click.stop
													v-bind="activatorProps"
												></v-btn>
											</template>
										</TemaDialog>
									</div>
									<div v-show="isEditing">
										<v-btn
											icon="delete"
											variant="text"
											size="small"
											@click.stop="handleDeleteTheme(t.ID)"
										></v-btn>
									</div>
								</template>
							</v-list-item>
						</v-hover>
					</template>
				</v-list>
				<div v-else class="no-themes-message">
					<p>Nenhum tema com revisões agendadas para esta disciplina.</p>
				</div>
				<v-divider></v-divider>
				<v-card-actions class="add-theme-button-container">
					<TemaDialog
						:title="'Novo tema'"
						:subtitle="'Crie um novo tema de estudo para esta disciplina'"
						:whichFuncToCall="'create'"
						:initialData="{
							id_disciplina: props.id_disciplina,
						}"
					>
						<template #button="props">
							<v-btn
								prepend-icon="add"
								color="inherit"
								variant="outlined"
								block
								v-bind="props"
								>Adicionar tema</v-btn
							>
						</template>
					</TemaDialog>
				</v-card-actions>
			</div>
		</v-expand-transition>
	</v-card>
	<ConfirmDialog ref="confirmDialogRef" />
</template>

<style scoped>
.card-main {
	margin: 10px;
	border-radius: 12px;
	background-color: v-bind(cardColor) !important;
	color: rgb(var(--v-theme-on-surface));
}

.discipline-card-header {
	cursor: pointer;
	min-height: 90px;
	background-color: inherit;
}

.discipline-name {
	font-size: 1rem;
	font-weight: 500;
	white-space: normal;
	color: rgb(var(--v-theme-on-surface));
}

.theme-count {
	font-size: 0.8rem;
	color: rgb(var(--v-theme-on-surface));
}

.expand-icon {
	transition: transform 0.2s ease 1s;
}

.theme-list {
	background-color: inherit;
}

.theme-item {
	border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.1);
}

.theme-item:last-child {
	border-bottom: none;
}

.theme-name {
	font-size: 0.9rem;
	white-space: normal;
}

.theme-card-status {
	font-size: 0.75rem;
	white-space: pre-line;
	overflow: hidden;
	max-height: 2rem;
	opacity: 0.7;

	transition:
		max-height 0.5s ease-in-out,
		opacity 0.3s ease;
}

.theme-card-status.on-hover {
	display: block;
	-webkit-line-clamp: none;
	line-clamp: none;
	max-height: 100%;
	opacity: 0.8;
}

.theme-card-status-item {
	display: block;
}

.no-themes-message {
	text-align: center;
	color: rgb(var(--v-theme-on-surface));
	padding: 16px;
}

.add-theme-button-container {
	margin: 1vh 0;
	padding: 8px 16px;
	display: flex;
	justify-content: center;
	background-color: inherit;
}

.add-theme-button-container .v-btn {
	text-transform: none;
}
</style>
