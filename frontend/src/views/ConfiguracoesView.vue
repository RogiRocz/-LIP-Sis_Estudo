<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h5 class="text-h5 mb-4">Configurações</h5>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Perfil</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="user.nome"
              label="Nome de Usuário"
              readonly
            ></v-text-field>
            <v-text-field
              v-model="user.email"
              label="Email"
              readonly
            ></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Aparência</v-card-title>
          <v-card-text>
            <v-switch
              v-model="isDarkMode"
              label="Tema Escuro"
              @change="toggleTheme"
            ></v-switch>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { storeToRefs } from 'pinia'

// User Store
const userStore = useUserStore()
const { user } = storeToRefs(userStore)

// Theme Store
const themeStore = useThemeStore()
const { toggleTheme } = themeStore
const isDarkMode = computed({
  get: () => themeStore.isDarkMode,
  set: (value) => {
    if (value !== themeStore.isDarkMode) {
      toggleTheme()
    }
  },
})
</script>
