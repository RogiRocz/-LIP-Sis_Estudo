import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import vuetify from './config/vuetify'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const initApp = async () => {
	const app = createApp(App)
	const pinia = createPinia()
	pinia.use(piniaPluginPersistedstate)

	app.use(vuetify)
	app.use(pinia)
	app.use(router)
	await router.isReady()

	app.mount('#app')
}

initApp()
