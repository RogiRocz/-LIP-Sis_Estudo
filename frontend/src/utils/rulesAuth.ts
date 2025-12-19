import type { Ref } from 'vue'

const required = (value: string): true | string => {
	return !!value || 'Campo obrigatório'
}

const validEmail = (value: string): true | string => {
	const emailRegex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
	return emailRegex.test(value) || 'Formato de email inválido'
}

const validPassword = (value: string): true | string => {
	return value.length >= 6 || 'A senha deve ter no mínimo 6 caracteres'
}

const passwordMatch = (password: Ref<string>) => (value: string): true | string => {
    return value === password.value || 'As senhas não conferem';
}

export { required, validEmail, validPassword, passwordMatch }