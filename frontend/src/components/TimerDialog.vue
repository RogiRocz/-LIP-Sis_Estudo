<script setup lang="ts">
import ConfirmDialog from '@/components/ConfirmDialog.vue'

import { computed, ref, watch, onUnmounted } from 'vue'
import { useTimerStore } from '@/stores/useTimerStore'
import { storeToRefs } from 'pinia'
import { concluirRevisao } from '@/api/revisao'
import { useSnackbarStore } from '@/stores/useSnackbarStore'

const timerStore = useTimerStore()
const { revisao, tema } = storeToRefs(timerStore)

const snackbarStore = useSnackbarStore()

const dialog = ref(false)
const lengthInput = ref(1)
const seconds = ref(0)
const minutes = ref(0)
const hours = ref(0)
const choose = ref('selecting_time')
const clock = ref(0)
const confirmDialog = ref<InstanceType<typeof ConfirmDialog> | null>(null)
const isPaused = ref(false)
const tempoDedicadoMinutos = ref()
let timerInterval: any = null

const totalInitialSeconds = ref(0)

const timeInSeconds = computed(() => minutes.value * 60 + hours.value * 3600)

const progressValue = computed(() => {
	if (totalInitialSeconds.value === 0) return 0
	return (clock.value / totalInitialSeconds.value) * 100
})

const alterTime = (amount: number) => {
	let total = timeInSeconds.value + amount * 60

	if (total < 0) total = 0

	seconds.value = total % 60
	hours.value = Math.floor(total / 3600)
	minutes.value = Math.floor((total % 3600) / 60)
	lengthInput.value = hours.value > 0 ? 2 : 1
}

const finalizarEstudo = async () => {
	isPaused.value = true

	const confirmou = await confirmDialog.value?.open(
		'Interromper estudos?',
		'O tempo estudado até agora será contabilizado. Deseja realmente parar?',
		'timer_pause',
	)

	if (confirmou) {
		clearInterval(timerInterval)
		const tempoGastoSegundos = totalInitialSeconds.value - clock.value
		tempoDedicadoMinutos.value = Math.floor(tempoGastoSegundos / 60)

		registrarTempoDedicado()

		clock.value = 0
		totalInitialSeconds.value = 0
		seconds.value = 0
		minutes.value = 0
		hours.value = 0
		isPaused.value = false
		lengthInput.value = 1
		choose.value = 'selecting_time'
		dialog.value = false
	} else {
		isPaused.value = false
	}
}

const tick = () => {
	clearInterval(timerInterval)

	if (clock.value === 0) {
		clock.value = timeInSeconds.value
		totalInitialSeconds.value = clock.value
	}

	if (clock.value > 0) {
		timerInterval = setInterval(() => {
			if (isPaused.value) return

			const tempoGastoSegundos = totalInitialSeconds.value - clock.value
			tempoDedicadoMinutos.value = Math.floor(tempoGastoSegundos / 60)

			if (clock.value > 0) {
				clock.value--
				seconds.value = clock.value % 60
				hours.value = Math.floor(clock.value / 3600)
				minutes.value = Math.floor((clock.value % 3600) / 60)
			} else {
				stopTimer()
			}
		}, 1000)
	}
}

const stopTimer = () => {
	clearInterval(timerInterval)
	if (clock.value <= 0) {
		registrarTempoDedicado()
		choose.value = 'selecting_time'
	}
}

const registrarTempoDedicado = async () => {
	if (tempoDedicadoMinutos.value) {
		if (!revisao.value) {
			snackbarStore.addMessage({
				text: 'Erro ao registrar seu tempo dedicado',
				color: 'warning',
			})
			return
		}

		const revisaoAtualizada = {
			...revisao.value,
			tempo_dedicado: tempoDedicadoMinutos.value,
		}

		const novaRevisao = await concluirRevisao(
			revisao.value?.ID,
			revisaoAtualizada,
		)

		timerStore.setRevisao(novaRevisao)
	} else {
		snackbarStore.addMessage({
			text: 'Você não registrou nenhum tempo dedicado',
			color: 'warning',
		})
	}
}

const comecarEstudar = () => {
	if (minutes.value === 0 && hours.value === 0) return

	choose.value = 'timer'
}

watch(choose, (newVal) => {
	if (newVal === 'timer') tick()
	else clearInterval(timerInterval)
})

watch(dialog, (val) => {
	if (!val) {
		clearInterval(timerInterval)
		isPaused.value = false
		clock.value = 0
		choose.value = 'selecting_time'
	}
})

