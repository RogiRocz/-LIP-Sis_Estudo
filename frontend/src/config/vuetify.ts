import { createVuetify } from 'vuetify'

/**
 * Paleta de Cores StudyFlow:
 * primary: #17a2b8 (Turquesa - Usado para botões e destaque)
 * secondary: #667eea (Roxo Mais Claro)
 * gradient_end: #764ba2 (Roxo Mais Escuro - Para o App Bar)
 */
const StudyFlowTheme = {
  defaultTheme: 'dark',

  themes: {
    // --- Tema Escuro ---
    dark: {
      dark: true,
      colors: {
        background: '#121212',

        surface: '#1E1E1E',

        primary: '#17a2b8',
        secondary: '#667eea',

        error: '#EF4444',
        info: '#17a2b8',
        success: '#10B981',
        warning: '#FBBF24',
      },

      variables: {
        'app-bar-gradient-start': '#667eea',
        'app-bar-gradient-end': '#764ba2',
      },
    },

    // --- Tema Claro ---
    light: {
      dark: false,
      colors: {
        primary: '#17a2b8',
        secondary: '#69306D',
        background: '#FFFFFF',
        surface: '#F5F5F5',
      },
    },
  },
}

const vuetify = createVuetify({
  theme: StudyFlowTheme,
})

export default vuetify
