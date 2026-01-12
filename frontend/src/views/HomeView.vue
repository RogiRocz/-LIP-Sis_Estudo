<script setup lang="ts">
import { computed, watch } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'

const userStore = useUserStore()
const { user, isDarkTheme } = storeToRefs(userStore)
const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'home'),
)

const themeColor = computed(() => (isDarkTheme.value ? 'secondary' : 'primary'))

const stats = [
	{ label: 'DISCIPLINAS', value: 12, icon: 'book' },
	{ label: 'TEMAS CRIADOS', value: 156, icon: 'layers' },
	{ label: 'TOTAL REVISÕES', value: 475, icon: 'history' },
	{ label: 'PARA HOJE', value: 0, icon: 'today' },
]
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
									<div class="d-flex align-end justify-space-between h-100">
										<div
											v-for="(h, i) in [40, 75, 45, 95, 65, 30, 80]"
											:key="i"
											:style="{
												height: h + '%',
												width: '10%',
												background: 'white',
												borderRadius: '6px 6px 2px 2px',
												opacity: 0.9,
											}"
										></div>
									</div>
								</v-sheet>

								<div
									class="d-flex justify-space-between text-caption mt-4 text-white opacity-80"
								>
									<span
										v-for="d in [
											'SEG',
											'TER',
											'QUA',
											'QUI',
											'SEX',
											'SAB',
											'DOM',
										]"
										:key="d"
										>{{ d }}</span
									>
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
								</p>
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
