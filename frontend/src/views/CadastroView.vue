<template>
	<AuthComponent
		title="Criar conta"
		subtitle="Preencha os dados para começar"
		:inputs="inputs"
	>
	</AuthComponent>
</template>

<script setup lang="ts">
import AuthComponent from '@/components/AuthComponent.vue'
import { AuthInput } from '@/utils/authInputs'
import { ref } from 'vue'

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
	},
	{
		name: 'email',
		type: 'email',
		placeholder: 'E-mail',
		model: email,
        icon: 'mail',
	},
	{
		name: 'senha',
		type: 'password',
		placeholder: 'Senha',
		model: senha,
        icon: 'password_2',
	},
	{
		name: 'confirmar senha',
		type: 'password',
		placeholder: 'Confirmar senha',
		model: confirmarSenha,
        icon: 'password_2',
	},
]
</script>

<style scoped></style>
