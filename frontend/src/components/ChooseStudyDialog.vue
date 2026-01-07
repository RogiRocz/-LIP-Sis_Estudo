<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { storeToRefs } from 'pinia'
import { Revisao, Tema } from '@/utils/apiTypes'
import { formatarData } from '@/utils/brDateFormat'

const dialog = ref(false)

const appBarStore = useAppBarStore()
const { actionsWidthDialog } = storeToRefs(appBarStore)

const props = defineProps<{
	tema: Tema | null
	revisoes: Revisaoao[] | []
}>()

const chooseIcon = (status: string) => {
	return status === 'REALIZADA' ? 'timer_off' : 'timer_play'
}

const statusPrioridade: Record<string, number> = {
	ATRASADA: 1,
	PENDENTE: 2,
	REALIZADA: 3,
}

const ordenarRevisoes = (a: Revisao, b: Revisao) => {
	const prioridadeA = statusPrioridade[a.status] || 99
	const prioridadeB = statusPrioridade[b.status] || 99

	if (prioridadeA !== prioridadeB) {
		return prioridadeA - prioridadeB
	}

	return (
		new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime()
	)
}

onMounted(() => {
	props.revisoes.sort(ordenarRevisoes)
})
</script>

<template>
	<v-dialog v-model="dialog" :max-width="actionsWidthDialog">
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>
		<v-card scrollable variant="flat" color="card" rounded="lg" class="pa-2">
			<v-card-title>Escolha o que estudar</v-card-title>
			<v-divider></v-divider>
			<v-card-title class="theme-name">{{ tema.nome }}</v-card-title>
			<v-card-subtitle class="theme-subtitle">{{
				tema.descricao
			}}</v-card-subtitle>
			<v-list bg-color="#dddddd" lines="one" rounded="lg">
				<v-list-item v-for="(r, i) in revisoes" :key="i" class="rev-item">
					<v-card
						scrollable
						variant="flat"
						color="primary"
						rounded="lg"
						class="rev-card pa-2"
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
								class="mr-2"
							>
								{{ r.status }}
							</v-chip>
						</template>
						<v-container>
							<v-col>
								<span class="rev-label">Data Prevista: </span>
								<span class="rev-content">{{
									formatarData(r.data_prevista)
								}}</span>
							</v-col>
							<v-col>
								<span class="rev-label">Data Realizada: </span>
								<span class="rev-content">{{
									r.data_realizada ? formatarData(r.data_realizada) : 'Nenhuma'
								}}</span>
							</v-col>
							<v-col>
								<span class="rev-label">Tempo dedicado: </span>
								<span class="rev-content">{{
									r.tempo_dedicado ? r.tempo_dedicado : 'Nenhum'
								}}</span>
							</v-col>
							<v-col>
								<span class="rev-label">Descrição: </span>
								<span class="rev-content">{{
									r.descricao ? r.descricao : 'Nenhuma'
								}}</span>
							</v-col>
						</v-container>

						<template #append>
							<v-btn
								:disabled="r.status === 'REALIZADA'"
								:icon="chooseIcon(r.status)"
								:color="r.status === 'REALIZADA' ? 'grey' : 'white'"
								variant="text"
								size="small"
							>
							</v-btn>
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
</template>

<style scoped>
.theme-subtitle {
	margin-bottom: 1vh;
}

.v-list-item {
	margin: 2vh 0;
}

.v-col {
	padding: 0;
}

.rev-card {
	display: flex;
	flex-direction: row-reverse;
}
</style>
