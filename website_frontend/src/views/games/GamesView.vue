<!-- src/views/games/GamesView.vue -->
<template>
  <div class="min-h-screen bg-myblack-2 text-mywhite-5 p-6">
    <h1 class="text-3xl font-bold mb-8">Наши игры</h1>

    <div v-if="loading" class="flex justify-center items-center h-64">
      <p class="text-mywhite-3">Загрузка...</p>
    </div>

    <div v-else-if="error" class="text-red-500">
      {{ error }}
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <router-link
        v-for="game in games"
        :key="game.id"
        :to="{ name: 'game-detail', params: { slug: game.slug } }"
        class="block bg-myblack-3 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300"
      >
        <img
          :src="game.cover_image"
          :alt="game.name"
          class="w-full h-48 object-cover"
        />
        <div class="p-4">
          <h2 class="text-xl font-semibold mb-2">{{ game.name }}</h2>
          <div class="mb-2">
            <span v-for="(genre, index) in game.genres" :key="index" class="inline-block mr-2 text-sm text-mypurple-4">
              {{ genre.name }}
            </span>
          </div>
          <div class="flex flex-wrap gap-1">
            <span v-for="(platform, index) in game.platforms" :key="index" class="text-xs bg-myblack-4 px-2 py-1 rounded">
              {{ platform.name }}
            </span>
          </div>
          <button
            class="mt-4 w-full py-2 bg-mypurple-4 hover:bg-mypurple-5 text-white rounded transition-colors duration-200"
          >
            Получить
          </button>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GamesService from '@/services/GamesService'
import { useRouter } from 'vue-router'

const router = useRouter()
const games = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await GamesService.getGames()
    games.value = response.data
  } catch (err) {
    error.value = 'Ошибка загрузки игр. Попробуйте позже.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>