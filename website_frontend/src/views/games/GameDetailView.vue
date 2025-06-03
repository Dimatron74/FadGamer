<!-- src/views/games/GameDetailView.vue -->
<template>
  <div class="min-h-screen bg-myblack-2 text-mywhite-5 p-6">
    <div v-if="loading" class="text-center py-10">
      <p>Загрузка игры...</p>
    </div>
    <div v-else-if="error" class="text-red-500 text-center py-10">
      {{ error }}
    </div>
    <div v-else class="max-w-4xl mx-auto">
      <div class="bg-myblack-3 rounded-lg overflow-hidden shadow-xl">
        <img :src="game.cover_image" :alt="game.name" class="w-full h-64 object-cover" />
        <div class="p-6">
          <h1 class="text-3xl font-bold mb-4">{{ game.name }}</h1>
          <p class="text-mywhite-3 mb-6">{{ game.description }}</p>

          <div class="mb-4">
            <strong class="text-mywhite-4">Жанры:</strong>
            <ul class="flex space-x-2 mt-1">
              <li v-for="(genre, index) in game.genres" :key="index" class="text-mypurple-4">
                {{ genre.name }}
              </li>
            </ul>
          </div>

          <div class="mb-4">
            <strong class="text-mywhite-4">Платформы:</strong>
            <ul class="flex flex-wrap gap-2 mt-1">
              <li v-for="(platform, index) in game.platforms" :key="index" class="text-xs bg-myblack-4 px-2 py-1 rounded">
                {{ platform.name }}
              </li>
            </ul>
          </div>

          <div class="flex gap-4">
            <a
              v-for="method in game.acquisition_methods"
              :key="method.id"
              :href="method.url"
              target="_blank"
              rel="noopener noreferrer"
              class="px-4 py-2 bg-mypurple-4 hover:bg-mypurple-5 text-white rounded transition-colors duration-200"
            >
              {{ method.service.name }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import GamesService from '@/services/GamesService'

const route = useRoute()
const game = ref({})
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const slug = route.params.slug
    const response = await GamesService.getGame(slug)
    game.value = response.data
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о игре'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>