<template>
  <div>
    <div class="parte_cima">
      <div>
        <h3>Minhas disciplinas</h3>
        <h5>Organize seus estudos por disciplinas e temas</h5>
      </div>
      <Button variant="primary" size="md">Nova disciplina</Button>
    </div>
    <div class="parte_baixo">
      <h4>Nenhuma disciplina ainda</h4>
      <h4>Comece criando sua primeira disciplina</h4>
      <Button>Criar disciplina</Button>
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
</style>
