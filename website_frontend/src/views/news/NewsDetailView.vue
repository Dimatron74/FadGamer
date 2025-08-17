<template>
  <div class="min-h-screen bg-myblack-2 text-mywhite-5 p-6">
    <div v-if="loading" class="text-center py-10">Загрузка новости...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

    <div v-else class="max-w-4xl mx-auto">
      <div class="mb-6">
        <div class="w-full max-h-[500px] flex items-center justify-center rounded-lg mb-4">
          <img :src="news.cover_image" :alt="news.title" class="max-w-full max-h-[500px] object-contain">
        </div>
        <h1 class="text-3xl font-bold mb-2">{{ news.title }}</h1>
        <p class="text-mywhite-3 mb-4">{{ news.short_description }}</p>
        <p class="text-xs text-mywhite-2">Опубликовано: {{ formatDate(news.created_at) }}</p>
        <p v-if="news.product" class="text-sm mt-2">Категория: {{ news.product.name }}</p>
      </div>

      <!-- Блоки -->
      <div class="space-y-6">
        <div v-for="block in news.blocks" :key="block.id" class="bg-myblack-2 p-4 rounded-lg">
          <!-- Текст -->
          <div v-if="block.block_type === 'text'" class="prose prose-invert max-w-none" v-html="block.content"></div>

          <!-- Tiptap (расширенный текст) -->
          <div v-else-if="block.block_type === 'tiptap'" class="tiptap-output" v-html="block.content"></div>

          <!-- Изображение -->
          <div v-if="block.block_type === 'image'" class="my-4">
            <img :src="block.image" :alt="block.order" class="w-full rounded-md">
          </div>

          <!-- Видео -->
          <div v-if="block.block_type === 'video'" class="aspect-video my-4">
            <iframe
              class="w-full h-full rounded-md"
              :src="block.video_url"
              frameborder="0"
              allowfullscreen
            ></iframe>
          </div>

          <!-- Цитата -->
          <div v-if="block.block_type === 'quote'" class="border-l-4 border-mypurple-4 pl-4 italic text-mywhite-3">
            {{ block.content }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NewsService from '@/services/NewsService'

const route = useRoute()
const news = ref({})
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const slug = route.params.slug
    const response = await NewsService.getNewsBySlug(slug)
    news.value = response.data
    console.log('Загруженные данные новости:', news.value)
  } catch (err) {
    error.value = 'Ошибка загрузки новости'
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