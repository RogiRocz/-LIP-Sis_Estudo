<script setup lang="ts">
import TimerDialog from '@/components/TimerDialog.vue'
import ReagendarDialog from '@/components/ReagendarDialog.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { ref, computed, watch } from 'vue'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { useTimerStore } from '@/stores/useTimerStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { storeToRefs } from 'pinia'
import { Revisao, Tema } from '@/utils/apiTypes'
import { formatarData } from '@/utils/brDateFormat'
import { deleteRevisao } from '@/api/revisao'

const props = defineProps<{
	tema: Tema | null
	revisoes: Revisao[] | []
}>()

const timerStore = useTimerStore()
const { tema } = storeToRefs(timerStore)

const dialog = ref(false)
const isEditingRevisions = ref(false)
const confirmDialog = ref<InstanceType<typeof ConfirmDialog> | null>(null)
const timerDialog = ref<InstanceType<typeof TimerDialog> | null>(null)

const appBarStore = useAppBarStore()
const snackbarStore = useSnackbarStore()
const { actionsWidthDialog } = storeToRefs(appBarStore)

const chooseIcon = (status: string) => {
	return status === 'REALIZADA' ? 'timer_off' : 'timer_play'
}

async function handleDeleteRevisao(id_revisao: number) {
	try {
		await deleteRevisao(id_revisao)
		snackbarStore.addMessage({
			text: 'Revisão excluída com sucesso!',
			color: 'success',
		})
	} catch (error) {
		console.error('Erro ao excluir revisão:', error)
		snackbarStore.addMessage({
			text: 'Erro ao excluir a revisão.',
			color: 'error',
		})
	}
}

async function promptToDelete(revisao: Revisao) {
	if (confirmDialog.value) {
		const confirmed = await confirmDialog.value.open(
			'Excluir Revisão',
			'Tem certeza que deseja excluir esta revisão? Esta ação não poderá ser desfeita.',
		)
		if (confirmed) {
			await handleDeleteRevisao(revisao.ID)
		}
	}
}

const revisoesOrdenadas = computed(() => {
	const statusPrioridade: Record<string, number> = {
		ATRASADA: 1,
		PENDENTE: 2,
		REALIZADA: 3,
	}

	return [...props.revisoes].sort((a, b) => {
		const prioridadeA = statusPrioridade[a.status] || 99
		const prioridadeB = statusPrioridade[b.status] || 99
		if (prioridadeA !== prioridadeB) return prioridadeA - prioridadeB
		return (
			new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime()
		)
	})
})

const timerInfo = (rev: Revisao) => {
	timerStore.setTema(props.tema)
	timerStore.setRevisao(rev)
}

const startTimer = (revisao: Revisao) => {
	timerInfo(revisao)
	if (timerDialog.value) {
		timerDialog.value.open()
	}
}

watch(dialog, (value) => {
	if (!value) {
		isEditingRevisions.value = false
	}
})
</script>

<template>
	<v-dialog v-model="dialog" :max-width="actionsWidthDialog">
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>

		<v-card scrollable variant="flat" color="card" rounded="lg" class="pa-2">
			<v-card-title class="d-flex align-center">
				Escolha o que estudar
				<v-spacer></v-spacer>
				<v-btn
					:icon="isEditingRevisions ? 'edit_off' : 'edit'"
					variant="text"
					@click="isEditingRevisions = !isEditingRevisions"
				></v-btn>
			</v-card-title>
			<v-divider></v-divider>
			<v-card-title class="theme-name">{{ tema?.nome }}</v-card-title>
			<v-card-subtitle class="theme-subtitle">{{
				tema?.descricao
			}}</v-card-subtitle>

			<v-list bg-color="#dddddd" lines="one" rounded="lg">
				<v-list-item
					v-for="(r, i) in revisoesOrdenadas"
					:key="i"
					class="pa-0 mb-4"
				>
					<v-card
						variant="flat"
						color="primary"
						rounded="lg"
						class="rev-card-item mx-2"
					>
						<template #prepend>
							<v-chip
								size="small"
								:color="
									r.status === 'REALIZADA'
										? 'success'
										: r.status === 'ATRASADA'
											? 'error'
											: 'warning'
								"
								variant="flat"
								class="ml-2"
							>
								{{ r.status }}
							</v-chip>
						</template>

						<v-card-text class="pa-2">
							<div class="d-flex flex-column" style="font-size: 0.8rem">
								<div>
									<strong>Data Prevista: </strong>
									{{ formatarData(r.data_prevista) }}
								</div>
								<div>
									<strong>Data Realizada: </strong>
									{{ r.data_realizada ? formatarData(r.data_realizada) : '-' }}
								</div>
								<div>
									<strong>Tempo dedicado: </strong>
									{{ r.tempo_dedicado ? r.tempo_dedicado + ' min' : '-' }}
								</div>
								<div>
									<strong>Descrição: </strong>
									{{ r.descricao ? r.descricao : 'Sem descrição' }}
								</div>
							</div>
						</v-card-text>

						<template #append>
							<div class="d-flex">
								<div v-if="isEditingRevisions">
									<ReagendarDialog :revisao="r" :tema_nome="tema?.nome || ''">
										<template #button="reagendaProps">
											<v-btn
												:disabled="r.status === 'REALIZADA'"
												v-bind="reagendaProps"
												icon="edit_calendar"
												color="white"
												variant="text"
											></v-btn>
										</template>
									</ReagendarDialog>
									<v-btn
										@click="promptToDelete(r)"
										icon="delete"
										color="white"
										variant="text"
									></v-btn>
								</div>
								<div v-else>
									<v-btn
										:disabled="r.status === 'REALIZADA'"
										:icon="chooseIcon(r.status)"
										color="white"
										variant="text"
										@click="startTimer(r)"
									></v-btn>
								</div>
							</div>
						</template>
					</v-card>
				</v-list-item>
			</v-list>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn variant="text" @click="dialog = false">Fechar</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>

	<ConfirmDialog ref="confirmDialog" />
	<TimerDialog ref="timerDialog" />
</template>

<style scoped>
.rev-card-item {
	display: flex;
	flex-direction: row-reverse;
}

.theme-subtitle {
	margin-bottom: 1vh;
}

.rev-label {
	font-weight: bold;
}
</style>
