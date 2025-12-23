import { ref } from 'vue'

export const tabsNavigation = ref([
	{
		name: 'Home',
		iconName: 'home',
		componentName: 'HomeComponent',
		routeName: 'home',
		description: 'Página inicial do aplicativo',
		isVisible: true,
	},
	{
		name: 'Login',
		iconName: 'login',
		componentName: 'LoginComponent',
		routeName: 'login',
		description: 'Acesse sua conta',
		isVisible: false,
	},
	{
		name: 'Disciplinas',
		iconName: 'book',
		componentName: 'DisciplinasComponent',
		routeName: 'disciplina',
		description: 'Organize seus estudos por disciplinas e temas',
		isVisible: true,
	},
	{
		name: 'Cronograma',
		iconName: 'calendar_month',
		componentName: 'CronogramaComponent',
		routeName: 'cronograma',
		description: 'Acompanhe suas revisões agendadas e sessões de estudo',
		isVisible: true,
	},
	{
		name: 'Relatórios',
		iconName: 'bar_chart',
		componentName: 'RelatoriosComponent',
		routeName: 'relatorios',
		description: 'Acompanhe seu desempenho e evolução',
		isVisible: true,
	},
	{
		name: 'Configurações',
		iconName: 'settings',
		componentName: 'ConfiguracoesComponent',
		routeName: 'configuracoes',
		description: 'Ajustes e preferências do aplicativo.',
		isVisible: false,
	},
])
