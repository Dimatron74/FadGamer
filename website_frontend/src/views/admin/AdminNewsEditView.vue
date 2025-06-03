<template>
  <div class="p-6 bg-myblack-2 text-mywhite-5 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Редактировать новость</h1>

    <form @submit.prevent="submit" class="space-y-6">
      <!-- Заголовок -->
      <div>
        <label class="block text-sm font-medium text-mywhite-3 mb-1">Заголовок</label>
        <input v-model="form.title" type="text" required
               class="w-full p-2 rounded bg-myblack-3 text-mywhite-5 border border-myblack-4 focus:outline-none focus:ring focus:ring-mypurple-4">
      </div>

      <!-- Краткое описание -->
      <div>
        <label class="block text-sm font-medium text-mywhite-3 mb-1">Краткое описание</label>
        <textarea v-model="form.short_description" rows="3"
                  class="w-full p-2 rounded bg-myblack-3 text-mywhite-5 border border-myblack-4 focus:outline-none focus:ring focus:ring-mypurple-4"></textarea>
      </div>

      <!-- Обложка -->
      <div>
        <label class="block text-sm font-medium text-mywhite-3 mb-1">Обложка</label>
        <div v-if="form.cover_image_url" class="mb-2">
          <img :src="form.cover_image_url" alt="Текущая обложка" class="w-40 h-24 object-cover rounded border border-myblack-4">
        </div>
        <input type="file" accept="image/*" @change="handleCoverImage"
               class="w-full p-2 rounded bg-myblack-3 text-mywhite-5 border border-myblack-4 focus:outline-none focus:ring focus:ring-mypurple-4">
      </div>

      <!-- Блоки -->
      <div>
        <label class="block text-sm font-medium text-mywhite-3 mb-1">Блоки новости</label>
        <div v-for="(block, index) in form.blocks" :key="index"
             class="bg-myblack-3 p-4 rounded-lg mb-4 relative">
          <button type="button" @click="removeBlock(index)"
                  class="absolute top-2 right-2 text-myred-4 hover:text-myred-5">×</button>

          <!-- Тип блока -->
          <div class="mb-3">
            <select v-model="block.block_type"
                    class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4">
              <option v-for="type in blockTypes" :key="type.value" :value="type.value">{{ type.label }}</option>
            </select>
          </div>

          <!-- Содержимое -->
          <div v-if="block.block_type === 'text'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Текст</label>
            <textarea v-model="block.content" rows="4"
                      class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4"></textarea>
          </div>

          <div v-if="block.block_type === 'image'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Изображение</label>
            <div v-if="block.image" class="mb-2">
              <img :src="block.image" alt="Текущее изображение" class="w-40 h-24 object-cover rounded border border-myblack-4">
            </div>
            <input type="file" accept="image/*" @change="handleBlockImage($event, index)"
                   class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4">
          </div>

          <div v-if="block.block_type === 'video'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Видео (URL)</label>
            <input v-model="block.video_url" type="url"
                   class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4">
          </div>

          <div v-if="block.block_type === 'quote'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Цитата</label>
            <textarea v-model="block.content" rows="2"
                      class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4"></textarea>
          </div>

          <!-- Порядок -->
          <div>
            <label class="block text-xs text-mywhite-3 mb-1">Порядок</label>
            <input v-model.number="block.order" type="number" min="0"
                   class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4">
          </div>
        </div>

        <button type="button" @click="addBlock"
                class="mt-2 px-3 py-1 bg-mypurple-4 hover:bg-mypurple-5 text-white rounded transition-colors duration-200 text-sm">
          + Добавить блок
        </button>
      </div>

      <!-- Кнопка отправки -->
      <div>
        <button type="submit"
                class="px-4 py-2 bg-mypurple-4 hover:bg-mypurple-5 text-white rounded transition-colors duration-200">
          Сохранить изменения
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import AdminService from '@/services/AdminService'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const slug = route.params.slug

// Форма
const form = ref({
  title: '',
  short_description: '',
  cover_image: null,
  cover_image_url: null,
  slug: '',
  blocks: []
})

const loading = ref(true)
const error = ref(null)

// Типы блоков
const blockTypes = [
  { value: 'text', label: 'Текст' },
  { value: 'image', label: 'Изображение' },
  { value: 'video', label: 'Видео' },
  { value: 'quote', label: 'Цитата' }
]

// Загрузка данных
onMounted(async () => {
  try {
    const response = await AdminService.getNews(slug)
    const data = response.data

    // Основные данные
    form.value.title = data.title
    form.value.short_description = data.short_description
    form.value.slug = data.slug
    form.value.cover_image_url = data.cover_image || null

    // Блоки
    form.value.blocks = data.blocks.map((block, index) => ({
      id: block.id,
      block_type: block.block_type,
      content: block.content || '',
      video_url: block.video_url || '',
      image: block.image || null,
      order: block.order || index
    }))
  } catch (err) {
    error.value = 'Не удалось загрузить новость'
    console.error(err)
  } finally {
    loading.value = false
  }
})

function addBlock() {
  form.value.blocks.push({
    block_type: 'text',
    content: '',
    video_url: '',
    image: null,
    order: form.value.blocks.length
  })
}

function removeBlock(index) {
  form.value.blocks.splice(index, 1)
}

function handleCoverImage(event) {
  const file = event.target.files[0]
  if (file && isImage(file)) {
    form.value.cover_image = file
  } else {
    alert('Неверный формат файла. Только изображения.')
  }
}

function handleBlockImage(event, index) {
  const file = event.target.files[0]
  if (file && isImage(file)) {
    form.value.blocks[index].image = file
  } else {
    alert('Неверный формат файла. Только изображения.')
  }
}

function isImage(file) {
  return file.type.startsWith('image/')
}

async function submit() {
  const formData = new FormData()

  // Основные поля
  formData.append('title', form.value.title)
  formData.append('short_description', form.value.short_description)

  // Обложка
  if (form.value.cover_image) {
    formData.append('cover_image', form.value.cover_image)
  }

  // Блоки
  form.value.blocks.forEach((block, index) => {
    formData.append(`blocks[${index}][id]`, block.id || '')
    formData.append(`blocks[${index}][block_type]`, block.block_type)
    formData.append(`blocks[${index}][order]`, block.order)

    if (block.block_type === 'text' || block.block_type === 'quote') {
      formData.append(`blocks[${index}][content]`, block.content)
    } else if (block.block_type === 'video') {
      formData.append(`blocks[${index}][video_url]`, block.video_url)
    } else if (block.block_type === 'image') {
      if (block.image instanceof File) {
        // Новое изображение
        formData.append(`blocks[${index}][image]`, block.image)
      } else {
        // Старое изображение — передаем относительный путь
        const existingImage = block.image?.replace(/^.*\/\/[^\/]+/, '') || ''
        formData.append(`blocks[${index}][existing_image]`, existingImage)
      }
    }
  })

  try {
    await AdminService.updateNews(slug, formData)
    router.push({ name: 'admin-news-list' })
  } catch (err) {
    alert('Ошибка при сохранении')
    console.error(err)
  }
}
</script>