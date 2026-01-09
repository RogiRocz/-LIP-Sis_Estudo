<template>
  <ViewContainer>
    <template #view-content>
      <PageHeader :pageTitle="name" :pageDescription="description" />

      <!-- Relatório de Estudos -->
      <v-card class="pa-4 mb-4" elevation="2">
        <v-card-title class="text-h6">Relatório de Estudos</v-card-title>
        <v-card-subtitle>Acompanhe seu desempenho e evolução</v-card-subtitle>
        <v-row class="pa-2 mt-2">
          <v-col cols="12" md="4">
            <v-sheet class="pa-4 text-center" rounded="lg" elevation="1">
              <div class="text-h4">{{ estatisticas.tempo_total }}</div>
              <div class="text-subtitle-1">Tempo Total</div>
            </v-sheet>
          </v-col>
          <v-col cols="12" md="4">
            <v-sheet class="pa-4 text-center" rounded="lg" elevation="1">
              <div class="text-h4">{{ estatisticas.sessoes_completas }}</div>
              <div class="text-subtitle-1">Sessões Completas</div>
            </v-sheet>
          </v-col>
          <v-col cols="12" md="4">
            <v-sheet class="pa-4 text-center" rounded="lg" elevation="1">
              <div class="text-h4">{{ estatisticas.dias_seguidos }}</div>
              <div class="text-subtitle-1">Dias Seguidos</div>
            </v-sheet>
          </v-col>
        </v-row>
      </v-card>

      <!-- Evolução Semanal -->
      <v-card class="pa-4 mb-4" elevation="2">
        <v-card-title class="text-h6">Evolução Semanal</v-card-title>
        <div class="chart-container">
          <GraficoEvolucaoSemanal v-if="evolucaoData.labels.length" :evolucaoData="evolucaoData" />
        </div>
      </v-card>

      <!-- Cronograma de Revisões -->
      <v-card class="pa-4" elevation="2">
        <v-card-title class="text-h6">Cronograma de Revisões</v-card-title>
        <v-tabs v-model="tab" bg-color="primary" class="mb-2">
          <v-tab value="atrasadas">Atrasadas ({{ revisoes.atrasadas.length }})</v-tab>
          <v-tab value="hoje">Hoje ({{ revisoes.hoje.length }})</v-tab>
        </v-tabs>
        <v-window v-model="tab">
          <v-window-item value="atrasadas">
            <v-list lines="one" v-if="revisoes.atrasadas.length > 0">
              <v-list-item
                v-for="revisao in revisoes.atrasadas"
                :key="revisao.ID"
                :title="revisao.tema.nome"
                :subtitle="`Previsto para: ${new Date(revisao.data_prevista).toLocaleDateString()}`"
              ></v-list-item>
            </v-list>
            <div v-else class="text-center pa-4">Nenhuma revisão atrasada.</div>
          </v-window-item>
          <v-window-item value="hoje">
            <v-list lines="one" v-if="revisoes.hoje.length > 0">
              <v-list-item
                v-for="revisao in revisoes.hoje"
                :key="revisao.ID"
                :title="revisao.tema.nome"
              ></v-list-item>
            </v-list>
            <div v-else class="text-center pa-4">Nenhuma revisão para hoje.</div>
          </v-window-item>
        </v-window>
      </v-card>
    </template>
  </ViewContainer>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import GraficoEvolucaoSemanal from '@/components/GraficoEvolucaoSemanal.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { painelApi } from '@/api/painel'

const currentView = computed(() =>
  tabsNavigation.value.find((tab) => tab.routeName === 'home'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')

const tab = ref('atrasadas')

const estatisticas = ref({
  tempo_total: '0h 0m',
  sessoes_completas: 0,
  dias_seguidos: 0,
})

const evolucaoData = ref({
  labels: [],
  datasets: [],
})

const revisoes = ref({
  atrasadas: [],
  hoje: [],
})

const api = painelApi()

onMounted(async () => {
  try {
    estatisticas.value = await api.getEstatisticas()
    evolucaoData.value = await api.getEvolucaoSemanal()
    revisoes.value = await api.getRevisoesDoDia()
  } catch (error) {
    console.error('Erro ao buscar dados do painel:', error)
  }
})
</script>

<style scoped>
.chart-container {
  height: 300px;
  padding: 1rem;
}
.v-card {
  margin-bottom: 16px;
}
</style>
