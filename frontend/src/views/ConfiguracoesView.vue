<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import { useTheme } from 'vuetify'
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'

const userStore = useUserStore()
const { user, isDarkTheme } = storeToRefs(userStore)
const { logout } = userStore
const theme = useTheme()

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'configuracoes'),
)

const themeColor = computed(() => (isDarkTheme.value ? 'secondary' : 'primary'))

const darkModeModel = computed({
	get: () => isDarkTheme.value,
	set: (val) => {
		theme.global.name.value = val ? 'dark' : 'light'
	},
})

const userName = ref(user.value?.nome || '')
const metaDiaria = ref(60)

const handleSeed = () => {}
const handleSave = () => {}
</script>

<template>
	<ViewContainer>
		<template #view-content>
			<PageHeader
				:pageTitle="currentView?.name"
				:pageDescription="currentView?.description"
			/>
			<MainContainer>
				<template #main-content>
					<v-row>
						<v-col cols="12">
							<v-card elevation="2" class="rounded-xl pa-2" :color="themeColor">
								<v-card-title class="d-flex align-center pt-4">
									<v-icon start icon="person_outline"></v-icon> Perfil
								</v-card-title>
								<v-card-text>
									<v-sheet
										class="pa-4 rounded-lg d-flex align-center mb-6 glass-input"
									>
										<span class="font-weight-medium">{{
											user?.nome || 'Usuário de Teste'
										}}</span>
										<v-spacer></v-spacer>
										<v-btn
											variant="text"
											size="small"
											prepend-icon="logout"
											@click="logout"
											class="text-capitalize opacity-80"
											>Sair</v-btn
										>
									</v-sheet>

									<v-text-field
										v-model="userName"
										label="Nome de Usuário"
										variant="solo"
										flat
										density="comfortable"
										class="glass-field"
										persistent-hint
										hint="Como você gostaria de ser chamado?"
									></v-text-field>
								</v-card-text>
							</v-card>
						</v-col>

						<v-col cols="12" md="6">
							<v-card
								elevation="2"
								class="rounded-xl pa-2"
								:color="themeColor"
								height="100%"
							>
								<v-card-title class="d-flex align-center pt-4">
									<v-icon start icon="dark_mode"></v-icon> Aparência
								</v-card-title>
								<v-card-text>
									<div class="d-flex align-center justify-space-between mt-2">
										<div>
											<div class="text-subtitle-1">Tema Escuro</div>
											<div class="text-caption opacity-80">
												Alternar visual da interface
											</div>
										</div>
										<v-switch
											v-model="darkModeModel"
											color="white"
											inset
											hide-details
										></v-switch>
									</div>
								</v-card-text>
							</v-card>
						</v-col>

						<v-col cols="12" md="6">
							<v-card
								elevation="2"
								class="rounded-xl pa-2"
								:color="themeColor"
								height="100%"
							>
								<v-card-title class="d-flex align-center pt-4">
									<v-icon start icon="track_changes"></v-icon> Meta de Estudo
								</v-card-title>
								<v-card-text>
									<v-text-field
										v-model.number="metaDiaria"
										label="Minutos diários"
										type="number"
										variant="solo"
										flat
										density="comfortable"
										class="glass-field"
									></v-text-field>
								</v-card-text>
							</v-card>
						</v-col>

						<v-col cols="12">
							<v-card
								elevation="1"
								class="rounded-xl pa-2"
								:color="themeColor"
								variant="tonal"
							>
								<v-card-text class="d-flex align-center py-2">
									<span class="text-body-2 font-weight-medium"
										>Deseja carregar dados de exemplo?</span
									>
									<v-spacer></v-spacer>
									<v-btn
										:color="themeColor"
										prepend-icon="storage"
										@click="handleSeed"
										variant="elevated"
										>CARREGAR DADOS</v-btn
									>
								</v-card-text>
							</v-card>
						</v-col>
					</v-row>

					<v-row class="mt-8">
						<v-col class="d-flex justify-end">
							<v-btn
								class="botao-gradient px-10"
								size="large"
								@click="handleSave"
								>SALVAR ALTERAÇÕES</v-btn
							>
						</v-col>
					</v-row>
				</template>
			</MainContainer>
		</template>
	</ViewContainer>
</template>

<style scoped>
.glass-input,
:deep(.glass-field .v-field) {
	background-color: rgba(255, 255, 255, 0.2) !important;
	backdrop-filter: blur(4px);
	color: white !important;
	border: none !important;
}

:deep(.v-label) {
	color: rgba(255, 255, 255, 0.9) !important;
}

.botao-gradient {
	background: linear-gradient(
		to right,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
	color: white;
	font-weight: bold;
}
</style>
