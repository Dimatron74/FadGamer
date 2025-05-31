<template>
  <div class="bg-myblack-3 rounded-lg shadow-lg p-6">

    <!-- Сообщение -->
    <div v-if="message" :class="{
        'text-green-500': success,
        'text-red-500': !success
      }" class="mb-4">
      {{ message }}
    </div>

    <!-- Форма -->
    <form @submit.prevent="activatePromoCode" class="space-y-4">
      <input
        v-model="promoCode"
        type="text"
        placeholder="Введите промокод"
        class="w-full bg-myblack-2 text-mywhite-4 placeholder-mywhite-2 border-none rounded-md px-4 py-2 focus:ring-2 focus:ring-mypurple-4"
        required
      />
      <button
        type="submit"
        class="w-full bg-mypurple-4 hover:bg-mypurple-3 text-white font-bold py-2 px-4 rounded"
        :disabled="loading"
      >
        {{ loading ? 'Активация...' : 'Активировать' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import promoCodeService from '@/services/promoCodeService'

const promoCode = ref('')
const message = ref('')
const success = ref(false)
const loading = ref(false)

async function activatePromoCode() {
  message.value = ''
  success.value = false
  loading.value = true

  try {
    const response = await promoCodeService.activatePromoCode({ code: promoCode.value })

    if (response.data.success) {
      message.value = response.data.success
      success.value = true
    } else {
      message.value = 'Неизвестная ошибка'
      success.value = false
    }
  } catch (error) {
    const errorMsg = error.response?.data?.error || 'Ошибка при активации промокода'
    message.value = errorMsg
    success.value = false
  } finally {
    loading.value = false
  }
}
</script>