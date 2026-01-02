<template>
	<v-container no-gutters fluid>
		<v-row id="page-header">
			<v-col id="page-header-info">
				<h2>{{ pageTitle }}</h2>
				<p>{{ pageDescription }}</p>
			</v-col>
			<v-col id="page-header-actions">
				<slot name="page-header-actions"> </slot>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup lang="ts">
import { useAppBarStore } from '@/stores/useAppBarStore';
import { storeToRefs } from 'pinia';
import { computed, watch } from 'vue';

const props = defineProps<{
	pageTitle: string
	pageDescription: string
}>()

const appBarStore = useAppBarStore()
const { nameDisplay } = storeToRefs(appBarStore)

const actionsDisplayHeaderInfo = computed(() => {
	return nameDisplay.value === 'xs' ? 'contents' : 'block'
})

const actionsFlexDirection = computed(() => {
	return nameDisplay.value === 'xs' ? 'column' : 'row'
})

const actionsAlign = computed(() => {
	return nameDisplay.value === 'xs' ? 'flex-end' : 'center'
})

const actionsGap = computed(() => {
	return nameDisplay.value === 'xs' ? '2vh' : 'auto'
})

</script>

<style scoped>
h2 {
	font-weight: 400;
}

p {
	color: #64748b;
}

#page-header-info {
	display: v-bind(actionsDisplayHeaderInfo);
}

#page-header-actions {
	display: flex;
	align-items: v-bind(actionsAlign);
	gap: v-bind(actionsGap);
	flex-direction: v-bind(actionsFlexDirection);
	justify-content: flex-end;
}

#page-header-actions > :deep(.v-btn) {
	margin: 0 .5vw;
}
</style>
