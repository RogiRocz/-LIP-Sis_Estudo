<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader :pageTitle="name" :pageDescription="description">
				<template #actions>
					<v-btn
						prepend-icon="download"
						color="primary"
						variant="tonal"
						:disabled="loading || sessions.length === 0"
						@click="exportToCSV"
					>
						Exportar CSV
					</v-btn>
				</template>
			</PageHeader>

			<div class="reports">
				<div v-if="loading" class="d-flex justify-center pa-10">
					<v-progress-circular indeterminate color="primary" />
				</div>

				<p v-if="error" class="error">{{ error }}</p>

				<div v-if="!loading && !error" class="grid">
					<div class="card highlight">
						<h3>Total estudado</h3>
						<span class="big">{{ totalHours }}h</span>
						<p class="text-caption">Soma de todos os temas</p>
					</div>

					<div class="card">
						<h3>Status das Revisões</h3>
						<div class="chart-container">
							<Pie :data="pieData" :options="chartOptions" />
						</div>
					</div>

					<div class="card wide">
						<h3>Horas por disciplina</h3>
						<div class="chart-container">
							<Bar :data="barData" :options="chartOptions" />
						</div>
					</div>
				</div>
			</div>
		</template>
	</ViewContainer>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { Pie, Bar } from 'vue-chartjs'
import {
	Chart as ChartJS,
	ArcElement,
	BarElement,
	CategoryScale,
	LinearScale,
	Tooltip,
	Legend,
} from 'chart.js'
import api from '@/api/apiConnect'

ChartJS.register(
	ArcElement,
	BarElement,
	CategoryScale,
	LinearScale,
	Tooltip,
	Legend,
)

const theme = useTheme()
const aprendizadoStore = useAprendizadoStore()

const loading = ref(true)
const error = ref(null)

const sessions = ref<any[]>([])

const fetchReports = async () => {
	try {
		loading.value = true

		const response = await api.get('/painel/relatorio-completo')

		sessions.value = response.data.data
	} catch (e: any) {
		error.value = 'Não foi possível carregar os dados reais.'
		console.error(e)
	} finally {
		loading.value = false
	}
}

onMounted(fetchReports)

const totalHours = computed(() => {
	const totalMinutes = sessions.value.reduce(
		(sum, s) => sum + s.studyMinutes,
		0,
	)
	return (totalMinutes / 60).toFixed(1)
})

const pieData = computed(() => {
	const colors = theme.current.value.colors
	const done = sessions.value.reduce((sum, s) => sum + s.revisionsDone, 0)
	const pending = sessions.value.reduce((sum, s) => sum + s.revisionsPending, 0)

	return {
		labels: ['Concluídas', 'Pendentes'],
		datasets: [
			{
				data: [done, pending],
				backgroundColor: [colors.primary, colors.secondary],
				borderWidth: 0,
			},
		],
	}
})

const barData = computed(() => {
	const colors = theme.current.value.colors
	return {
		labels: sessions.value.map((s) => s.subject),
		datasets: [
			{
				label: 'Horas',
				data: sessions.value.map((s) =>
					Number((s.studyMinutes / 60).toFixed(2)),
				),
				backgroundColor: colors.secondary,
			},
		],
	}
})

const chartOptions = { responsive: true, maintainAspectRatio: false }

const exportToCSV = () => {
	const headers = [
		'Disciplina',
		'Minutos Estudados',
		'Revisões Concluídas',
		'Revisões Pendentes',
	]
	const rows = sessions.value.map((s) => [
		s.subject,
		s.studyMinutes,
		s.revisionsDone,
		s.revisionsPending,
	])

	const csvContent =
		'\uFEFF' +
		[headers.join(','), ...rows.map((row) => row.join(','))].join('\n')
	const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
	const url = URL.createObjectURL(blob)
	const link = document.createElement('a')
	link.href = url
	link.setAttribute(
		'download',
		`relatorio_estudos_${new Date().toLocaleDateString()}.csv`,
	)
	link.click()
}

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'relatorios'),
)
const name = computed(() => currentView.value?.name || 'Relatórios')
const description = computed(
	() => currentView.value?.description || 'Visualize seu progresso',
)
</script>

<style scoped>
.reports {
	padding: 24px;
	color: rgb(var(--v-theme-on-surface));
}

.grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
	gap: 24px;
}

.card {
	background: rgb(var(--v-theme-surface));
	border: 1px solid rgba(var(--v-border-color), 0.12);
	border-radius: 16px;
	padding: 24px;
	min-height: 300px;
	display: flex;
	flex-direction: column;
}

.card.highlight {
	justify-content: center;
	align-items: center;
	text-align: center;
}

.card.wide {
	grid-column: span 2;
}

.chart-container {
	flex-grow: 1;
	position: relative;
	margin-top: 16px;
	min-height: 200px;
}

.big {
	font-size: 56px;
	font-weight: 800;
	color: rgb(var(--v-theme-primary));
}

.error {
	color: rgb(var(--v-theme-error));
	text-align: center;
}

@media (max-width: 960px) {
	.card.wide {
		grid-column: span 1;
	}
}
</style>
