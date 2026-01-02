import { defineStore } from "pinia";
import { ref } from "vue";

export const useDisciplinaStore = defineStore('disciplinaStore', () => {
    const isEditing = ref(false)

    return {
        isEditing
    }
})