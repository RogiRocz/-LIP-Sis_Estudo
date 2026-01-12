<script setup lang="ts">
import { useUserStore } from '@/stores/useUserStore'
import { tabsNavigation } from '@/utils/tabsNavigation'
import { storeToRefs } from 'pinia'
import { computed } from 'vue'

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const { logout } = userStore

const userInitials = computed(() => {
	if (user.value && user.value.nome) {
		const names = user.value.nome.split(' ')
		if (names.length > 1 && names[names.length - 1]) {
			return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase()
		}
		return `${names[0]?.[0] || ''}`.toUpperCase()
	}
	return ''
})

const configTab = tabsNavigation.value.find(
	(tab) => tab.routeName === 'configuracoes',
)
</script>

<template>
	<v-menu location="bottom" transition="slide-y-transition">
		<template v-slot:activator="{ props }">
			<v-btn v-bind="props" class="user-settings-btn" variant="outlined">
				<v-avatar color="primary" size="32">
					<span class="text-white font-weight-bold">{{ userInitials }}</span>
				</v-avatar>
			</v-btn>
		</template>

		<v-list density="compact">
			<v-list-item class="mb-2">
				<template v-slot:prepend>
					<v-avatar color="primary" size="40" class="mr-3">
						<span class="text-white font-weight-bold">{{ userInitials }}</span>
					</v-avatar>
				</template>
				<v-list-item-title class="font-weight-bold">{{
					user?.nome
				}}</v-list-item-title>
				<v-list-item-subtitle>{{ user?.email }}</v-list-item-subtitle>
			</v-list-item>

			<v-divider></v-divider>

			<v-list-item
				:to="{ name: configTab.routeName }"
				:prepend-icon="configTab.iconName"
				class="mt-2"
			>
				<v-list-item-title>{{ configTab.name }}</v-list-item-title>
			</v-list-item>

			<v-divider></v-divider>

			<v-list-item
				@click="logout"
				prepend-icon="logout"
				class="mt-2"
				base-color="error"
			>
				<v-list-item-title>Sair</v-list-item-title>
			</v-list-item>
		</v-list>
	</v-menu>
</template>

<style scoped>
.user-settings-btn {
	text-transform: none;
	letter-spacing: normal;
	font-family: inherit;
	min-width: min-content;
	padding: 0;
	margin: 0 1vw;
	border-radius: 200px;
}
.user-info {
	line-height: 1.2;
}
</style>
