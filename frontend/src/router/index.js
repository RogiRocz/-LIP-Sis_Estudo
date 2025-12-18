import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'

const routes = [
	{
		path: '/',
		name: 'home',
		component: import('@/views/HomeView.vue'),
		redirect: { name: 'cadastro' },
	},
	{
		path: '/login',
		name: 'login',
		component: import('@/views/LoginView.vue'),
	},
	{
		path: '/cadastro',
		name: 'cadastro',
		component: import('@/views/CadastroView.vue'),
	},
	{
		path: '/disciplina',
		name: 'disciplina',
		component: import('@/views/DisciplinaView.vue'),
	},
	{
		path: '/calendario',
		name: 'calendario',
		component: import('@/views/CalendarioView.vue'),
	},
	{
		path: '/relatorios',
		name: 'relatorios',
		component: import('@/views/RelatoriosView.vue'),
	},
	{
		path: '/configuracoes',
		name: 'configuracoes',
		component: import('@/views/ConfiguracoesView.vue'),
	},
]

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes,
})

router.beforeEach((to, from) => {
	const userStore = useUserStore()
	const { token } = storeToRefs(userStore)

	const publicRoutes = ['login']

	// if (!publicRoutes.includes(to.name) && !token.value) {
	// 	return { name: 'login' }
	// }
})

export default router
