import { ref } from 'vue'

export const tabsNavigation = ref([
	{
		name: 'Disciplinas',
		iconName: 'book',
		componentName: 'DisciplinasComponent',
		routeName: 'disciplina',
	},
	{
		name: 'Cronograma',
		iconName: 'calendar_month',
		componentName: 'CronogramaComponent',
		routeName: 'calendario',
	},
	{
		name: 'Relatórios',
		iconName: 'bar_chart',
		componentName: 'RelatoriosComponent',
		routeName: 'relatorios',
	},
	{
		name: 'Configurações',
		iconName: 'settings',
		componentName: 'ConfiguracoesComponent',
		routeName: 'configuracoes',
	},
])
