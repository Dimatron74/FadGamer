<template>
  <div class="min-h-screen bg-myblack-2 text-mywhite-5 p-6">
    <h1 class="text-3xl font-bold mb-8">Новости</h1>

    <div v-if="loading" class="text-center py-10">Загрузка...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="article in news"
        :key="article.id"
        :to="{ name: 'news-detail', params: { slug: article.slug }}"
        class="bg-myblack-3 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300"
      >
        <img
          :src="article.cover_image"
          alt="Обложка"
          class="w-full h-48 object-cover"
        />
        <div class="p-4">
          <h2 class="text-xl font-semibold mb-2 truncate">{{ article.title }}</h2>
          <p class="text-mywhite-3 text-sm mb-3">{{ article.short_description }}</p>
          <span class="text-xs text-mywhite-2">{{ formatDate(article.created_at) }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NewsService from '@/services/NewsService'

const news = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await NewsService.getNews()
    news.value = response.data
  } catch (err) {
    error.value = 'Ошибка загрузки новостей.'
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