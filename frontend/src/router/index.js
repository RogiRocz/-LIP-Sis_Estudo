import { createRouter, createWebHistory } from 'vue-router'

import Disciplinas from '@/components/Disciplinas.vue'
import Relatorios from '@/components/Relatorios.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/disciplinas', component: Disciplinas},
    {path: '/relatorios', component: Relatorios},
  ]
})

export default router
