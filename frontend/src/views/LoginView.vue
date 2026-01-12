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

// LoginView.vue
async function handleSubmit() {
    try {
        loading.value = true
        
        // 1. Login no seu Backend (Prioridade máxima)
        const response = await login({ 
            email: email.value, 
            senha: senha.value // Aqui deve ser '123456'
        })

        if (response && response.token) {
            setToken(response.token)
            setUser(response.user)

            // 2. Tenta conectar ao Supabase (Opcional para o sistema rodar)
            const { error: sbError } = await supabase.auth.signInWithPassword({
                email: email.value,
                password: senha.value, // Deve ser a senha pura '123456'
            })

            if (sbError) {
                console.warn('Realtime não disponível:', sbError.message)
                addMessage({ 
                    text: 'Aviso: Funções de tempo real desativadas (Senha do servidor de sync pode estar diferente).', 
                    color: 'warning' 
                })
            } else {
                const aprendizadoStore = useAprendizadoStore()
                await aprendizadoStore.setupRealtime()
            }

            router.push({ name: 'home' })
        }
    } catch (error: any) {
        addMessage({ text: error.message || 'Erro ao logar', color: 'error' })
    } finally {
        loading.value = false
    }
}
</script>

<style scoped></style>
