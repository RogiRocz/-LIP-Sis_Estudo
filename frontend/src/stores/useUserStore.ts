import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
	const token = ref<String | null>(localStorage.getItem('authToken'))

	function setToken(newToken) {
		token.value = newToken
		if (newToken) {
			localStorage.setItem('authToken', newToken)
		} else {
			localStorage.removeItem('authToken')
		}
	}

	function clearToken() {
		token.value = null
		localStorage.removeItem('authToken')
	}

	const isAuthenticated = () => !!token.value

	return {
		token,
		setToken,
		clearToken,
		isAuthenticated,
	}
})
