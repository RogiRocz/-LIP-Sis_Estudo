<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { useTheme } from 'vuetify'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

const props = defineProps({
  evolucaoSemanal: {
    type: Array,
    required: true,
  },
})

const theme = useTheme()

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: 'Revisões Realizadas',
      backgroundColor: theme.current.value.colors.primary,
      data: [],
    },
  ],
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      ticks: {
        color: theme.current.value.dark ? 'white' : 'black',
      },
    },
    y: {
      ticks: {
        color: theme.current.value.dark ? 'white' : 'black',
      },
    },
  },
}))

watch(
  () => props.evolucaoSemanal,
  (newVal) => {
    if (newVal && newVal.length) {
      chartData.value.labels = newVal.map((item) => {
        const date = new Date(item.data)
        return date.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
        })
      })
      chartData.value.datasets[0].data = newVal.map(
        (item) => item.revisoes_realizadas
      )
    }
  },
  { immediate: true }
)

watch(
  () => theme.current.value.colors.primary,
  (newColor) => {
    chartData.value.datasets[0].backgroundColor = newColor
  }
)
</script>
