import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([])

  function addToast(message, type = 'info') {
    toasts.value.push({ message, type, id: Date.now() })
  }

  function removeToast(id) {
    toasts.value = toasts.value.filter(toast => toast.id !== id)
  }

  return { toasts, addToast, removeToast }
})
