import { h } from 'vue'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import 'material-symbols/outlined.css'

/**
 * Paleta de Cores StudyFlow:
 * primary: 17a2b8 (Turquesa - Usado para botões e destaque)
 * secondary: 667eea (Roxo Mais Claro)
 * gradient_end: 764ba2 (Roxo Mais Escuro - Para o App Bar)
 */
const StudyFlowTheme = {
	defaultTheme: 'dark',

	themes: {
		dark: {
			dark: true,
			colors: {
				background: '121212',
				surface: '1E1E1E',
				primary: '17a2b8',
				secondary: '667eea',
				error: 'EF4444',
				info: '17a2b8',
				success: '10B981',
				warning: 'FBBF24',
				'app-bar-gradient-start': '667eea',
				'app-bar-gradient-end': '764ba2',
			},
			variables: {
				'app-bar-gradient-start': '667eea',
				'app-bar-gradient-end': '764ba2',
			},
		},
		light: {
			dark: false,
			colors: {
				background: '#FFFFFF',
				'app-bar-gradient-start': '667eea',
				'app-bar-gradient-end': '764ba2',
			},
			variables: {
				'app-bar-gradient-start': '667eea',
				'app-bar-gradient-end': '764ba2',
			},
		},
	},
}

const materialSymbols = {
	component: (props) =>
		h('span', { ...props, class: 'material-symbols-outlined' }, props.icon),
}

export default createVuetify({
	theme: StudyFlowTheme,
	icons: {
		defaultSet: 'materialSymbols',
		sets: {
			materialSymbols,
		},
		aliases: {
			menu: 'menu',
			book_ribbon: 'book',
		},
	},
})
