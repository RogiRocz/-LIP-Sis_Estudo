<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader :pageTitle="name" :pageDescription="description" />
			<div class="reports">
				<!-- <h1>Relatórios</h1> -->
				<!-- <p class="subtitle">Acompanhe seu desempenho e evolução</p> -->

				<p v-if="loading">Carregando dados...</p>
				<p v-if="error" class="error">{{ error }}</p>

				<div v-if="!loading && !error" class="grid">
					<div class="card highlight">
						<h3>Total estudado</h3>
						<span class="big">{{ totalHours }}h</span>
					</div>

					<div class="card">
						<h3>Revisões</h3>
						<Pie :data="pieData" />
					</div>

					<div class="card wide">
						<h3>Horas por disciplina</h3>
						<Bar :data="barData" />
					</div>
				</div>
			</div>
		</template>
	</ViewContainer>
</template>

<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { ref, computed, onMounted } from 'vue'
import { Pie, Bar } from 'vue-chartjs'
import { useTheme } from 'vuetify'
import {
	Chart as ChartJS,
	ArcElement,
	BarElement,
	CategoryScale,
	LinearScale,
	Tooltip,
	Legend,
} from 'chart.js'

ChartJS.register(
	ArcElement,
	BarElement,
	CategoryScale,
	LinearScale,
	Tooltip,
	Legend,
)

const theme = useTheme()

const loading = ref(true)
const error = ref(null)
const sessions = ref([])

const fetchReports = async () => {
	try {
		loading.value = true
		const res = await fetch('/api/study-reports')
		if (!res.ok) throw new Error('Erro ao buscar dados')

		sessions.value = [
			{
				id: 1,
				subject: 'Matemática',
				studyMinutes: 90,
				revisionsDone: 3,
				revisionsPending: 2,
			},
			{
				id: 2,
				subject: 'Portugues',
				studyMinutes: 30,
				revisionsDone: 5,
				revisionsPending: 3,
			},
		]
	} catch (e) {
		error.value = e.message
	} finally {
		loading.value = false
	}
}

onMounted(fetchReports)

const totalMinutes = computed(() =>
	sessions.value.reduce((sum, s) => sum + s.studyMinutes, 0),
)

const totalHours = computed(() => (totalMinutes.value / 60).toFixed(1))

const revisionsDone = computed(() =>
	sessions.value.reduce((sum, s) => sum + s.revisionsDone, 0),
)

const revisionsPending = computed(() =>
	sessions.value.reduce((sum, s) => sum + s.revisionsPending, 0),
)

const pieData = computed(() => {
	const currentColors = theme.current.value.colors

	return {
		labels: ['Concluídas', 'Pendentes'],
		datasets: [
			{
				data: [revisionsDone.value, revisionsPending.value],

				backgroundColor: [currentColors.primary, currentColors.secondary],
				borderWidth: 0,
			},
		],
	}
})

const barData = computed(() => {
	const currentColors = theme.current.value.colors

	return {
		labels: sessions.value.map((s) => s.subject),
		datasets: [
			{
				label: 'Horas de estudo',

				data: sessions.value.map((s) =>
					Number((s.studyMinutes / 60).toFixed(2)),
				),

				backgroundColor: currentColors.secondary,
			},
		],
	}
})

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'relatorios'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')
</script>

<!-- rgb(var(--v-theme-app-bar-gradient-start)), -->
<!-- rgb(var(--v-theme-app-bar-gradient-end)) -->
<style scoped>
.reports {
	min-height: 100vh;
	padding: 32px;
	/* background: radial-gradient(circle at top left, #1c1c2b, #0b0b0f); */
	color: rgb(var(--v-theme-secondary));
	font-family: 'Inter', system-ui, sans-serif;
}

h1 {
	font-size: 28px;
	margin-bottom: 4px;
}

.subtitle {
	color: rgb(var(--v-theme-primary));
	margin-bottom: 32px;
}

.grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	gap: 24px;
}

.card {
	background: rgb(var(--v-theme-card));
	border-radius: 16px;
	padding: 20px;
	backdrop-filter: blur(8px);
}

.card.highlight {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.card.wide {
	grid-column: span 2;
}

.big {
	font-size: 42px;
	font-weight: 600;
	margin-top: 8px;
	color: rgb(var(--v-theme-primary));
}

.error {
	color: rgb(var(--v-theme-error));
}
</style>
