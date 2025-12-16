<template>
  <div class="form-card">
    <!-- Header -->
    <header class="header">
      <div>
        <h2>Nova Disciplina</h2>
        <p>Crie uma nova disciplina para organizar seus estudos</p>
      </div>

      <button class="close" @click="$emit('close')">×</button>
    </header>

    <!-- Content -->
    <div class="content">
      <!-- Name -->
      <label>Nome da Disciplina</label>
      <input
        v-model="name"
        placeholder="Ex: Matemática, História, Biologia..."
      />

      <!-- Colors -->
      <label>Cor da Disciplina</label>
      <div class="colors">
        <button
          v-for="color in colors"
          :key="color"
          class="color"
          :style="{ background: color }"
          :class="{ selected: color === selectedColor }"
          @click="selectedColor = color"
        />
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <button class="cancel" @click="$emit('close')">
        Cancelar
      </button>

      <button class="create" @click="submit">
        <span>＋</span> Criar Disciplina
      </button>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["close", "create"]);

const name = ref("");
const selectedColor = ref("#6C7CFF");

const colors = [
  "#6C7CFF",
  "#19A6B6",
  "#7A4DA3",
  "#56D6C2",
  "#A787F2",
  "#50C878",
  "#F28C38",
  "#FF6B6B"
];

function submit() {
  if (!name.value) return;

  emit("create", {
    name: name.value,
    color: selectedColor.value
  });

  name.value = "";
}
</script>

<style scoped>
.form-card {
  width: 420px;
  background: linear-gradient(180deg, #1b2230, #151b26);
  border-radius: 16px;
  padding: 20px;
  color: #fff;
  box-shadow: 0 20px 50px rgba(0,0,0,.4);
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header h2 {
  margin: 0;
  font-size: 18px;
}

.header p {
  margin-top: 4px;
  font-size: 13px;
  color: #aab2c8;
}

.close {
  background: none;
  border: none;
  font-size: 20px;
  color: #aab2c8;
  cursor: pointer;
}

/* Content */
.content {
  margin-top: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  color: #cbd3ee;
}

input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #2c3550;
  background: #111726;
  color: #fff;
  outline: none;
  margin-bottom: 16px;
}

input:focus {
  border-color: #6c7cff;
}

/* Colors */
.colors {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.color {
  height: 42px;
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
}

.color.selected {
  border-color: #fff;
}

/* Footer */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
}

.cancel {
  background: none;
  border: none;
  color: #aab2c8;
  cursor: pointer;
}

.create {
  background: linear-gradient(90deg, #6c7cff, #8e6cff);
  border: none;
  padding: 10px 16px;
  border-radius: 12px;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}
</style>