const fechaDialogo = () => {
	lengthInput.value = 1
	timerStore.clear()
	dialog.value = false
}

const open = () => {
	dialog.value = true
}

defineExpose({ open })

onUnmounted(() => {
	clearInterval(timerInterval)
	lengthInput.value = 1
})
</script>

<template>
	<v-dialog fullscreen v-model="dialog">
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>

		<v-card
			variant="flat"
			color="secondary"
			class="pa-4 d-flex flex-column align-center justify-center"
		>
			<div v-if="tema" class="text-center mb-4">
				<h2 class="text-h5">{{ tema.nome }}</h2>
				<p class="text-subtitle-1">{{ tema.descricao }}</p>
			</div>

			<v-card-title class="text-h5 mb-4">
				{{
					choose === 'selecting_time'
						? 'Quanto tempo você vai estudar?'
						: 'Mantenha o foco'
				}}
			</v-card-title>

			<v-container class="d-flex flex-column align-center">
				<template v-if="choose === 'selecting_time'">
					<v-row justify="center" align="center" class="time-selector mb-6">
						<v-text-field
							bg-color="primary"
							v-show="lengthInput === 2"
							v-model="hours"
							disabled
							variant="outlined"
							density="compact"
							hide-details
							class="time-input"
						></v-text-field>
						<span v-show="lengthInput === 2" class="ml-3 measurement-text"
							>H</span
						>
						<span v-show="lengthInput === 2" class="mx-2 text-h6">:</span>

						<v-text-field
							bg-color="primary"
							v-model="minutes"
							disabled
							variant="outlined"
							density="compact"
							hide-details
							class="time-input"
						></v-text-field>
						<span class="ml-3 measurement-text">Minutos</span>
					</v-row>

					<v-row justify="center" class="gap-2">
						<v-btn
							variant="outlined"
							icon="remove"
							class="mx-1"
							color="on-secondary"
							@click="alterTime(-15)"
							>-15</v-btn
						>
						<v-btn
							variant="outlined"
							icon="remove"
							class="mx-1"
							color="on-secondary"
							@click="alterTime(-5)"
							>-5</v-btn
						>
						<v-btn
							variant="outlined"
							icon="add"
							class="mx-1"
							color="on-secondary"
							@click="alterTime(5)"
							>+5</v-btn
						>
						<v-btn
							variant="outlined"
							icon="add"
							class="mx-1"
							color="on-secondary"
							@click="alterTime(15)"
							>+15</v-btn
						>
					</v-row>
				</template>

				<template v-else>
					<v-progress-circular
						:model-value="progressValue"
						:size="250"
						:width="15"
						color="on-secondary"
						rotate="0"
					>
						<div class="text-center">
							<span class="text-h3 font-weight-bold">
								{{ hours > 0 ? hours + ':' : '' }}
								{{ minutes.toString().padStart(2, '0') }}:
								{{ seconds.toString().padStart(2, '0') }}
							</span>
							<div class="text-caption">RESTANTES</div>
						</div>
					</v-progress-circular>
				</template>
			</v-container>

			<v-card-actions class="mt-10">
				<v-btn
					v-if="choose === 'selecting_time'"
					variant="text"
					@click="fechaDialogo"
					>Fechar</v-btn
				>
				<v-spacer></v-spacer>
				<v-btn
					v-if="choose === 'selecting_time'"
					color="white"
					variant="outlined"
					@click="comecarEstudar"
					>Continuar</v-btn
				>
				<v-btn
					v-if="choose === 'timer'"
					color="error"
					variant="elevated"
					@click="finalizarEstudo"
					>Cancelar</v-btn
				>
				<v-spacer></v-spacer>
				<v-btn
					v-if="choose === 'timer' && !isPaused"
					color="warning"
					variant="elevated"
					@click="isPaused = true"
				>
					Pausar
				</v-btn>

				<v-btn
					v-if="choose === 'timer' && isPaused"
					color="success"
					variant="elevated"
					@click="isPaused = false"
				>
					Retomar Foco
				</v-btn>
			</v-card-actions>
		</v-card>

		<ConfirmDialog ref="confirmDialog" />
	</v-dialog>
</template>

<style scoped>
.v-card {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

.time-selector {
	padding: 20px 0;
}

.time-input {
	width: 70px;
	flex: none;
}

.time-input :deep(input) {
	text-align: center !important;
	font-size: 1.5rem;
	opacity: 1 !important;
	color: inherit !important;
}

.measurement-text {
	font-size: 1.1rem;
	font-weight: 500;
}
</style>
