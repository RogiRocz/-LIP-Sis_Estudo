<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import { usePainelStore } from '@/stores/usePainelStore'
import { storeToRefs } from 'pinia'
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { getEstatisticas, getEvolucaoSemanal } from '@/api/painel'

const userStore = useUserStore()
const { user, isDarkTheme } = storeToRefs(userStore)
const painelStore = usePainelStore()
const { needReload } = storeToRefs(painelStore)

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'home'),
)

watch(needReload, (value) => {
	if (value) {
		fetchDashboardData()
	}
})


const loading = ref(false)
const themeColor = computed(() => (isDarkTheme.value ? 'secondary' : 'primary'))

const estatisticasReais = ref({
	total_disciplinas: 0,
	total_temas: 0,
	total_revisoes: 0,
	revisoes_hoje: 0,
})

const evolucaoSemanal = ref<
	Array<{ data: string; revisoes_realizadas: number }>
>([])

const stats = computed(() => [
	{
		label: 'DISCIPLINAS',
		value: estatisticasReais.value.total_disciplinas,
		icon: 'book',
	},
	{
		label: 'TEMAS CRIADOS',
		value: estatisticasReais.value.total_temas,
		icon: 'layers',
	},
	{
		label: 'TOTAL REVISÕES',
		value: estatisticasReais.value.total_revisoes,
		icon: 'history',
	},
	{
		label: 'PARA HOJE',
		value: estatisticasReais.value.revisoes_hoje,
		icon: 'today',
	},
])

async function fetchDashboardData() {
	loading.value = true
	try {
		const est = await getEstatisticas()
		estatisticasReais.value = est

		const evolucao = await getEvolucaoSemanal()
		evolucaoSemanal.value = evolucao
	} catch (error) {
		console.error('Erro ao buscar dados do painel:', error)
	} finally {
		loading.value = false
	}
}

const graficoAlturas = computed(() => {
	if (!evolucaoSemanal.value.length) {
		return [40, 75, 45, 95, 65, 30, 80]
	}

	const maxRevisoes = Math.max(
		...evolucaoSemanal.value.map((item) => item.revisoes_realizadas),
	)

	return evolucaoSemanal.value.map((item) => {
		if (maxRevisoes === 0) return 10
		return Math.max(10, (item.revisoes_realizadas / maxRevisoes) * 100)
	})
})

const diasSemana = computed(() => {
	if (!evolucaoSemanal.value.length) {
		return ['SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB', 'DOM']
	}

	return evolucaoSemanal.value.map((item) => {
		const data = new Date(item.data + 'T00:00:00')
		return data.toLocaleDateString('pt-BR', { weekday: 'short' }).toUpperCase()
	})
})

onMounted(() => {
	fetchDashboardData()	
})
</script>

<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader
				:pageTitle="currentView?.name"
				:pageDescription="`Olá, ${user?.nome}. Acompanhe seu progresso.`"
			/>
			<MainContainer>
				<template #main-content>
					<v-row class="mb-6">
						<v-col
							v-for="item in stats"
							:key="item.label"
							cols="12"
							sm="6"
							md="3"
						>
							<v-card elevation="4" class="rounded-xl pa-4" :color="themeColor">
								<div class="d-flex align-center mb-4 text-white opacity-90">
									<v-icon
										:icon="item.icon"
										size="x-small"
										class="mr-2"
									></v-icon>
									<span
										class="text-overline font-weight-bold"
										style="letter-spacing: 1px !important"
										>{{ item.label }}</span
									>
								</div>

								<v-sheet
									class="pa-2 rounded-lg glass-display d-flex justify-center align-center"
								>
									<span class="text-h4 font-weight-black">{{
										item.value
									}}</span>
								</v-sheet>
							</v-card>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols="12" md="8">
							<v-card
								elevation="4"
								class="rounded-xl pa-6"
								:color="themeColor"
								height="100%"
							>
								<v-card-title class="px-0 font-weight-bold text-white mb-4"
									>Evolução de Estudos</v-card-title
								>

								<v-sheet class="pa-6 rounded-xl glass-display" height="220">
									<div
										v-if="loading"
										class="d-flex align-center justify-center h-100"
									>
										<v-progress-circular
											indeterminate
											color="white"
										></v-progress-circular>
									</div>
									<div
										v-else
										class="d-flex align-end justify-space-between h-100"
									>
										<div
											v-for="(altura, i) in graficoAlturas"
											:key="i"
											:style="{
												height: altura + '%',
												width: '12%',
												background: 'white',
												borderRadius: '6px 6px 2px 2px',
												opacity: 0.9,
											}"
											:title="`${diasSemana[i]}: ${evolucaoSemanal[i]?.revisoes_realizadas || 0} revisões`"
										></div>
									</div>
								</v-sheet>

								<div
									class="d-flex justify-space-between text-caption mt-4 text-white opacity-80"
								>
									<span v-for="dia in diasSemana" :key="dia">{{ dia }}</span>
								</div>
							</v-card>
						</v-col>

						<v-col cols="12" md="4">
							<v-card
								class="botao-gradient text-white pa-8 rounded-xl d-flex flex-column"
								elevation="6"
								height="100%"
							>
								<div class="text-h5 font-weight-bold mb-4">StudyFlow</div>
								<p class="text-body-2 mb-6 opacity-90">
									Sua jornada de aprendizado organizada com ciência e
									tecnologia.
									{{
										user?.nome
											? `Continue assim, ${user.nome.split(' ')[0]}!`
											: 'Bons estudos!'
									}}
								</p>

								<div class="mb-4">
									<div class="d-flex align-center mb-2">
										<v-icon
											icon="trending_up"
											class="mr-2"
											size="small"
										></v-icon>
										<span class="text-caption">Progresso esta semana:</span>
									</div>
									<v-progress-linear
										:model-value="estatisticasReais.revisoes_hoje > 0 ? 100 : 0"
										color="white"
										height="8"
										rounded
									></v-progress-linear>
									<div class="text-caption mt-1">
										{{ estatisticasReais.revisoes_hoje }} revisões para hoje
									</div>
								</div>

								<v-spacer></v-spacer>
								<v-divider dark class="mb-6 opacity-20"></v-divider>
								<div class="d-flex align-center">
									<v-icon icon="lightbulb" class="mr-2" size="small"></v-icon>
									<span class="text-caption font-italic"
										>"A constância vence o talento."</span
									>
								</div>
							</v-card>
						</v-col>
					</v-row>
				</template>
			</MainContainer>
		</template>
	</ViewContainer>
</template>

<style scoped>
.glass-display {
	background-color: rgba(255, 255, 255, 0.2) !important;
	backdrop-filter: blur(4px);
	color: white !important;
}

.botao-gradient {
	background: linear-gradient(
		135deg,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
}

.v-card {
	color: white !important;
	transition: transform 0.2s ease;
}

.v-card:hover {
	transform: translateY(-4px);
}
</style>
