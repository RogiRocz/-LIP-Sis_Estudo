<script setup lang="ts">
import ConfirmDialog from './ConfirmDialog.vue'
import DisciplineDialog from './DisciplineDialog.vue'
import { Tema } from '@/utils/apiTypes'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'
import { deleteDisciplina } from '@/api/disciplina'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useDisciplinaStore } from '@/stores/useDisciplinaStore'

const aprendizadoStore = useAprendizadoStore()
const { revisoes } = storeToRefs(aprendizadoStore)
const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore
const disciplinaStore = useDisciplinaStore()
const { isEditing } = storeToRefs(disciplinaStore)

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

const formatarData = (dataStr: string) => {
	return new Date(dataStr).toLocaleDateString('pt-BR', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})
}

function getStatus(tema_id: number): string {
	const revisoes_tema = revisoes.value?.get(tema_id) || []
	const hoje = new Date().setHours(0, 0, 0, 0)

	if (revisoes_tema.length === 0) return 'Nenhuma revisão agendada.'

	const pendentes = revisoes_tema.filter((rev) => {
		const dataRev = new Date(rev.data_prevista).getTime()

		return (
			rev.status !== 'REALIZADA' &&
			(rev.status === 'ATRASADA' ||
				rev.status === 'PENDENTE' ||
				dataRev <= hoje)
		)
	})

	if (pendentes.length === 0) {
		return revisoes_tema.every((r) => r.status === 'REALIZADA')
			? 'Todas as revisões concluídas.'
			: 'Nenhuma revisão para hoje.'
	}

	pendentes.sort(
		(a, b) =>
			new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime(),
	)

	return pendentes
		.map((rev) => {
			const dataRev = new Date(rev.data_prevista).getTime()
			let label = rev.status

			if (dataRev === hoje) label = 'HOJE'
			else if (dataRev < hoje) label = 'ATRASADA'

			return `${label} em ${formatarData(rev.data_prevista)}`
		})
		.join('\n')
}

const temasVisiveis = computed(() => {
	if (!props.temas) return []

	return props.temas.filter((tema) => {
		const lista = revisoes.value?.get(tema.ID) || []
		return lista.some((r) => r.status !== 'REALIZADA')
	})
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
						cor: props.color
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
				></v-icon>
			</template>
		</v-card-item>

		<v-expand-transition>
			<div v-show="isThemesExpanded">
				<v-divider></v-divider>
				<v-list v-if="temasVisiveis.length > 0" lines="two" class="theme-list">
					<v-list-item
						v-for="t in temasVisiveis"
						:key="t.ID"
						class="theme-item"
					>
						<v-list-item-title class="theme-name">{{
							t.nome
						}}</v-list-item-title>
						<v-list-item-subtitle class="theme-card-status">{{
							getStatus(t.ID)
						}}</v-list-item-subtitle>

						<template #append>
							<div v-show="!isEditing">
								<v-btn
									icon="play_arrow"
									variant="text"
									size="small"
									@click.stop
								></v-btn>
								<v-btn
									icon="delete"
									variant="text"
									size="small"
									@click.stop
								></v-btn>
							</div>
							<div v-show="isEditing">
								<v-btn
									icon="edit_square"
									variant="text"
									size="small"
									@click.stop
								></v-btn>
							</div>
						</template>
					</v-list-item>
				</v-list>
				<div v-else class="no-themes-message">
					<p>Nenhum tema com revisões agendadas para esta disciplina.</p>
				</div>
				<v-divider></v-divider>
				<v-card-actions class="add-theme-button-container">
					<v-btn prepend-icon="add" color="secondary" variant="outlined" block
						>Adicionar tema</v-btn
					>
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
	background-color: rgb(var(--v-theme-surface));
	color: rgb(var(--v-theme-on-surface));
}

.discipline-card-header {
	cursor: pointer;
	min-height: 90px;
}

.discipline-name {
	font-size: 1rem;
	font-weight: 500;
	white-space: normal;
}

.theme-count {
	font-size: 0.8rem;
	color: rgb(var(--v-theme-primary));
}

.expand-icon {
	transition: transform 0.2s ease;
}

.theme-list {
	background-color: transparent;
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
	display: -webkit-box;
	line-clamp: 1;
	-webkit-line-clamp: 1;
	-webkit-box-orient: vertical;
}

.theme-card-status {
	font-size: 0.75rem;
	white-space: pre-line;
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
}

.add-theme-button-container .v-btn {
	text-transform: none;
}
</style>
