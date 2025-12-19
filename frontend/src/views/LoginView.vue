<template>
	<AuthComponent
		title="Bem vindo de volta!"
		subtitle="Entre com suas credenciais para continuar"
		:inputs="inputs"
	>
		<template #submit-form>
			<v-btn type="submit" :loading="loading" @click.prevent="handleSubmit">
				Entrar
			</v-btn>
		</template>

		<template #actions>
			<p align="center">
				Não tem uma conta?
				<router-link :to="{ name: 'cadastro' }">Criar conta</router-link>
			</p>
		</template>
	</AuthComponent>
</template>

<script setup lang="ts">
import { login } from '@/api/auth'
import AuthComponent from '@/components/AuthComponent.vue'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useUserStore } from '@/stores/useUserStore'
import { AuthInput } from '@/utils/authInputs'
import { required, validEmail, validPassword } from '@/utils/rulesAuth'
import { storeToRefs } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vuetify/lib/composables/router.mjs'

const email = ref('')
const senha = ref('')

const showPassword = ref(false)

const inputs: AuthInput[] = [
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
		showPassword,
	},
]

const router = useRouter()

const userStore = useUserStore()
const { loading } = storeToRefs(userStore)
const { setToken, setUser } = userStore

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

async function handleSubmit() {
	try {
		loading.value = true
		const response = await login({
			email: email.value,
			senha: senha.value,
		})

		if (response && response.token) {
			setToken(response.token)
			setUser(response.user)

			router.push({ name: 'home' })
		}
	} catch (error) {
		console.error('Falha ao logar:', error)
		addMessage({ text: error.response.data.detail, color: 'error' })
	} finally {
		loading.value = false
	}
}
</script>

<style scoped>
/* Estilos específicos para LoginView */
</style>
