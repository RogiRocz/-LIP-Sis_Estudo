<script setup lang="ts">
import { required } from '@/utils/rulesAuth'
import { useSnackbarStore } from '@/stores/useSnackbarStore'
import { createDisciplina, updateDisciplina } from '@/api/disciplina'
import { computed, ref, watch } from 'vue'
import { getColorName, initColors, ORIGINAL_COLORS } from 'ntc-ts'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { storeToRefs } from 'pinia'

const dialog = ref(false)
const loading = ref(false)
const form = ref()
const nome = ref('')
const descricao = ref('')
const cor = ref('')
const id = ref(null)

const snackbarStore = useSnackbarStore()
const { addMessage } = snackbarStore

const appBarStore = useAppBarStore()
const { nameDisplay } = storeToRefs(appBarStore)

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
			cor.value = props.initialData.cor
			id.value = props.initialData.id || props.initialData.ID
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

		if (props.whichFuncToCall === 'create') {
			const response = await createDisciplina({
				nome: nome.value,
				cor: cor.value,
				descricao: descricao.value,
			})
		} else if (props.whichFuncToCall === 'update') {
			const idDisciplina = id.value

			const data = {
				nome: nome.value,
				cor: cor.value,
				descricao: descricao.value,
			}
			const response = await updateDisciplina(id.value!, data)
			addMessage({ text: 'Disciplina alterada com sucesso', color: 'success' })
		}

		nome.value = ''
		descricao.value = ''
		cor.value = ''
		form.value.reset()
		dialog.value = false
	} catch (error) {
		if (props.whichFuncToCall === 'create') {
			console.log('Erro ao criar disciplina: ', error)
			addMessage({ text: 'Erro ao criar disciplina', color: 'error' })
		} else if (props.whichFuncToCall === 'update') {
			console.log('Erro ao atualizar disciplina: ', error)
			addMessage({ text: 'Erro ao atualizar disciplina', color: 'error' })
		}
	} finally {
		loading.value = false
	}
}

initColors(ORIGINAL_COLORS)

const showTooltip = ref(false)
const hoverColorName = ref('')
const tooltipTarget = ref<HTMLElement | null>(null)

const rgbToHex = (rgb: string) => {
	if (rgb.startsWith('#')) return rgb.toUpperCase()

	const match = rgb.match(/\d+/g)
	if (!match || match.length < 3) return '#000000'

	const hex =
		'#' +
		match
			.slice(0, 3)
			.map((x) => {
				const h = parseInt(x).toString(16).toUpperCase()
				return h.length === 1 ? '0' + h : h
			})
			.join('')

	return hex
}

const handlePickerHover = (event: MouseEvent) => {
    const target = (event.target as HTMLElement).closest('.v-color-picker-swatches__color') as HTMLElement;

    if (target) {
        const rgbColor = target.children.item(0).attributes.getNamedItem('style')?.value.match(/\d+/g)?.join(',')		
        
        if (rgbColor) {
            const hexColor = rgbToHex(rgbColor);
            
            // LOG PARA DEBUG: Se continuar Black, veja o que aparece no console
            // console.log("HEX convertido:", hexColor); 

            const result = getColorName(hexColor);

            if (result && result.name !== 'not-a-color') {
                hoverColorName.value = result.name;
                tooltipTarget.value = target;
                showTooltip.value = true;
            }
        }
    } else {
        showTooltip.value = false;
    }
}
</script>

<template>
	<v-dialog v-model="dialog" :max-width="actionsWidthDialog" scrollable>
		<template v-slot:activator="{ props: activatorProps }">
			<slot name="button" v-bind="activatorProps"></slot>
		</template>
		<v-card variant="flat" color="card" rounded="lg" class="pa-2">
			<v-card-title>{{ title }}</v-card-title>
			<v-card-subtitle>{{ subtitle }}</v-card-subtitle>
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
					<div
						class="picker-container"
						@mousemove="handlePickerHover"
						@mouseleave="showTooltip = false"
					>
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

						<v-tooltip
							v-model="showTooltip"
							:activator="tooltipTarget"
							location="right"
							offset="10"
						>
							<span>{{ hoverColorName }}</span>
						</v-tooltip>
					</div>
				</v-form>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn variant="outlined" @click="dialog = false">Cancelar</v-btn>
				<v-btn
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
.picker-container {
	position: relative;
}

.input-title {
	display: inline-block;
	margin: 1vh 0;
}
</style>
