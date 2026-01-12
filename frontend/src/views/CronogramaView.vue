<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { useUserStore } from '@/stores/useUserStore'

import { getDisciplinas } from '@/api/disciplina'
import { getTemas } from '@/api/tema'
import { getRevisoes } from '@/api/revisao'

import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import MainContainer from '@/components/MainContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { useTheme } from 'vuetify'

const aprendizadoStore = useAprendizadoStore()
const userStore = useUserStore()
const { isDarkTheme } = storeToRefs(userStore)
const { disciplinas, temas, revisoes, loading } = storeToRefs(aprendizadoStore)

const calendar = ref<any>(null)
const calendarKey = ref(0)
const type = ref<'month' | 'week'>('month')

const focus = ref(new Date())

const themeColor = computed(() => (isDarkTheme.value ? 'secondary' : 'primary'))

const dayDialog = ref(false)
const selectedDayRevisions = ref<any[]>([])
const selectedDateStr = ref('')
const activeDisciplinaId = ref<number | null>(null)
const disciplinaDialog = ref(false)
const disciplinaSelecionada = ref<any>(null)

const theme = useTheme()

const calendarBackground = computed(() => {
	const current = theme?.global?.current?.value
	if (!current || !current.colors) {
		return isDarkTheme.value ? '#1E1E1E' : '#FFFFFF'
	}

	return isDarkTheme.value ? current.colors.secondary : current.colors.primary
})

const next = () => {
	calendar.value?.next()
	sincronizarFoco()
}
const prev = () => {
	calendar.value?.prev()
	sincronizarFoco()
}

const sincronizarFoco = () => {
	setTimeout(() => {
		if (calendar.value && calendar.value.displayValue) {
			focus.value = new Date(calendar.value.displayValue)
		}
	}, 50)
}

const irParaHoje = () => {
	focus.value = new Date()
}

const sincronizarDados = async () => {
	try {
		aprendizadoStore.loading = true
		const discData = await getDisciplinas({ page: 1, size: 100 })
		aprendizadoStore.setDisciplinas(discData.items.flat())

		const temasMap = new Map()
		await Promise.all(
			discData.items.flat().map(async (d: any) => {
				const temasData = await getTemas(d.ID)
				temasMap.set(d.ID, temasData.items.flat())
			}),
		)
		aprendizadoStore.setTemas(temasMap)

		const revisoesMap = new Map()
		const revData = await getRevisoes()
		if (revData?.items) {
			revData.items.flat().forEach((rev: any) => {
				if (!revisoesMap.has(rev.tema_id)) revisoesMap.set(rev.tema_id, [])
				revisoesMap.get(rev.tema_id).push(rev)
			})
		}
		aprendizadoStore.setRevisoes(revisoesMap)
	} finally {
		aprendizadoStore.loading = false
	}
}

const events = computed(() => {
	const allEvents: any[] = []
	revisoes.value?.forEach((revisoesArray, temaId) => {
		let temaInfo: any = null
		let disciplinaPai: any = null
		temas.value?.forEach((temasArray) => {
			const t = temasArray.find((tema) => tema.ID === temaId)
			if (t) temaInfo = t
		})
		if (temaInfo)
			disciplinaPai = disciplinas.value?.find(
				(d) => d.ID === temaInfo.disciplina_id,
			)

		revisoesArray.forEach((rev) => {
			const dataValida = new Date(rev.data_prevista)
			if (!isNaN(dataValida.getTime())) {
				allEvents.push({
					title: temaInfo?.nome || 'Revisão',
					start: dataValida,
					end: dataValida,
					color: disciplinaPai?.cor || 'primary',
					raw: rev,
					disciplina: disciplinaPai,
				})
			}
		})
	})
	return allEvents
})

const onDayClick = ({ date }: any) => {
	const clickedDate = new Date(date)
	selectedDateStr.value = clickedDate.toLocaleDateString('pt-BR')
	selectedDayRevisions.value = events.value.filter(
		(e) =>
			new Date(e.start).toLocaleDateString('pt-BR') === selectedDateStr.value,
	)
	dayDialog.value = true
}

const getStatusColor = (status: string) => {
	if (status === 'ATRASADA') return 'error'
	if (status === 'REALIZADA') return 'success'
	return 'warning'
}

const revisoesDaDisciplina = computed(() => {
	if (!disciplinaSelecionada.value) return []
	const idDis = disciplinaSelecionada.value.ID
	const lista: any[] = []
	const temasDaDis = temas.value?.get(idDis) || []
	temasDaDis.forEach((tema) => {
		const revs = revisoes.value?.get(tema.ID) || []
		revs.forEach((r) => lista.push({ ...r, temaNome: tema.nome }))
	})
	return lista.sort(
		(a, b) =>
			new Date(a.data_prevista).getTime() - new Date(b.data_prevista).getTime(),
	)
})

