<template>
  <section class="relative mx-auto">
    <!-- Заголовок -->
    <h2 class="text-3xl font-bold mb-6 text-mywhite-1">Наши игры</h2>

    <!-- Контейнер слайдера -->
    <div class="relative overflow-hidden rounded-xl shadow-2xl bg-myblack-3">
      <!-- Прелоадер -->
      <div v-if="loading" class="flex justify-center items-center h-80 text-mywhite-3">
        Загрузка...
      </div>

      <!-- Ошибка -->
      <div v-else-if="error" class="text-red-500 p-4">{{ error }}</div>

      <!-- Слайд -->
      <router-link :to="{ name: 'game-detail', params: { slug: currentGame.slug } }" v-else class="transition-all duration-500 ease-in-out transform">
        <img
          :src="currentGame.cover_image"
          :alt="currentGame.name"
          class="w-full h-96 object-cover transition-transform duration-700 hover:scale-105"
        />

        <!-- Название игры поверх изображения -->
        <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-myblack-2 to-transparent p-6">
          <h3 class="text-2xl font-bold text-mywhite-1">{{ currentGame.name }}</h3>
          <p class="text-sm text-mywhite-3 mt-1">
            {{ formatDate(currentGame.release_date) }}
          </p>
        </div>
      </router-link>

      <!-- Кнопки навигации -->
      <button
        @click="prevSlide"
        class="absolute left-4 top-1/2 transform -translate-y-1/2 z-10 bg-mypurple-5 hover:bg-mypurple-4 text-myblack-1 w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-colors duration-300"
        aria-label="Предыдущая игра"
      >
        ❮
      </button>
      <button
        @click="nextSlide"
        class="absolute right-4 top-1/2 transform -translate-y-1/2 z-10 bg-mypurple-5 hover:bg-mypurple-4 text-myblack-1 w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-colors duration-300"
        aria-label="Следующая игра"
      >
        ❯
      </button>
    </div>

    <!-- Индикаторы -->
    <div class="flex justify-center mt-4 space-x-2">
      <button
        v-for="(game, index) in games.value"
        :key="game.id"
        :class="[
          'w-3 h-3 rounded-full transition-all duration-300',
          index === currentGameIndex ? 'bg-mypurple-5 scale-125' : 'bg-mywhite-2 hover:bg-mywhite-3'
        ]"
        @click="currentGameIndex = index"
        :aria-label="'Перейти к слайду ' + (index + 1)"
      ></button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import GamesService from '@/services/GamesService'

const games = ref([])
const loading = ref(true)
const error = ref(null)
const currentGameIndex = ref(0)

// Получаем данные об играх
onMounted(async () => {
  try {
    const response = await GamesService.getGames()
    games.value = response.data.slice(-3) // Берём последние 3 опубликованные игры
  } catch (err) {
    error.value = 'Ошибка загрузки игр.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// Текущая игра
const currentGame = computed(() => {
  return games.value.length > 0 ? games.value[currentGameIndex.value] : null
})

// Функции для навигации
function nextSlide() {
  currentGameIndex.value = (currentGameIndex.value + 1) % games.value.length
}

function prevSlide() {
  currentGameIndex.value =
    (currentGameIndex.value - 1 + games.value.length) % games.value.length
}

// Форматирование даты
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}
</script>