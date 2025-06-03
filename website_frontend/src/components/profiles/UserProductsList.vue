<template>
  <div class="bg-myblack-3 rounded-lg shadow-lg p-6">
    <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Продукты</h2>

    <div v-if="loading" class="text-center py-4 text-mywhite-3">Загрузка...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <div v-else>
      <!-- Игры -->
      <h3 class="text-lg font-medium text-mywhite-4 mt-6 mb-3">Игры</h3>
      <div v-if="games.length === 0" class="text-mywhite-3 italic mb-4">Нет игр</div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="item in games" :key="item.id" class="bg-myblack-2 p-3 rounded-md flex items-center space-x-3">
          <img :src="item.cover_image" alt="Обложка" class="w-16 h-16 object-cover rounded">
          <div>
            <p class="font-medium text-mywhite-5">{{ item.product_name }}</p>
            <p class="text-sm text-mywhite-3">Дата добавления: {{ formatDate(item.created_at) }}</p>
            <p class="text-sm text-mywhite-3">Лицензия: {{ item.distribution_model }}</p>
            <p class="text-xs mt-1" :class="{
              'text-myred-4': item.is_blocked,
              'text-mypurple-4': !item.is_blocked
            }">
              {{ item.is_blocked ? 'Заблокирован' : 'Активен' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Продукты -->
      <h3 class="text-lg font-medium text-mywhite-4 mt-8 mb-3">Другие продукты</h3>
      <div v-if="otherProducts.length === 0" class="text-mywhite-3 italic mb-4">Нет других продуктов</div>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        <div v-for="item in otherProducts" :key="item.id" class="bg-myblack-2 p-3 rounded-md flex items-center space-x-3">
          <img :src="item.cover_image" alt="Обложка" class="w-16 h-16 object-cover rounded">
          <div>
            <p class="font-medium text-mywhite-5">{{ item.product_name }}</p>
            <p class="text-sm text-mywhite-3">Модель: {{ item.distribution_model }}</p>
            <p class="text-xs mt-1" :class="{
              'text-myred-4': item.is_blocked,
              'text-mypurple-4': !item.is_blocked
            }">
              {{ item.is_blocked ? 'Заблокирован' : 'Активен' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import profileService from '@/services/profileService'

const loading = ref(true)
const error = ref(null)
const products = ref([])
const games = ref([])
const otherProducts = ref([])

onMounted(async () => {
  try {
    const response = await profileService.getUserProducts()
    products.value = response.data

    // Разделяем по is_game
    games.value = products.value.filter(p => p.is_game === true)
    otherProducts.value = products.value.filter(p => p.is_game !== true)

  } catch (err) {
    error.value = 'Ошибка загрузки продуктов.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}
</script>