<template>
	<ViewContainer>
		<template #view-content>
			<AuthComponent
				title="Criar conta"
				subtitle="Preencha os dados para começar"
				:inputs="inputs"
			>
				<template #submit-form>
					<v-btn type="submit" :loading="loading" @click.prevent="handleSubmit">
						Criar Conta
					</v-btn>
				</template>

				<template #actions>
					<p align="center">
						Já tem uma conta?
						<router-link :to="{ name: 'login' }">Faça login</router-link>
					</p>
				</template>
			</AuthComponent>
		</template>
	</ViewContainer>
</template>

<script setup lang="ts">
import AuthComponent from '@/components/AuthComponent.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { AuthInput } from '@/utils/authInputs'
import { useUserStore } from '@/stores/useUserStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import {
	required,
	validEmail,
	validPassword,
	passwordMatch,
} from '@/utils/rulesAuth'
import { register } from '@/api/auth'
import { supabase } from '@/config/supabase'

const nome = ref('')
const email = ref('')
const senha = ref('')
const confirmarSenha = ref('')

const showPassword1 = ref(false)
const showPassword2 = ref(false)

const inputs: AuthInput[] = [
	{
		name: 'nome',
		type: 'text',
		placeholder: 'Nome',
		model: nome,
		icon: 'account_circle',
		rules: [required],
	},
	{
		name: 'email',
		type: 'email',
		placeholder: 'E-mail',
		model: email,
		icon: 'mail',
		rules: [required, validEmail],
	},
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

const router = useRouter()

const userStore = useUserStore()
const { loading } = storeToRefs(userStore)
const { setTokens, setUser } = userStore

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

async function handleSubmit() {
	try {
		loading.value = true

		const response = await register({
			nome: nome.value,
			email: email.value,
			senha: senha.value,
			confirmar_senha: confirmarSenha.value,
		})

		if (response) {
			const {token, refresh_token, expires_at} = response
			setTokens(token, refresh_token, expires_at)
			setUser(response.user)

			addMessage({ text: 'Conta criada com sucesso!', color: 'success' })
			router.push({ name: 'disciplina' })
		}
	} catch (error: any) {
		console.error('Falha ao criar usuário:', error)

		const errorMsg =
			error.response?.data?.detail || error.message || 'Erro ao registrar'
		addMessage({ text: errorMsg, color: 'error' })
	} finally {
		loading.value = false
	}
}
</script>

<style scoped>
a {
	color: rgb(var(--v-theme-primary));
	text-decoration: none;
}
</style>
