<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import MainContainer from '@/components/MainContainer.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

import { ref, computed, watch, capitalize } from 'vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import { useTheme } from 'vuetify'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { updateProfile } from '@/api/user'
import {
	passwordMatch,
	required,
	validEmail,
	validPassword,
} from '@/utils/rulesAuth'
import { AuthInput } from '@/utils/authInputs'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { generateMockData } from '@/api/seed'

const userStore = useUserStore()
const { user, isDarkTheme, intervalos } = storeToRefs(userStore)
const { logout } = userStore

const snackbarStore = useSnackbarStore()

const theme = useTheme()

const editPerfil = ref(false)
const form = ref()
const formConfirmPass = ref()
const confirmPassDialog = ref(false)
const loading = ref(false)
const senha = ref()
const confirmarSenha = ref()
const showPassword1 = ref(false)
const showPassword2 = ref(false)

const colorBasedInTheme = computed(() => {
	const colors = theme.global.current.value?.colors
	if (!colors) return '#FFFFFF'

	return isDarkTheme.value ? `${colors.secondary}` : `${colors.primary}`
})

const confirmDialogRef = ref<InstanceType<typeof ConfirmDialog> | null>(null)

const authInputs: AuthInput[] = [
	{
		name: 'senha',
		type: 'password',
		placeholder: 'Senha',
		model: senha,
		icon: 'password_2',
		rules: [required, validPassword],
		showPassword: showPassword1,
	},
	{
		name: 'confirmar senha',
		type: 'password',
		placeholder: 'Confirmar senha',
		model: confirmarSenha,
		icon: 'password_2',
		rules: [required, passwordMatch(senha)],
		showPassword: showPassword2,
	},
]

const listaIntervalos = ref<number[]>(
	intervalos.value ? [...intervalos.value] : [1, 7, 14],
)

watch(intervalos, (newVal) => {
	if (newVal) listaIntervalos.value = [...newVal]
})

const adicionarIntervalo = () => {
	listaIntervalos.value.push(
		listaIntervalos.value.slice(-1)
			? listaIntervalos.value.slice(-1)[0] + 7
			: 0,
	)
}

const removerIntervalo = (index: number) => {
	listaIntervalos.value.splice(index, 1)
}

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'configuracoes'),
)

const themeColor = computed(() => (isDarkTheme.value ? 'secondary' : 'primary'))

const darkModeModel = computed({
	get: () => isDarkTheme.value,
	set: async (val) => {
		try {
			userStore.setTheme(val)
		} catch (e) {
			console.error('Erro ao mudar tema, mas mantendo a interface:', e)
		}
	},
})

const userName = ref(user.value?.nome || '')
const userEmail = ref(user.value?.email || '')

const resolvePopup = ref<((value: boolean) => void) | null>(null)

const pedirConfirmacaoSenha = (): Promise<boolean> => {
	confirmPassDialog.value = true
	return new Promise((resolve) => {
		resolvePopup.value = resolve
	})
}

const confirmarCredenciais = async () => {
	const { valid } = await formConfirmPass.value.validate()

	if (valid) {
		confirmPassDialog.value = false
		resolvePopup.value?.(true)
	}
}

const cancelarCredenciais = () => {
	confirmPassDialog.value = false
	resolvePopup.value?.(false)
}

const handleSeed = async () => {
	const confirmed = await confirmDialogRef.value?.open(
		'Carregar Dados de Exemplo',
		'Isso criará disciplinas, temas e revisões fictícias para você explorar a aplicação. Deseja continuar?',
		'database',
	)

	if (confirmed) {
		loading.value = true
		try {
			const result = await generateMockData({
				num_disciplinas: 5,
				num_temas_por_disciplina: 3,
				dias_retroceder: 180,
			})

			snackbarStore.addMessage({
				text: `Dados criados: ${result.disciplinas_criadas} disciplinas, ${result.temas_criados} temas, ${result.revisoes_criadas} revisões`,
				color: 'success',
			})

			// Força recarregar os dados da aplicação
			window.location.reload()
		} catch (error: any) {
			console.error('Erro ao gerar dados:', error)
			snackbarStore.addMessage({
				text: error.message || 'Erro ao gerar dados de exemplo',
				color: 'error',
			})
		} finally {
			loading.value = false
		}
	}
}

