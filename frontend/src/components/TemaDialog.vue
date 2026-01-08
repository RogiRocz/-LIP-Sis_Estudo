<script setup lang="ts">
import { createTema, updateTema } from '@/api/tema'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useUserStore } from '@/stores/useUserStore'
import { Revisao } from '@/utils/apiTypes'
import { required } from '@/utils/rulesAuth'
import { storeToRefs } from 'pinia'
import { computed, ref, watch } from 'vue'

const dialog = ref(false)
const loading = ref(false)
const form = ref()
const nome = ref('Um tema qualquer')
const descricao = ref('Descricao boa')
const id = ref(null)
const id_disciplina = ref(null)

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const appBarStore = useAppBarStore()
const { actionsWidthDialog } = storeToRefs(appBarStore)

const { getUser } = useUserStore()
const { intervalo_revisoes } = getUser
const intervalo = ref<number[]>(intervalo_revisoes)

const props = defineProps<{
	title: string
	subtitle: string
	whichFuncToCall: string
	initialData?: any
}>()

const isEditing = computed(() => props.whichFuncToCall === 'update')

function calcDays(r: Revisao) {
	const dataRev = new Date(r.data_prevista).getTime()
	const hoje = new Date().getTime()
	const diff = dataRev - hoje
	const days = Math.ceil(diff / (1000 * 60 * 60 * 24))
	return days
}

watch(
	() => dialog.value,
	(isOpen) => {
		if (!isOpen) return

		if (isOpen && props.whichFuncToCall === 'update' && props.initialData) {
			nome.value = props.initialData.nome
			descricao.value = props.initialData.descricao
			id.value = props.initialData.id || props.initialData.ID
			id_disciplina.value = props.initialData.id_disciplina

			const revisoes: Revisao[] = props.initialData.revisoes
			if (revisoes && revisoes.length > 0) {
				intervalo.value = revisoes
					.filter((r) => r.status !== 'REALIZADA')
					.map((r) => calcDays(r))

				intervalo.value.sort((a, b) => a - b)
			}
		} else {
			id_disciplina.value = props.initialData.id_disciplina
			nome.value = ''
			descricao.value = ''
		}
	},
)

async function handleClick() {
	try {
		loading.value = true

		const { valid } = await form.value.validate()

		if (!valid) {
			addMessage({ text: 'Preencha todos os campos', color: 'error' })
			return
		}

		const payload: any = {
			nome: nome.value,
			descricao: descricao.value,
			disciplina_id: id_disciplina.value,
			intervalos: intervalo.value,
		}

		if (props.whichFuncToCall === 'create') {
			const response = await createTema(id_disciplina.value, payload)
			addMessage({ text: 'Tema criado com sucesso', color: 'success' })
		} else if (props.whichFuncToCall === 'update') {
			const response = await updateTema(id.value!, payload)
			addMessage({ text: 'Tema alterado com sucesso', color: 'success' })
		}

		nome.value = ''
		descricao.value = ''

		form.value.reset()
		dialog.value = false
	} catch (error) {
		if (props.whichFuncToCall === 'create') {
			console.log('Erro ao criar o tema: ', error)
			addMessage({ text: 'Erro ao criar o tema', color: 'error' })
		} else if (props.whichFuncToCall === 'update') {
			console.log('Erro ao atualizar o tema: ', error)
			addMessage({ text: 'Erro ao atualizar o tema', color: 'error' })
		}
	} finally {
		loading.value = false
	}
}

function addInterval() {
	const ultimoValor =
		intervalo.value.length > 0 ? intervalo.value[intervalo.value.length - 1] : 0

	intervalo.value.push(ultimoValor + 7)
}

function removeInterval(index: number) {
	intervalo.value.splice(index, 1)
}
</script>

<template>
	<v-dialog v-model="dialog" :max-width="actionsWidthDialog">
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>
		<v-card variant="flat" color="card" rounded="lg" class="pa-2">
			<v-card-title>{{ title }}</v-card-title>
			<v-card-subtitle>{{ subtitle }}</v-card-subtitle>
			<v-card-text>
				<v-form ref="form">
					<span class="input-title">Nome do tema</span>
					<v-text-field
						v-model="nome"
						placeholder="Ex.: Equações do 2º grau, Revolução francesa..."
						variant="plain"
						:rules="[required]"
						required
					></v-text-field>
					<span class="input-title">Descrição do tema (opcional)</span>
					<v-text-field
						v-model="descricao"
						placeholder="Breve descrição do que vai estudar"
						variant="plain"
					></v-text-field>
					<span class="input-title">Revisões do tema (dias)</span>
					<span class="input-subtitle"
						>Defina quando você quer revisar este tema após estudá-lo</span
					>
					<v-container
						v-for="(revisao, i) in intervalo"
						class="revisao-container"
					>
						<v-row :key="i" class="revisao-container">
							<span class="revisao-label">Revisão {{ i + 1 }}</span>
							<v-number-input
								:disabled="isEditing"
								class="custom-number-input"
								control-variant="stacked"
								max-width="10vw"
								:model-value="Number(revisao)"
								variant="outlined"
								inset
								density="compact"
								hide-details
							></v-number-input>
							<span>dias</span>
							<v-btn
								v-show="!isEditing"
								variant="plain"
								icon="close"
								@click="removeInterval(i)"
								color="error"
								density="compact"
								elevation="elevation-10"
								rounded="circle"
							></v-btn>
						</v-row>
					</v-container>
					<v-btn
						variant="outlined"
						class="revisao-add"
						color="primary"
						prepend-icon="add"
						@click.prevent="addInterval"
						>Adicionar intervalo</v-btn
					>
				</v-form>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn variant="outlined" @click="dialog = false">Cancelar</v-btn>
				<v-btn
					color="warming"
					variant="outlined"
					type="submit"
					:loading="loading"
					@click="handleClick"
					>Salvar</v-btn
				>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<style scoped>
.revisao-container {
	height: 10vh;
	gap: 1vw;
	align-items: center;
}

.input-title {
	display: block;
	margin: 1vh 0;
}

.input-subtitle {
	color: #767676d6;
	font-size: 0.875rem;
	margin-bottom: 8px;
	font-weight: 300;
}

.input-number > :deep(div) {
	width: 10vw;
}

.revisao-add {
	display: flex;
	margin: 1vh auto;
}

.custom-number-input {
	width: 10vw !important;
	flex: none !important;
	min-width: 0 !important;
}

.custom-number-input :deep(input) {
	text-align: center !important;
	padding: 0;
	height: 100%;
}

.custom-number-input :deep(.v-input__control) {
	min-width: 0 !important;
	width: 100% !important;
}
</style>
