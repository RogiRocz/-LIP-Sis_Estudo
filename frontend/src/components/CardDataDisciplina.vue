<script setup lang="ts">
import { Tema } from '@/utils/apiTypes'
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
	<v-card class="card-main" variant="outlined">
		<v-card-item
			class="discipline-card-header"
			@click="isThemesExpanded = !isThemesExpanded"
		>
			<template #prepend>
				<v-sheet
					:color="props.color"
					rounded="circle"
					width="10"
					height="10"
				></v-sheet>
			</template>

			<div>
				<v-card-title class="discipline-name pa-0">{{
					name_disciplina
				}}</v-card-title>
				<v-card-subtitle class="theme-count pa-0"
					>{{ tema_quantity }} temas</v-card-subtitle
				>
			</div>

			<template #append>
				<v-btn icon="delete" variant="text" size="small" @click.stop></v-btn>
				<v-icon
					:icon="isThemesExpanded ? 'expand_less' : 'expand_more'"
					size="small"
					class="expand-icon"
				></v-icon>
			</template>
		</v-card-item>

		<v-slide-y-transition>
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
		</v-slide-y-transition>
	</v-card>
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
	white-space: normal;
}

.no-themes-message {
	text-align: center;
	color: rgb(var(--v-theme-on-surface-variant));
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
