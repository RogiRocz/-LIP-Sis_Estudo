<template>
	<ViewContainer>
		<template #view-content>
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
	</ViewContainer>
</template>

<script setup lang="ts">
import { login } from '@/api/auth'
import AuthComponent from '@/components/AuthComponent.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { supabase } from '@/config/supabase'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
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

			// const { data: sessionData, error: errorSupabase } =
			// 	await supabase.auth.setSession({
			// 		access_token: response.token,
			// 		refresh_token: response.token,
			// 	})

			// if (errorSupabase) {
			// 	console.error('Erro detalhado:', errorSupabase)
			// 	console.log('Informações da sessão: ', sessionData)
			// }

			// console.log('Informações da sessão do supabase: ', sessionData)

			const aprendizadoStore = useAprendizadoStore()
			await aprendizadoStore.setupRealtime()

			router.push({ name: 'home' })
		}
	} catch (error) {
		console.error('Falha ao logar:', error)
		const message = error.response?.data?.detail || 'Erro interno no servidor'
		addMessage({ text: message, color: 'error' })
	} finally {
		loading.value = false
	}
}
</script>

<style scoped></style>
