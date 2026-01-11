import { h } from 'vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import 'material-symbols/outlined.css'
import { aliases, md } from 'vuetify/iconsets/md'
import * as LabsComponentes from 'vuetify/labs/components'

/**
 * Paleta de Cores StudyFlow:
 * primary: 17a2b8 (Turquesa - Usado para botões e destaque)
 * secondary: 667eea (Roxo Mais Claro)
 * gradient_end: 764ba2 (Roxo Mais Escuro - Para o App Bar)
 */
const StudyFlowTheme = {
	defaultTheme: 'light',

	themes: {
		dark: {
			dark: true,
			colors: {
				background: '#121212',
				surface: '#1E1E1E',
				primary: '#A18CD1',
				secondary: '#667eea',
				card: '#2d3748',
				error: '#EF4444',
				info: '#17a2b8',
				success: '#48BB78',
				warning: '#F687B3',
				'app-bar-gradient-start': '#667eea',
				'app-bar-gradient-end': '#764ba2',
			},
			variables: {
				'app-bar-gradient-start': '#667eea',
				'app-bar-gradient-end': '#764ba2',
			},
		},
		light: {
			dark: false,
			colors: {
				background: '#fff',
				surface: '#1E1E1E',
				primary: '#A18CD1',
				secondary: '#667eea',
				card: '#f0f4f8',
				error: '#EF4444',
				info: '#17a2b8',
				success: '#48BB78',
				warning: '#F687B3',
				'app-bar-gradient-start': '#667eea',
				'app-bar-gradient-end': '#764ba2',
			},
			variables: {
				'app-bar-gradient-start': '#667eea',
				'app-bar-gradient-end': '#764ba2',
			},
		},
	},
}

export default createVuetify({
	theme: {
		defaultTheme: 'light',
		themes: StudyFlowTheme.themes,
	},
	icons: {
		defaultSet: 'md',
		aliases,
		sets: {
			md: {
				...md,
				component: (props: any) => {
					return h(
						'span',
						{
							...props,
							class: [
								'v-icon',
								'notranslate',
								'material-symbols-outlined',
								props.class,
							],
						},
						props.icon,
					)
				},
			},
		},
	},
	components: {
		...LabsComponentes,
	},
})
