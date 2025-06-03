<template>
  <div class="p-6 bg-myblack-2 text-mywhite-5 min-h-screen">
    <!-- Заголовок и кнопка добавления -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Новости</h1>
      <router-link
        :to="{ name: 'admin-news-create' }"
        class="px-4 py-2 bg-mypurple-4 hover:bg-mypurple-5 text-white rounded transition-colors duration-200"
      >
        Добавить новость
      </router-link>
    </div>

    <!-- Статусы загрузки -->
    <div v-if="loading" class="text-center py-10">Загрузка новостей...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>

    <!-- Основной контент -->
    <div v-else>
      <!-- Список новостей -->
      <div
        v-if="newsList.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="news in newsList"
          :key="news.id"
          class="bg-myblack-3 rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-shadow duration-300"
        >
          <!-- Обложка -->
          <img
            :src="news.cover_image"
            alt="Обложка"
            class="w-full h-40 object-cover"
          />

          <!-- Контент -->
          <div class="p-4">
            <h2 class="text-lg font-semibold mb-2 truncate">{{ news.title }}</h2>
            <p class="text-sm text-mywhite-3 mb-3 line-clamp-2">
              {{ news.short_description || 'Краткое описание отсутствует' }}
            </p>
            <p class="text-xs text-mywhite-2 mb-4">
              {{ formatDate(news.created_at) }}
            </p>

            <!-- Кнопки -->
            <div class="flex space-x-2">
              <router-link
                v-if="news.slug"
                :to="{ name: 'admin-news-edit', params: { slug: news.slug } }"
                class="flex-1 px-3 py-1 bg-mypurple-4 hover:bg-mypurple-5 text-white text-center rounded transition-colors duration-200 text-sm"
              >
                Редактировать
              </router-link>
              <button
                @click="deleteNews(news.slug)"
                class="flex-1 px-3 py-1 bg-myred-4 hover:bg-myred-5 text-white text-center rounded transition-colors duration-200 text-sm"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Если нет новостей -->
      <div v-else class="text-center py-10 text-mywhite-3">
        Новостей пока нет.
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminService from '@/services/AdminService'
import { ref, onMounted } from 'vue'

// Состояние
const newsList = ref([])
const loading = ref(true)
const error = ref(null)

// Загрузка данных
onMounted(async () => {
  try {
    const response = await AdminService.getNewsList()
    console.log(response)

    // Проверяем, есть ли данные и это массив
    if (Array.isArray(response?.data)) {
      newsList.value = response.data
    } else {
      throw new Error('Неверный формат данных')
    }
  } catch (err) {
    console.error('Ошибка при загрузке новостей:', err)
    error.value = 'Не удалось загрузить список новостей.'
  } finally {
    loading.value = false
  }
})

// Формат даты
function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// Удаление новости
async function deleteNews(slug) {
  const confirmed = confirm('Вы уверены, что хотите удалить эту новость?')
  if (!confirmed) return

  try {
    await AdminService.deleteNews(slug)
    // Обновляем список, исключая удалённую новость
    newsList.value = newsList.value.filter((n) => n.slug !== slug)
  } catch (err) {
    alert('Ошибка при удалении новости')
    console.error('Ошибка при удалении новости:', err)
  }
}
</script>