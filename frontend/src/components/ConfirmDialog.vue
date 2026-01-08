<script setup lang="ts">
import { ref } from 'vue'
import { useAppBarStore } from '@/stores/useAppBarStore'
import { storeToRefs } from 'pinia'

const isOpen = ref(false)
const title = ref('')
const message = ref('')
const icon = ref('')

const appBarStore = useAppBarStore()
const { actionsWidthDialog } = storeToRefs(appBarStore)

let resolvePromise: (value: boolean) => void

const open = (newTitle: string, newMessage: string, newIcon?: string) => {
	title.value = newTitle
	message.value = newMessage
	icon.value = newIcon ? newIcon : 'delete'
	isOpen.value = true

	return new Promise<boolean>((resolve) => {
		resolvePromise = (value: boolean) => {
			isOpen.value = false
			resolve(value)
		}
	})
}

defineExpose({ open })
</script>

<template>
	<v-dialog v-model="isOpen" :max-width="actionsWidthDialog" persistent>
		<v-card rounded="lg">
			<v-card-title class="d-flex align-center bg-error-lighten-5 py-4">
				<v-icon color="error" class="mr-2">{{ icon }}</v-icon>
				<span class="text-error font-weight-bold">{{ title }}</span>
			</v-card-title>

			<v-card-text class="py-6 text-body-1">
				{{ message }}
			</v-card-text>

			<v-divider></v-divider>

			<v-card-actions class="pa-4">
				<v-spacer></v-spacer>
				<v-btn
					variant="text"
					color="grey-darken-1"
					@click="resolvePromise(false)"
				>
					Cancelar
				</v-btn>
				<v-btn
					color="error"
					variant="elevated"
					class="px-6"
					@click="resolvePromise(true)"
				>
					Confirmar
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<style scoped></style>
