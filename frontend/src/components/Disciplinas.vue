<template>
  <div>
    <div class="parte_cima">
      <div>
        <h3>Minhas disciplinas</h3>
        <h5>Organize seus estudos por disciplinas e temas</h5>
      </div>
      <div id="botao">
        <Button variant="primary" size="md">Nova disciplina</Button>
      </div>
    </div>
    <div class="parte_baixo">
      <div>
        <h4>Nenhuma disciplina ainda</h4>
        <h4>Comece criando sua primeira disciplina</h4>
        <button>Criar disciplina</button>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '@/components/Button.vue'
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

.parte_baixo div *{
  text-align: center;
}

#botao {
  display: flex;
  align-items: center;
}
</style>
