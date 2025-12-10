<template>
	<v-app-bar app class="gradient-app-bar" color="transparent" flat>
		<template v-slot:prepend>
			<v-container class="pa-0">
				<v-row align="center">
					<v-col cols="auto" class="app-bar-titulo">
						<v-icon id="icone" icon="book_ribbon" class="mr-2"></v-icon>
						<div>
							<v-app-bar-title>StudyFlow</v-app-bar-title>
							<span>Aprenda no momento certo</span>
						</div>
					</v-col>
				</v-row>
			</v-container>
		</template>
		<template v-slot:append>
			<v-spacer></v-spacer>
			<div v-if="nameDisplay !== 'xs'">
				<v-btn
					v-for="(tab, i) in tabsNavigation"
					:key="i"
					:prepend-icon="tab.iconName"
				>
					{{ tab.name }}
				</v-btn>
			</div>
			<div v-else>
				<v-menu v-model="menu" :close-on-content-on="false" location="end">
					<template v-slot:activator="{ props }">
						<v-app-bar-nav-icon v-bind="props"></v-app-bar-nav-icon>
					</template>
					<v-list>
						<v-list-item
							v-for="(tab, i) in tabsNavigation"
							:key="i"
							:title="tab.name"
							:prepend-icon="tab.iconName"
						></v-list-item>
					</v-list>
				</v-menu>
			</div>
		</template>
	</v-app-bar>
</template>

<script setup lang="ts">
import { tabsNavigation } from "@/utils/tabsNavigation";
import { ref } from "vue";
import { useDisplay } from "vuetify";

const { name: nameDisplay } = useDisplay();

const menu = ref(false);
</script>

<style scoped>
.gradient-app-bar {
	background: linear-gradient(
		to right,
		rgb(var(--v-theme-app-bar-gradient-start)),
		rgb(var(--v-theme-app-bar-gradient-end))
	) !important;
}

.app-bar-titulo {
	display: flex;
	align-items: center;
	justify-content: space-between;
}

.app-bar-titulo > * {
	margin: auto 1vw;
}

</style>
