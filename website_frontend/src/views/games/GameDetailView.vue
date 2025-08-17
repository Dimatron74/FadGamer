<!-- src/views/games/GameDetailView.vue -->
<template>
  <div class="min-h-screen bg-myblack-2 text-mywhite-5">
    <!-- Состояния загрузки / ошибки -->
    <div v-if="loading" class="text-center py-20 text-lg text-mywhite-3">Загрузка игры...</div>
    <div v-else-if="error" class="text-center py-20 text-red-500">{{ error }}</div>

    <!-- Контент -->
    <div v-else class="max-w-6xl mx-auto px-4 lg:px-8 py-10 space-y-12">
      <!-- Hero: обложка и трейлер -->
      <section class="relative rounded-2xl overflow-hidden shadow-xl">
        <img
          :src="game.cover_image"
          :alt="game.name"
          class="w-full h-[400px] object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-myblack-2/90 via-myblack-2/40 to-transparent"></div>
        <div class="absolute bottom-0 left-0 p-6 md:p-10">
          <h1 class="text-4xl md:text-5xl font-extrabold text-white drop-shadow-lg">
            {{ game.name }}
          </h1>
          <p class="mt-3 text-mywhite-3 max-w-2xl">
            {{ game.tagline || game.short_description || 'Добро пожаловать в мир игры!' }}
          </p>
        </div>
      </section>

      <!-- Основной блок -->
      <section class="grid lg:grid-cols-3 gap-10">
        <!-- Левая колонка -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Описание -->
          <div class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4">
            <h2 class="text-2xl font-bold mb-4">Об игре</h2>
            <p class="text-mywhite-3 leading-relaxed whitespace-pre-line">
              {{ game.description }}
            </p>
          </div>

          <!-- Галерея скриншотов -->
          <div v-if="game.screenshots?.length" class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4">
            <h2 class="text-2xl font-bold mb-4">Галерея</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <img
                v-for="(shot, idx) in game.screenshots"
                :key="idx"
                :src="shot"
                :alt="`Скриншот ${idx+1}`"
                class="rounded-lg object-cover h-40 w-full hover:opacity-90 transition"
              />
            </div>
          </div>

          <!-- Особенности -->
          <div v-if="game.features?.length" class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4">
            <h2 class="text-2xl font-bold mb-4">Особенности</h2>
            <ul class="list-disc list-inside space-y-2 text-mywhite-3">
              <li v-for="(feature, idx) in game.features" :key="idx">{{ feature.name }}</li>
            </ul>
          </div>

          <!-- Системные требования -->
          <div v-if="game.requirements" class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4">
            <h2 class="text-2xl font-bold mb-4">Системные требования</h2>
            <div class="grid md:grid-cols-2 gap-6 text-mywhite-3">
              <div>
                <h3 class="font-semibold mb-2">Минимальные</h3>
                <ul class="space-y-1 text-sm">
                  <li v-for="(val, key) in game.requirements.min" :key="key">
                    <strong>{{ key }}:</strong> {{ val }}
                  </li>
                </ul>
              </div>
              <div v-if="game.requirements.recommended">
                <h3 class="font-semibold mb-2">Рекомендуемые</h3>
                <ul class="space-y-1 text-sm">
                  <li v-for="(val, key) in game.requirements.recommended" :key="key">
                    <strong>{{ key }}:</strong> {{ val }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Правая колонка (инфо-карточка) -->
        <aside class="space-y-6">
          <div class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4 space-y-4">
            <h2 class="text-xl font-bold">Информация</h2>
            <p><strong>Дата выхода:</strong> {{ game.release_date || 'TBA' }}</p>
            <p><strong>Разработчик:</strong> {{ game.developer || 'Неизвестно' }}</p>
            <p><strong>Издатель:</strong> {{ game.publisher || 'Неизвестно' }}</p>

            <div>
              <strong>Жанры:</strong>
              <ul class="flex flex-wrap gap-2 mt-1">
                <li
                  v-for="(genre, idx) in game.genres"
                  :key="idx"
                  class="bg-myred-4/10 text-myred-4 px-2 py-1 text-xs rounded"
                >
                  {{ genre.name }}
                </li>
              </ul>
            </div>

            <div>
              <strong>Платформы:</strong>
              <ul class="flex flex-wrap gap-2 mt-1">
                <li
                  v-for="(platform, idx) in game.platforms"
                  :key="idx"
                  class="bg-myblack-4 px-2 py-1 text-xs rounded"
                >
                  {{ platform.name }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Кнопки приобретения -->
          <div v-if="game.acquisition_methods?.length" class="bg-myblack-3 rounded-xl p-6 shadow-md border border-myblack-4">
            <h2 class="text-xl font-bold mb-4">Играть:</h2>
            <div class="flex flex-col gap-3">
              <a
                v-for="method in game.acquisition_methods"
                :key="method.id"
                :href="method.url"
                target="_blank"
                rel="noopener noreferrer"
                class="px-4 py-2 rounded-lg bg-mypurple-4 hover:bg-mypurple-5 text-center font-semibold transition-colors"
              >
                {{ method.service.name }}
              </a>
            </div>
          </div>
        </aside>
      </section>
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
    console.log('Game data:', game.value)
  } catch (err) {
    error.value = 'Не удалось загрузить информацию о игре'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>