onMounted(() => {
	sincronizarDados()
})
</script>

<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader
				:pageTitle="
					tabsNavigation.find((t) => t.routeName === 'cronograma')?.name
				"
				pageDescription="Ciclos de estudo e revisões agendadas."
			/>

			<MainContainer>
				<template #main-content>
					<v-row>
						<v-col cols="12">
							<v-card
								elevation="4"
								class="rounded-xl overflow-hidden calendar-wrapper"
							>
								<v-toolbar flat :color="themeColor" class="px-4 text-white">
									<v-btn
										variant="elevated"
										:color="calendarBackground"
										class="rounded-lg font-weight-bold"
										@click="irParaHoje"
										>Hoje</v-btn
									>

									<v-btn
										icon="chevron_left"
										variant="text"
										@click="prev"
									></v-btn>

									<v-container width="min-content">
										<v-toolbar-title
											class="text-h6 font-weight-bold text-uppercase"
										>
											{{
												focus.toLocaleString('pt-BR', {
													month: 'long',
													year: 'numeric',
												})
											}}
										</v-toolbar-title>
									</v-container>

									<v-btn
										icon="chevron_right"
										variant="text"
										@click="next"
									></v-btn>

									<v-spacer></v-spacer>

									<v-btn-toggle
										v-model="type"
										mandatory
										variant="flat"
										class="rounded-lg toggle-glass"
									>
										<v-btn
											value="month"
											class="btn-switch px-4"
											:color="
												type === 'month' ? calendarBackground : 'background'
											"
										>
											MÊS
										</v-btn>
										<v-btn
											value="week"
											class="btn-switch px-4"
											:color="
												type === 'week' ? calendarBackground : 'background'
											"
										>
											SEMANA
										</v-btn>
									</v-btn-toggle>
								</v-toolbar>

								<v-calendar
									ref="calendar"
									v-model="focus"
									:type="type"
									:events="events"
									locale="pt-br"
									header-less
									@click:day="onDayClick"
								>
									<template #event="{ event }">
										<div
											class="v-calendar-event-custom"
											:style="{ backgroundColor: event.color }"
											@click.stop="onDayClick({ date: event.start })"
										>
											{{ event.title }}
										</div>
									</template>
								</v-calendar>
							</v-card>
						</v-col>

						<v-col cols="12" class="mt-4">
							<div class="d-flex flex-wrap" style="gap: 12px">
								<v-chip
									v-for="dis in disciplinas"
									:key="dis.ID"
									:color="dis.cor"
									variant="flat"
									class="text-white px-4 font-weight-bold"
									@click="
										((disciplinaSelecionada = dis),
										(disciplinaDialog = true),
										(activeDisciplinaId = dis.ID))
									"
								>
									<v-icon
										start
										:icon="
											activeDisciplinaId === dis.ID
												? 'radio_button_checked'
												: 'radio_button_unchecked'
										"
										size="16"
									></v-icon>
									{{ dis.nome }}
								</v-chip>
							</div>
						</v-col>
					</v-row>

					<v-dialog v-model="dayDialog" max-width="450">
						<v-card class="rounded-xl app-modal-bg">
							<v-card-title class="pa-4 font-weight-bold d-flex align-center">
								{{ selectedDateStr }}
								<v-spacer></v-spacer>
								<v-btn
									icon="close"
									variant="text"
									@click="dayDialog = false"
								></v-btn>
							</v-card-title>
							<v-divider></v-divider>
							<v-card-text class="pa-4">
								<div v-if="selectedDayRevisions.length > 0">
									<v-card
										v-for="(rev, i) in selectedDayRevisions"
										:key="i"
										:color="rev.color"
										variant="flat"
										class="mb-3 rounded-xl text-white pa-4"
									>
										<div class="text-overline opacity-80">
											{{ rev.disciplina?.nome }}
										</div>
										<div class="text-h6 font-weight-bold">{{ rev.title }}</div>
										<v-chip
											size="x-small"
											color="white"
											variant="outlined"
											class="mt-2"
											>{{ rev.raw.status }}</v-chip
										>
									</v-card>
								</div>
								<div v-else class="text-center pa-8 opacity-60 font-italic">
									Nenhum compromisso.
								</div>
							</v-card-text>
						</v-card>
					</v-dialog>

					<v-dialog v-model="disciplinaDialog" max-width="500" scrollable>
						<v-card class="rounded-xl app-modal-bg">
							<v-toolbar
								:color="disciplinaSelecionada?.cor"
								flat
								class="text-white"
							>
								<v-toolbar-title class="font-weight-bold">{{
									disciplinaSelecionada?.nome
								}}</v-toolbar-title>
								<v-btn icon="close" @click="disciplinaDialog = false"></v-btn>
							</v-toolbar>
							<v-card-text class="pa-0">
								<div
									class="list-wrapper"
									v-if="revisoesDaDisciplina.length > 0"
								>
									<v-list
										bg-color="background"
										class="pa-4 bg-transparent"
										lines="two"
									>
										<v-list-item
											v-for="r in revisoesDaDisciplina"
											:key="r.ID"
											class="mb-3 border rounded-xl shadow-sm"
											:class="
												themeColor === 'primary'
													? 'revisao-item-primary'
													: 'revisao-item-secondary'
											"
										>
											<v-list-item-title class="font-weight-bold">{{
												r.temaNome
											}}</v-list-item-title>
											<v-list-item-subtitle
												>Previsão:
												{{
													new Date(r.data_prevista).toLocaleDateString()
												}}</v-list-item-subtitle
											>
											<template #append>
												<v-chip
													size="x-small"
													:color="getStatusColor(r.status)"
													class="font-weight-black text-white px-3"
												>
													{{ r.status }}
												</v-chip>
											</template>
										</v-list-item>
									</v-list>
								</div>
								<div v-else class="pa-12 text-center">
									<v-icon
										size="64"
										color="grey"
										icon="assignment_late"
										class="mb-4"
									></v-icon>
									<p class="text-h6 text-grey">Nada agendado.</p>
								</div>
							</v-card-text>
						</v-card>
					</v-dialog>
				</template>
			</MainContainer>
		</template>
	</ViewContainer>
