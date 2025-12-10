import { ref } from 'vue'

export const tabsNavigation = ref([
  {
    name: 'Disciplinas',
    iconName: 'book',
    componentName: 'DisciplinasComponent',
  },
  {
    name: 'Cronograma',
    iconName: 'calendar_month',
    componentName: 'CronogramaComponent',
  },
  {
    name: 'Relatórios',
    iconName: 'bar_chart',
    componentName: 'RelatoriosComponent',
  },
  {
    name: 'Configurações',
    iconName: 'settings',
    componentName: 'ConfiguracoesComponent',
  },
])
