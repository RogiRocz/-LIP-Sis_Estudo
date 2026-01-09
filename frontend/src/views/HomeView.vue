<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h5 class="text-h5">Estatísticas Gerais</h5>
      </v-col>
      <v-col
        v-for="(stat, index) in estatisticas"
        :key="index"
        cols="12"
        sm="6"
        md="3"
      >
        <v-card>
          <v-card-title>{{ stat.title }}</v-card-title>
          <v-card-text class="text-h4">{{ stat.value }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Evolução Semanal</v-card-title>
          <v-card-text>
            <GraficoEvolucaoSemanal :evolucao-semanal="evolucaoSemanal" />
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Revisões do Dia</v-card-title>
          <v-list>
            <v-list-item
              v-for="revisao in revisoesDoDia"
              :key="revisao.id_revisao"
            >
              <v-list-item-title>{{ revisao.titulo_tema }}</v-list-item-title>
              <v-list-item-subtitle>{{
                revisao.nome_disciplina
              }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item v-if="!revisoesDoDia.length">
              <v-list-item-title>Nenhuma revisão para hoje.</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getEstatisticas } from '@/api/painel'
import GraficoEvolucaoSemanal from '@/components/GraficoEvolucaoSemanal.vue'

const painelData = ref(null)

const estatisticas = computed(() => {
  if (!painelData.value) return []
  const { estatisticas } = painelData.value
  return [
    { title: 'Total de Disciplinas', value: estatisticas.total_disciplinas },
    { title: 'Total de Temas', value: estatisticas.total_temas },
    { title: 'Total de Revisões', value: estatisticas.total_revisoes },
    { title: 'Revisões para Hoje', value: estatisticas.revisoes_hoje },
  ]
})

const evolucaoSemanal = computed(() => painelData.value?.evolucao_semanal || [])
const revisoesDoDia = computed(() => painelData.value?.revisoes_do_dia || [])

onMounted(async () => {
  try {
    const response = await getEstatisticas()
    painelData.value = response.data
  } catch (error) {
    console.error('Erro ao buscar dados do painel:', error)
  }
})
</script>
