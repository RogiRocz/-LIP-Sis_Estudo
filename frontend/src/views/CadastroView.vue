<template>
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

<script setup lang="ts">
import AuthComponent from '@/components/AuthComponent.vue'
import { AuthInput } from '@/utils/authInputs'
import { useUserStore } from '@/stores/useUserStore'
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

const nome = ref('')
const email = ref('')
const senha = ref('')
const confirmarSenha = ref('')

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
	},
	{
		name: 'confirmar senha',
		type: 'password',
		placeholder: 'Confirmar senha',
		model: confirmarSenha,
		icon: 'password_2',
		rules: [required, passwordMatch(senha)],
	},
]

const router = useRouter()
const userStore = useUserStore()
const { loading } = storeToRefs(userStore)
const { setToken, setUser } = userStore

async function handleSubmit() {
	try {
		loading.value = true
		const response = await register({
			nome: nome.value,
			email: email.value,
			senha: senha.value,
			confirmar_senha: confirmarSenha.value,
		})

		if (response && response.token) {
			setToken(response.token)
			setUser(response.user)

			router.push({ name: 'disciplina' })
		}
	} catch (error) {
		console.error('Falha ao criar usuário:', error)
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
