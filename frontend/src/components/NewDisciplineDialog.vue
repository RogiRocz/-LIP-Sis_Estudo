<script setup lang="ts">
import { required } from '@/utils/rulesAuth'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useAprendizadoStore } from '@/stores/useAprendizadoStore'
import { createDisciplina } from '@/api/disciplina'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

const dialog = ref(false)
const loading = ref(false)
const form = ref()
const nome = ref('')
const descricao = ref('')
const cor = ref('')

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const aprendizadoStore = useAprendizadoStore()

async function handleCreation() {
	try {
		loading.value = true

		const { valid } = await form.value.validate()

		if (!valid) {
			addMessage({ text: 'Preencha todos os campos', color: 'error' })
			return
		}

		const response = await createDisciplina({
			nome: nome.value,
			cor: cor.value,
			descricao: descricao.value,
		})		

		form.value.reset()
		dialog.value = false

		addMessage({ text: 'Disciplina criada com sucesso', color: 'success' })
	} catch (error) {
		console.log('Erro ao criar disciplina: ', error)
		addMessage({ text: 'Erro ao criar disciplina', color: 'error' })
	} finally {
		loading.value = false
	}
}
</script>

<template>
	<v-dialog v-model="dialog" max-width="50vw" scrollable>
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>
		<v-card variant="flat" color="card" rounded="lg" class="pa-2">
			<v-card-title>Nova disciplina</v-card-title>
			<v-card-subtitle
				>Crie uma nova disciplina para organizar seus estudos</v-card-subtitle
			>
			<v-card-text>
				<v-form ref="form">
					<span class="input-title">Nome da disciplina</span>
					<v-text-field
						v-model="nome"
						placeholder="Ex.: Matemática, Estrutura de dados"
						variant="plain"
						:rules="[required]"
						required
					></v-text-field>
					<span class="input-title">Descrição da disciplina (opcional)</span>
					<v-text-field
						v-model="descricao"
						placeholder="Ex.: Estudos sobre a história moderna"
						variant="plain"
					></v-text-field>
					<span class="input-title">Cor da disciplina</span>
					<v-color-picker
						bg-color="card"
						flat
						v-model="cor"
						hide-inputs
						hide-sliders
						hide-eye-dropper
						hide-canvas
						show-swatches
					></v-color-picker>
				</v-form>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn variant="outlined" @click="dialog = false">Cancelar</v-btn>
				<v-btn
					variant="outlined"
					type="submit"
					:loading="loading"
					@click="handleCreation"
					>Salvar</v-btn
				>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<style scoped>
/* .v-card {
	background-color: rgb(var(--v-theme-card));
	color: rgb(var(--v-theme-secondary));
} */

.input-title {
	display: inline-block;
	margin: 1vh 0;
}
</style>
