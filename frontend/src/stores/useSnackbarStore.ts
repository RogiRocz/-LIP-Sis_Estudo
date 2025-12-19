import { SnackbarType } from "@/utils/snackbarType";
import { defineStore } from "pinia";
import { computed, ref } from "vue";

export const useSnackbarStore = defineStore('snackbarStore', () => {
    // States
    const messages = ref<SnackbarType[]>([])

    // Getters
    const getMessages = computed(() => messages.value)

    // Actions
    function addMessage(msg: SnackbarType) {
        if (!!msg){
            messages.value.push(msg)
        }
    }

    return { messages, getMessages, addMessage }
})