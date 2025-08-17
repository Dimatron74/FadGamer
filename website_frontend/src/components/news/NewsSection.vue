<template>
  <section class="mt-16">
    <!-- Заголовок -->
    <h2 class="text-4xl font-extrabold mb-8 text-myred-5">Новости</h2>

    <!-- Контейнер -->
    <div class="flex flex-col md:flex-row gap-8 items-start bg-myblack-2 p-6 rounded-xl shadow-lg">
      <!-- Большое изображение активной новости -->
      <div class="md:w-2/5 w-full relative rounded-lg overflow-hidden shadow-md transition-transform duration-300 transform hover:scale-105">
        <router-link :to="{ name: 'news-detail', params: { slug: activeNews?.slug ? activeNews.slug : 'no-slug' }}">
            <img
            :src="activeNews.cover_image"
            alt="Изображение новости"
            class="w-full h-96 object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-myblack-2 to-transparent opacity-80"></div>
            <div class="absolute bottom-0 left-0 p-4 text-mywhite-1">
            <h3 class="text-2xl font-bold">{{ activeNews.title }}</h3>
            <p class="text-sm text-mywhite-3 mt-1">{{ formatDate(activeNews.created_at) }}</p>
            </div>
        </router-link>
      </div>

      <!-- Список новостей -->
      <div class="md:w-3/5 space-y-3">
        <div
          v-for="(newsItem, index) in newsItems"
          :key="newsItem.id"
          @mouseenter="setActiveNews(index)"
          class="group cursor-pointer p-3 rounded-lg transition-all duration-300 shadow-sm"
          :class="[
            activeNews?.id === newsItem.id
              ? 'bg-myblack-3 border-l-4 border-mypurple-4'
              : 'bg-myblack-2 border-l-4 border-transparent hover:bg-myblack-3 hover:border-mypurple-4'
          ]"
        >
          <router-link :to="{ name: 'news-detail', params: { slug: newsItem.slug }}">
            <h3 class="text-lg font-semibold group-hover:text-mypurple-4 transition-colors duration-300 line-clamp-1">
                {{ newsItem.title }}
            </h3>
            <p class="text-xs text-mywhite-3 mt-1 line-clamp-2">
                {{ newsItem.short_description || 'Без описания' }}
            </p>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NewsService from '@/services/NewsService'

const newsItems = ref([])
const activeNews = ref({})

// Получаем данные о новостях через API
onMounted(async () => {
  try {
    const response = await NewsService.getNews()
    newsItems.value = response.data.slice(-5) // Берём последние 5 новостей
    if (newsItems.value.length > 0) {
      activeNews.value = newsItems.value[0]
    }
  } catch (error) {
    console.error('Ошибка при получении данных о новостях:', error)
  }
})

// Установка активной новости при наведении
function setActiveNews(index) {
  activeNews.value = newsItems.value[index]
}

// Форматирование даты
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}
</script>