const handleSave = async () => {
	const { valid: formPrincipalValido } = await form.value.validate()
	if (!formPrincipalValido) return

	const confirm = await confirmDialogRef.value?.open(
		'Confirme suas alterações',
		'Certeza que deseja alterar essas informações?',
		'person_edit',
	)

	if (confirm) {
		const senhaConfirmada = await pedirConfirmacaoSenha()

		if (senhaConfirmada) {
			loading.value = true
			formConfirmPass.value.reset()

			try {
				const intervalosOrdenados = listaIntervalos.value
					.filter((n) => n > 0)
					.sort((a, b) => a - b)

				const response = await updateProfile({
					nome: userName.value,
					email: userEmail.value,
					ui_theme: theme.global.name.value,
					intervalo_revisoes: intervalosOrdenados,
				})

				userStore.setUser(response)
				userStore.updateTheme(response.ui_theme)
				editPerfil.value = false
				snackbarStore.addMessage({
					text: 'Configurações do usário atualizadas',
					color: 'success',
				})
			} catch (error) {
				console.error('Erro ao atualizar:', error)
			} finally {
				loading.value = false
			}
		}
	}
}

watch(
	user,
	(newUser) => {
		if (newUser) {
			userName.value = newUser.nome
			userEmail.value = newUser.email
		}
	},
	{ immediate: true },
)
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
						<v-col cols="12" md="6">
							<v-card elevation="2" class="rounded-xl pa-2" :color="themeColor">
								<v-card-title class="d-flex align-center pt-4">
									<v-icon start icon="person_outline"></v-icon> Perfil

									<v-spacer></v-spacer>
									<v-btn
										color="background"
										:icon="editPerfil ? 'edit_off' : 'edit'"
										size="small"
										compact
										@click="editPerfil = !editPerfil"
									>
									</v-btn>
								</v-card-title>

								<v-card-text>
									<v-sheet
										width="100%"
										class="pa-4 rounded-lg d-flex align-center mb-6 glass-input"
									>
										<span class="font-weight-medium">{{
											user?.nome || 'Usuário de Teste'
										}}</span>
										<v-spacer></v-spacer>
										<v-btn
											variant="text"
											size="small"
											color="error"
											prepend-icon="logout"
											@click="logout"
											class="text-capitalize opacity-80"
											>Sair</v-btn
										>
									</v-sheet>

									<v-form ref="form">
										<v-text-field
											:disabled="!editPerfil"
											v-model="userName"
											label="Nome de Usuário"
											variant="solo"
											flat
											density="comfortable"
											class="mt-4 mb-4 glass-field"
											persistent-hint
											:rules="[required]"
											:hint="
												editPerfil ? 'Como você gostaria de ser chamado?' : ''
											"
										></v-text-field>

										<v-text-field
											:disabled="!editPerfil"
											v-model="userEmail"
											label="Email"
											variant="solo"
											flat
											density="comfortable"
											class="mt-4 mb-4 glass-field"
											persistent-hint
											:rules="[required, validEmail]"
											:hint="editPerfil ? 'Vai mudar o email?' : ''"
										></v-text-field>
									</v-form>
								</v-card-text>
							</v-card>
						</v-col>

						<v-col class="section" cols="12" md="6">
							<v-col>
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

							<v-col>
								<v-card
									elevation="1"
									class="d-flex rounded-xl pa-2"
									:color="themeColor"
									variant="tonal"
									height="100%"
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
						</v-col>

						<v-col cols="12">
							<v-card elevation="2" class="rounded-xl pa-2" :color="themeColor">
								<v-card-title class="d-flex align-center pt-4">
									<v-icon start icon="update"></v-icon> Ciclos de Revisão Padrão
									<v-spacer></v-spacer>
									<v-btn
										icon="add"
										variant="elevated"
										size="x-small"
										color="white"
										class="text-primary"
										@click="adicionarIntervalo"
									></v-btn>
								</v-card-title>

								<v-card-text>
									<p class="text-caption mb-4 opacity-90">
										Ajuste os dias das revisões automáticas (ex: 1º dia, 7º
										dia...).
									</p>

									<v-row dense>
										<v-col
											v-for="(dias, index) in listaIntervalos"
											:key="index"
											cols="6"
											sm="4"
											md="2"
										>
											<v-text-field
												v-model.number="listaIntervalos[index]"
												type="number"
												suffix="d"
												variant="solo"
												flat
												density="compact"
												class="glass-field"
												hide-details
											>
												<template #append-inner>
													<v-icon
														icon="close"
														size="14"
														class="cursor-pointer"
														@click="removerIntervalo(index)"
													></v-icon>
												</template>
											</v-text-field>
										</v-col>
									</v-row>

									<div class="mt-6 pa-4 rounded-lg glass-input">
										<div class="text-overline mb-2">Fluxo de Memória</div>
										<div class="d-flex align-center flex-wrap" style="gap: 8px">
											<v-chip
												size="small"
												color="white"
												variant="flat"
												class="text-primary"
												>Estudo</v-chip
											>
											<template
												v-for="(dias, i) in listaIntervalos"
												:key="'step-' + i"
											>
												<v-icon
													icon="chevron_right"
													size="small"
													color="white"
												></v-icon>
												<v-chip size="small" color="white" variant="outlined"
													>{{ dias }}d</v-chip
												>
											</template>
										</div>
									</div>
								</v-card-text>
							</v-card>
						</v-col>
					</v-row>

					<v-row class="mt-8">
						<v-col class="d-flex justify-end">
							<v-btn
								class="botao-gradient px-10"
								size="large"
								:loading="loading"
								@click="handleSave"
								>SALVAR ALTERAÇÕES</v-btn
							>
						</v-col>
					</v-row>
				</template>
			</MainContainer>
		</template>
	</ViewContainer>

	<v-dialog
		v-model="confirmPassDialog"
		max-width="75vw"
		persistent
		scrim="primary"
	>
		<v-card class="dialog-pass" color="background">
			<v-card-title :style="{ color: colorBasedInTheme }"
				>Confirme suas credenciais</v-card-title
			>
			<v-form ref="formConfirmPass" validate-on="submit">
				<div v-for="(input, i) in authInputs" :key="i">
					<span :style="{ color: colorBasedInTheme }">{{
						capitalize(input.name)
					}}</span>
					<v-text-field
						v-if="input.type != 'password'"
						clearable
						clear-icon="close"
						persistent-clear
						:glow="true"
						variant="filled"
						class="input"
						:type="input.type"
						:prepend-inner-icon="input.icon"
						:placeholder="input.placeholder"
						v-model="input.model.value"
						:rules="input.rules"
					>
					</v-text-field>
					<v-text-field
						v-else
						clearable
						clear-icon="close"
						persistent-clear
						:append-inner-icon="
							input.showPassword.value ? 'visibility' : 'visibility_off'
						"
						:glow="true"
						variant="filled"
						class="input"
						:type="input.showPassword.value ? 'text' : 'password'"
						:prepend-inner-icon="input.icon"
						:placeholder="input.placeholder"
						v-model="input.model.value"
						:rules="input.rules"
						@click:append-inner="
							input.showPassword.value = !input.showPassword.value
						"
					>
					</v-text-field>
				</div>
				<v-card-actions>
					<v-btn @click="cancelarCredenciais">Cancelar</v-btn>

					<v-btn
						class="botao-gradient"
						:loading="loading"
						@click="confirmarCredenciais"
					>
						Confirmar
					</v-btn>
				</v-card-actions>
			</v-form>
		</v-card>
	</v-dialog>

	<ConfirmDialog ref="confirmDialogRef" />
</template>

<style scoped>
.glass-input,
:deep(.glass-field .v-field) {
	background-color: rgba(255, 255, 255, 0.2) !important;
	backdrop-filter: blur(4px);
	color: white !important;
	border: none !important;
	width: fit-content;
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

.section {
	display: flex;
	flex-direction: column;
	padding: 0;
}

.v-card-actions {
	justify-content: flex-end;
}

.dialog-pass {
	padding: 1vw;
}
</style>
