<script setup lang="ts">
import { useAppBarStore } from '@/stores/useAppBarStore'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { useUserStore } from '@/stores/useUserStore'
import { required } from '@/utils/rulesAuth'
import { storeToRefs } from 'pinia'
import { computed, onMounted, ref, watch } from 'vue'

const dialog = ref(false)
const loading = ref(false)
const form = ref()
const nome = ref('')
const descricao = ref('')
const revisoes = ref<string[]>([])
const id = ref(null)

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const appBarStore = useAppBarStore()
const { nameDisplay } = storeToRefs(appBarStore)

const { getUser } = useUserStore()
const { intervalo_revisoes } = getUser

const actionsWidthDialog = computed(() => {
	return nameDisplay.value === 'xs' ? '100%' : '50vw'
})

const props = defineProps<{
	title: string
	subtitle: string
	whichFuncToCall: string
	initialData?: any
}>()

watch(
	() => dialog.value,
	(isOpen) => {
		if (isOpen && props.whichFuncToCall === 'update' && props.initialData) {
			nome.value = props.initialData.nome
			descricao.value = props.initialData.descricao
			revisoes.value = props.initialData.revisoes
			id.value = props.initialData.id || props.initialData.ID
		}
	},
)

async function handleClick() {
	console.log('Entrou')
}

onMounted(() => {
	console.log(intervalo_revisoes.split(','))
})
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
						v-for="(revisao, i) in intervalo_revisoes.split(',')"
						class="revisao-container"
					>
						<v-row :key="i" class="revisao-container">
							<span class="revisao-label">Revisão {{ i + 1 }}</span>
							<v-number-input
								class="custom-number-input"
								control-variant="stacked"
								max-width="10vw"
								:model-value="Number(revisao)"~
								variant="outlined"
								inset
								density="compact"
								hide-details
							></v-number-input>
							<span>dias</span>
							<v-btn
								variant="plain"
								icon="close"
								@click="revisoes.splice(i, 1)"
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
					 prepend-icon="add">Adicionar intervalo</v-btn>
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
