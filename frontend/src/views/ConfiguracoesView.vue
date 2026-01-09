<template>
  <ViewContainer>
    <template #view-content>
      <PageHeader :pageTitle="name" :pageDescription="description" />

      <v-row>
        <!-- Card de Perfil -->
        <v-col cols="12">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="text-h6">Perfil</v-card-title>
            <v-card-subtitle>Gerencie suas informações</v-card-subtitle>
            <v-card-text>
              <v-text-field
                label="Nome de Usuário"
                prepend-inner-icon="person"
                readonly
              ></v-text-field>
              <v-text-field
                label="Email"
                prepend-inner-icon="mail"
                readonly
              ></v-text-field>
              <v-btn color="primary" class="mt-2">Salvar Alterações</v-btn>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Card de Aparência -->
        <v-col cols="12">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="text-h6">Aparência</v-card-title>
            <v-card-text>
              <v-switch
                label="Tema Escuro"
                prepend-icon="dark_mode"
                color="primary"
              ></v-switch>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Card de Dados de Exemplo -->
        <v-col cols="12">
          <v-card class="pa-4" elevation="2">
            <v-card-title class="text-h6">Dados de Exemplo</v-card-title>
            <v-card-subtitle>Preencha a aplicação com dados fictícios para teste.</v-card-subtitle>
            <v-card-text>
              <v-btn color="secondary" @click="handleCriarDadosExemplo">
                <v-icon left>add_circle</v-icon>
                Carregar Dados
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </ViewContainer>
</template>

<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { computed } from 'vue'
import { criarDadosExemplo } from '@/api/user'
import { useSnackbarStore } from '@/stores/useSnackbarStore'

const snackbarStore = useSnackbarStore()

const currentView = computed(() =>
  tabsNavigation.value.find((tab) => tab.routeName === 'configuracoes'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')

const handleCriarDadosExemplo = async () => {
  try {
    await criarDadosExemplo()
    snackbarStore.showSnackbar('Dados de exemplo carregados com sucesso!', 'success')
  } catch (error) {
    console.error(error)
    snackbarStore.showSnackbar('Ocorreu um erro ao carregar os dados de exemplo.', 'error')
  }
}
</script>

<style scoped>
.v-card {
  margin-bottom: 16px;
}
</style>
