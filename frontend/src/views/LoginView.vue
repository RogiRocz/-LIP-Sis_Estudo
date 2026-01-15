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
const { setTokens, setUser } = userStore

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

async function handleSubmit() {
	try {
		loading.value = true

		const response = await login({
			email: email.value,
			senha: senha.value,
		})

		if (response) {
			const { token, refresh_token, expires_at } = response
			setTokens(token, refresh_token, expires_at)
			setUser(response.user)

			const { data, error: sbError } = await supabase.auth.setSession({
				access_token: token,
				refresh_token: refresh_token,
			})

			console.log('Dados pra debug: ', {
				response,
				data,
			})

			if (sbError) {
				console.error(
					'Erro detalhado do Supabase:',
					sbError.status,
					sbError.message,
				)
				const session = await supabase.auth.signInWithPassword({
					email: email.value,
					password: senha.value,
				})
				console.log('Nova tentiva de conexão de sessão: ', session)

				if (session.error) {
					addMessage({
						text: 'Aviso: Funções de tempo real desativadas.',
						color: 'warning',
					})
				}
			} else if (data.session) {
				console.log('Sessão Supabase iniciada')
				console.log('Info da sessão do supabase: ', data.session)
			}

			router.replace({ name: 'home' })
		}
	} catch (error: any) {
		addMessage({
			text: error.response.data.detail || 'Erro ao logar',
			color: 'error',
		})
	} finally {
		loading.value = false
	}
}
</script>

<style scoped></style>
