import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'


const routes = [
	{
		path: '/',
		name: 'home',
		component: () => import('@/views/HomeView.vue'),
	},
	{
		path: '/login',
		name: 'login',
		component: () => import('@/views/LoginView.vue'),
	},
	{
		path: '/cadastro',
		name: 'cadastro',
		component: () => import('@/views/CadastroView.vue'),
	},
	{
		path: '/disciplina',
		name: 'disciplina',
		component: () => import('@/views/DisciplinaView.vue'),
	},
	{
		path: '/calendario',
		name: 'calendario',
		component: () => import('@/views/CalendarioView.vue'),
	},
	{
		path: '/relatorios',
		name: 'relatorios',
		component: () => import('@/views/RelatoriosView.vue'),
	},
	{
		path: '/configuracoes',
		name: 'configuracoes',
		component: () => import('@/views/ConfiguracoesView.vue'),
	},
	{
		path: '/:pathMatch(.*)*',
		name: 'not-found',
		component: () => import('@/views/NotFoundView.vue')
	},
]

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes,
})

router.beforeEach((to, from, next) => {
	const userStore = useUserStore()
	const { isAuthenticated } = storeToRefs(userStore)

	const publicRoutes = ['login', 'cadastro']
	const authRequired = !publicRoutes.includes(to.name)	

	if (authRequired && !isAuthenticated.value) {
		next({ name: 'login' })
	} else if (!authRequired && isAuthenticated.value) {
		next({ name: 'home' })
	} else {
		next()
	}
})


export default router