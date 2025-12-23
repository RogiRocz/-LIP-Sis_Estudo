<script setup lang="ts">
import { Tema, Revisao } from '@/utils/apiTypes'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { storeToRefs } from 'pinia'
import { computed, ref } from 'vue'

const aprendizadoStore = useAprendizadoStore()
const { revisoes } = storeToRefs(aprendizadoStore)

const isThemesExpanded = ref(false)

function getStatus(tema_id: number): string {
	const revisoes_tema = revisoes.value?.get(tema_id)

	if (!revisoes_tema || revisoes_tema.length === 0) {
		return 'Nenhuma revisão agendada.'
	}

	const pendenteOuAtrasada = revisoes_tema.filter(
		(rev) => rev.status === 'PENDENTE' || rev.status === 'ATRASADA',
	)

	if (pendenteOuAtrasada.length === 0) {
		const todasRealizadas = revisoes_tema.every((r) => r.status === 'REALIZADA')
		if (todasRealizadas) {
			return 'Todas as revisões concluídas.'
		}
		return 'Nenhuma revisão pendente/atrasada.'
	}

	pendenteOuAtrasada.sort(
		(a, b) =>
			new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime(),
	)

	const primeiraRevisao = pendenteOuAtrasada[0]
	const dataPrevista = new Date(primeiraRevisao.data_prevista)
	const dataFormatada = dataPrevista.toLocaleDateString('pt-BR', {
		day: '2-digit',
		month: '2-digit',
		year: 'numeric',
	})

	return `${primeiraRevisao.status} em ${dataFormatada}`
}

const props = defineProps<{
	name_disciplina: string
	description: string
	color: string
	tema_quantity: number
	temas: Array<Tema> | null
}>()

const temasVisiveis = computed(() => {
	if (!props.temas) {
		return []
	}
	return props.temas.filter(
		(tema) => getStatus(tema.ID) !== 'Nenhuma revisão agendada.',
	)
})
</script>
<template>
	<v-card class="card-main">
		<div
			class="discipline-card-header"
			@click="isThemesExpanded = !isThemesExpanded"
		>
			<div class="card-head-left">
				<div class="color-dot" :style="{ backgroundColor: props.color }"></div>
				<div class="card-head-info">
					<v-card-title class="discipline-name pa-0">{{
						name_disciplina
					}}</v-card-title>
					<v-card-subtitle class="theme-count pa-0"
						>{{ tema_quantity }} temas</v-card-subtitle
					>
				</div>
				<v-icon
					:icon="isThemesExpanded ? 'expand_less' : 'expand_more'"
					size="small"
					class="expand-icon"
				></v-icon>
			</div>
			<div class="card-head-actions">
				<v-btn icon="delete" variant="text" size="small"></v-btn>
			</div>
		</div>

		<v-container class="theme-list-container" fluid v-if="isThemesExpanded">
			<v-row class="theme-list-row" v-if="temasVisiveis.length > 0">
				<v-col
					v-for="t in temasVisiveis"
					:key="t.ID"
					cols="12"
					class="theme-col-wrapper"
				>
					<v-card class="theme-card d-flex align-center justify-space-between">
						<div class="theme-card-content">
							<v-card-text class="theme-name pa-0">{{ t.nome }}</v-card-text>
							<v-card-subtitle class="theme-card-status pa-0">
								<span>{{ getStatus(t.ID) }}</span>
							</v-card-subtitle>
						</div>
						<div class="theme-card-actions">
							<v-btn icon="play_arrow" variant="text" size="small"></v-btn>
							<v-btn icon="delete" variant="text" size="small"></v-btn>
						</div>
					</v-card>
				</v-col>
			</v-row>
			<v-row class="theme-list-row" v-else>
				<v-col cols="12" class="theme-col-wrapper">
					<p class="no-themes-message">
						Nenhum tema com revisões agendadas para esta disciplina.
					</p>
				</v-col>
			</v-row>
		</v-container>

		<div class="add-theme-button-container" v-if="isThemesExpanded">
			<v-btn prepend-icon="add">Adicionar tema</v-btn>
		</div>
	</v-card>
</template>
<style scoped>
.card-main {
	margin: 10px;
	border-radius: 12px;
	box-shadow: none;
	background-color: rgb(var(--v-theme-surface));
	color: rgb(var(--v-theme-on-surface));
	display: flex;
	flex-direction: column;
	min-width: 300px;
	flex: 1;
}

.discipline-card-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 12px 16px;
	border-bottom: 1px solid rgba(var(--v-theme-on-surface), 0.1);
	cursor: pointer;
	gap: 16px;
	height: 15vh;
}

.card-head-left {
	display: flex;
	align-items: center;
	gap: 8px;
	flex-grow: 1;
}

.color-dot {
	width: 10px;
	height: 10px;
	min-width: 10px;
	border-radius: 50%;
	flex-shrink: 0;
}

.card-head-info {
	display: flex;
	flex-direction: column;
	flex-grow: 1;
}

.discipline-name {
	font-size: 1rem;
	font-weight: 500;
	color: white;
	padding: 0;
	line-height: 1.2;
	white-space: normal !important;
}

.theme-count {
	font-size: 0.8rem;
	color: rgb(var(--v-theme-primary));
	padding: 0;
	line-height: 1.2;
	white-space: normal !important;
}

.expand-icon {
	transition: transform 0.2s ease;
}

.card-head-actions {
	display: flex;
	align-items: center;
	gap: 4px;
	flex-shrink: 0;
}

.theme-list-container {
	padding: 8px 16px !important;
}

.theme-list-row {
	margin: 0;
}

.theme-col-wrapper {
	padding: 4px !important;
}

.theme-card {
	background-color: rgb(var(--v-theme-surface-variant));
	border-radius: 8px;
	box-shadow: none;
	padding: 0px;
	width: 100%;
	min-height: 15vh;
}

.theme-card-content {
	flex-grow: 1;
	display: flex;
	flex-direction: column;
	height: 15vh;
}

.theme-name {
	font-size: 0.9rem;
	font-weight: 400;
	color: rgb(var(--v-theme-on-surface));
	padding: 8px 12px 0px 12px !important;
	white-space: normal;
	line-height: 1.3;
	height: 8vh;
	overflow: hidden;
	text-overflow: ellipsis;
}

.theme-card-status {
	font-size: 0.75rem;
	color: rgb(var(--v-theme-on-surface-variant));
	padding: 0px 12px 8px 12px !important;
	line-height: 1.2;
	white-space: normal;
}

.theme-card-actions {
	display: flex;
	flex-direction: column;
	justify-content: center;
	padding: 4px;
}

.theme-card-actions .v-btn {
	color: rgb(var(--v-theme-on-surface-variant));
	opacity: 0.8;
}

.theme-card-actions .v-btn:hover {
	opacity: 1;
}

.no-themes-message {
	text-align: center;
	color: rgb(var(--v-theme-on-surface-variant));
	padding: 16px;
}

.add-theme-button-container {
	padding: 8px 16px;
	border-top: 1px solid rgba(var(--v-theme-on-surface), 0.1);
	text-align: center;
	margin: 1vh 0;
}

.add-theme-button-container .v-btn {
	background-color: rgb(var(--v-theme-primary));
	color: rgb(var(--v-theme-on-primary));
	border-radius: 8px;
	padding: 8px 16px;
	text-transform: none;
	height: 40px;
	width: 100%;
}
</style>
