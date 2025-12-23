<template>
  <ViewContainer>
    <template #view-content>
      <PageHeader :pageTitle="name" :pageDescription="description" />
    </template>
  </ViewContainer>
</template>

<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import ViewContainer from '@/components/ViewContainer.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { computed, onActivated } from 'vue'

const currentView = computed(() =>
  tabsNavigation.value.find((tab) => tab.routeName === 'cronograma'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')

onActivated(() => {
  console.log('Componente Ativado')
})
</script>

<style scoped>

</style>