</template>

<style scoped>
.calendar-wrapper {
	border: 2px solid v-bind('isDarkTheme ? "#1e1e2e" : "#f5f5f5"');
}

:deep(.v-calendar) {
	background-color: v-bind(calendarBackground) !important;

	min-height: 700px;
}

:deep(.v-calendar-month__day) {
	min-height: 120px !important;
}

.toggle-glass {
	background-color: rgba(255, 255, 255, 0.2) !important;
	color: white !important;
}

.v-calendar-event-custom {
	border-radius: 4px;
	font-size: 11px;
	font-weight: bold;
	padding: 2px 6px;
	margin: 1px;
	color: white;
	cursor: pointer;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.app-modal-bg {
	background-color: rgb(var(--v-theme-surface)) !important;
	color: rgb(var(--v-theme-on-surface)) !important;
}

:deep(.v-calendar-month__day--today) {
	background-color: rgba(var(--v-theme-primary), 0.05) !important;
	border: 1px solid rgb(var(--v-theme-primary)) !important;
}

:deep(.v-calendar-weekly__week) {
	background-color: v-bind(calendarBackground);
}

:deep(.v-calendar-weekly .v-calendar-weekly__head-weekday.v-outside) {
	border: v-bind(calendarBackground) 1px solid;
	border-top: 0;

	border-right: 0;
	color: v-bind(calendarBackground);
}

:deep(.v-calendar-weekly__head-weekday.v-past.v-past:not(.v-outside)) {
	background-color: v-bind(calendarBackground);
}

:deep(.v-calendar-weekly__head-weekday.v-present) {
	background-color: v-bind(calendarBackground);
}

:deep(.v-calendar-weekly__head-weekday.v-past.v-outside) {
	border: v-bind(calendarBackground) 1px solid;
	border-top: 0;

	border-right: 0;
	color: v-bind(calendarBackground);
}

:deep(.v-calendar-weekly__day.v-past.v-outside) {
	border: v-bind(calendarBackground) 1px solid;
	border-top: 0;
	border-bottom: 0;
	border-right: 0;
	color: v-bind(calendarBackground);
}

:deep(.text-surface-variant) {
	color: inherit !important;
}

.today-btn {
	color: rgb(var(--v-theme-surface)) !important;
}

.border {
	border: 1px solid rgba(var(--v-border-color), 0.1) !important;
}

:deep(.v-calendar-weekly__container) {
	height: auto !important;
	min-height: 600px;
}

:deep(.v-calendar-weekly__head) {
	background-color: v-bind(calendarBackground);
	color: white;
}

.btn-switch {
	background-color: rgb(var(--v-theme-background));
	color: v-bind(calendarBackground);
	transition: background-color 0.4s ease-in-out;
}

.revisao-item-secondary {
	background-color: rgb(var(--v-theme-secondary)) !important;
	color: rgb(var(--v-theme-background)) !important;
}

.revisao-item-primary {
	background-color: rgb(var(--v-theme-primary)) !important;
	color: rgb(var(--v-theme-background)) !important;
}
</style>
