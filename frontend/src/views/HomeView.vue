<template>
	<PageHeader :pageTitle="name" :pageDescription="description" />
</template>

<script setup lang="ts">
import PageHeader from '@/components/PageHeader.vue'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { computed } from 'vue'

const currentView = computed(() =>
	tabsNavigation.value.find((tab) => tab.routeName === 'home'),
)
const name = computed(() => currentView.value?.name || '')
const description = computed(() => currentView.value?.description || '')
</script>

<style scoped></style>
