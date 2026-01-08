<script setup lang="ts">
import { ref } from 'vue';
import { reagendarRevisao } from '@/api/revisao';
import { useSnackbarStore } from '@/stores/useSnackbarStore';
import { Revisao } from '@/utils/apiTypes';

const props = defineProps<{
  revisao: Revisao;
  tema_nome: string;
}>();

const dialog = ref(false);
const loading = ref(false);
const novaData = ref<Date | null>(null);

const snackbarStore = useSnackbarStore();

async function handleReagendar() {
  if (!novaData.value) {
    snackbarStore.addMessage({ text: 'Por favor, selecione uma data.', color: 'error' });
    return;
  }

  loading.value = true;
  try {
    const dataFormatada = novaData.value.toISOString().split('T')[0];
    await reagendarRevisao(props.revisao.ID, dataFormatada);
    snackbarStore.addMessage({ text: 'Revisão reagendada com sucesso!', color: 'success' });
    dialog.value = false;
  } catch (error) {
    console.error('Erro ao reagendar revisão:', error);
    snackbarStore.addMessage({ text: 'Erro ao reagendar a revisão.', color: 'error' });
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="400px">
    <template v-slot:activator="{ props: activatorProps }">
      <slot name="button" v-bind="activatorProps"></slot>
    </template>

    <v-card>
      <v-card-title>Reagendar Revisão</v-card-title>
      <v-card-text>
        <p class="mb-4">Escolha uma nova data para a revisão do tema <strong>{{ tema_nome }}</strong>.</p>
        <v-date-picker
          v-model="novaData"
          color="primary"
          show-adjacent-months
          hide-header
          width="100%"
        ></v-date-picker>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="dialog = false">Cancelar</v-btn>
        <v-btn color="primary" @click="handleReagendar" :loading="loading">Salvar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
