import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY

export const supabase = createClient(supabaseUrl, supabaseKey, {
	auth: {
		// debug: true,
		persistSession: false,
		autoRefreshToken: false,
		storage: window.sessionStorage,
		detectSessionInUrl: false,
	},
	realtime: {
		log_level: 'info',
		params: {
			eventsPerSecond: 10,
		},
	},
})
