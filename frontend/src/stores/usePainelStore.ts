import { supabase } from '@/config/supabase'
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const usePainelStore = defineStore('painelStore', () => {
	const needReload = ref(false)

	supabase
		.channel('painel-changes')
		.on(
			'postgres_changes',
			{ event: '*', schema: 'public', table: 'Disciplina' },
			(payload) => {
				if (['INSERT', 'DELETE'].includes(payload.eventType)) {
					needReload.value = true
					needReload.value = false
				}
			},
		)
		.on(
			'postgres_changes',
			{ event: '*', schema: 'public', table: 'Tema' },
			(payload) => {
				if (['INSERT', 'DELETE'].includes(payload.eventType)) {
					needReload.value = true
					needReload.value = false
				}
			},
		)
		.on(
			'postgres_changes',
			{ event: '*', schema: 'public', table: 'Revisao' },
			(payload) => {
				if (['INSERT', 'DELETE'].includes(payload.eventType)) {
					needReload.value = true
					needReload.value = false
				}
			},
		)
		.subscribe((status, err) => {})

        return {
            needReload
        }
})