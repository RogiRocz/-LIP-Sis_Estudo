import type { Ref } from "vue";

export interface AuthInput {
	name: string;
	type: string;
	placeholder: string;
	model: Ref<string>;
	icon: string;
}