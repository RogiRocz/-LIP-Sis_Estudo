import { defineStore } from 'pinia';
import type { Tema, Revisao } from '@/utils/apiTypes';

export const useTimerStore = defineStore('timer', {
  state: () => ({
    tema: null as Tema | null,
    revisao: null as Revisao | null,
  }),
  getters: {
    getTema: (state) => state.tema,
    getRevisoes: (state) => state.revisao,
  },
  actions: {
    setTema(tema: Tema) {
      this.tema = tema;
    },
    setRevisao(revisao: Revisao) {
      this.revisao = revisao;
    },
    clear() {
      this.tema = null;
      this.revisao = null;
    },
  },
});
