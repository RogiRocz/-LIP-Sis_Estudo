import { defineStore } from 'pinia'
import { useDisplay } from 'vuetify'
import { computed, ref, watch } from 'vue'

export const useAppBarStore = defineStore('appBarStore', () => {
	// State
	const drawer = ref(false)
	const { name: nameDisplay } = useDisplay()

	// Getters

	const actionsWidthDialog = computed(() => {
		return nameDisplay.value === 'xs' ? '100%' : '75vw'
	})

	// Actions
	function toggleDrawer() {
		drawer.value = !drawer.value
	}

	// Watcher to close drawer on screen resize
	watch(nameDisplay, (newName) => {
		if (newName !== 'xs') {
			drawer.value = false
		}
	})

	return {
		drawer,
		nameDisplay,
		toggleDrawer,
		actionsWidthDialog,
	}
})
