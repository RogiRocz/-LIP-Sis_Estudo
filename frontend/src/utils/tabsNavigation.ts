import { ref } from 'vue'

export const tabsNavigation = ref([
	{
		name: 'Disciplinas',
		iconName: 'book',
		componentName: 'DisciplinasComponent',
		routeName: 'disciplina',
		description: 'Organize seus estudos por disciplinas e temas',
	},
	{
		name: 'Cronograma',
		iconName: 'calendar_month',
		componentName: 'CronogramaComponent',
		routeName: 'calendario',
		description: 'Acompanhe suas revisões agendadas e sessões de estudo',
	},
	{
		name: 'Relatórios',
		iconName: 'bar_chart',
		componentName: 'RelatoriosComponent',
		routeName: 'relatorios',
		description: 'Acompanhe seu desempenho e evolução',
	},
	{
		name: 'Configurações',
		iconName: 'settings',
		componentName: 'ConfiguracoesComponent',
		routeName: 'configuracoes',
		description: 'Ajustes e preferências do aplicativo.',
	},
])
