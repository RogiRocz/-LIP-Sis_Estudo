<template>
  <div>
    <div class="parte_cima">
      <div>
        <h3>Minhas disciplinas</h3>
        <h5>Organize seus estudos por disciplinas e temas</h5>
      </div>
      <div id="botao">
        <Button @click="switchModal" variant="primary" size="md">Nova disciplina</Button>
      </div>
    </div>
    <div class="parte_baixo">
      <div>
        <h4>Nenhuma disciplina ainda</h4>
        <h4>Comece criando sua primeira disciplina</h4>
        <button @click="switchModal">Criar disciplina</button>
      </div>
    </div>
  </div>
  <span v-if="modalHidden">
    <div id="fade"></div>
    <NewForm id="modal" @close="switchModal" />
  </span>
</template>

<script setup>
import { ref } from 'vue'
import Button from '@/components/Button.vue'
import NewForm from '@/components/NewForm.vue'

const modalHidden = ref(false)

function switchModal() {
  modalHidden.value = !modalHidden.value
}
</script>

<style scoped>
.parte_cima {
  display: flex;
  justify-content: space-around;
}

.parte_baixo {
  border-radius: 5px;
  border: 1px solid black;
  width: 75vw;
  height: 50vh;
  margin: auto;
}

.parte_baixo div {
  margin: auto;
  height: 100%;
  width: 75%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.parte_baixo div * {
  text-align: center;
}

#botao {
  display: flex;
  align-items: center;
}

#fade {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 5;
}

#modal {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 6;
}
</style>
