<template>
  <div class="p-6 bg-myblack-2 text-mywhite-5 min-h-screen">
    <h1 class="text-2xl font-bold mb-6">Создать новость</h1>

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

          <!-- Контент -->
          <div v-if="block.block_type === 'text'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Текст (обычный)</label>
            <textarea v-model="block.content" rows="4"
                      class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4"></textarea>
          </div>

          <!-- Tiptap -->
          <div v-if="block.block_type === 'tiptap'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Текст (расширенный)</label>
            <TiptapEditor
              v-model="block.content"
              class="w-full p-2 rounded bg-myblack-2 text-mywhite-5 border border-myblack-4"
            />
          </div>

          <div v-if="block.block_type === 'image'" class="mb-3">
            <label class="block text-xs text-mywhite-3 mb-1">Изображение</label>
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
          Опубликовать
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import AdminService from '@/services/AdminService'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import TiptapEditor from '@/components/main/TiptapEditor.vue'

const router = useRouter()

const form = ref({
  title: '',
  short_description: '',
  cover_image: null,
  blocks: []
})

// Типы блоков
const blockTypes = [
  { value: 'text', label: 'Текст (обычный)' },
  { value: 'tiptap', label: 'Текст (расширенный)' },
  { value: 'image', label: 'Изображение' },
  { value: 'video', label: 'Видео' },
  { value: 'quote', label: 'Цитата' }
]

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

  // Обязательные поля
  formData.append('title', form.value.title)
  formData.append('short_description', form.value.short_description)

  // Обложка
  if (form.value.cover_image) {
    formData.append('cover_image', form.value.cover_image)
  }

  // Блоки
  form.value.blocks.forEach((block, index) => {
    formData.append(`blocks[${index}][block_type]`, block.block_type)
    formData.append(`blocks[${index}][order]`, block.order)

    if (block.block_type === 'text' || block.block_type === 'quote' || block.block_type === 'tiptap') {
      formData.append(`blocks[${index}][content]`, block.content)
    } else if (block.block_type === 'image' && block.image) {
      formData.append(`blocks[${index}][image]`, block.image)
    } else if (block.block_type === 'video') {
      formData.append(`blocks[${index}][video_url]`, block.video_url)
    }
  })

  try {
    await AdminService.createNews(formData)
    router.push({ name: 'admin-news-list' })
  } catch (err) {
    console.error('Ошибка при создании новости:', err)
    alert('Не удалось сохранить новость')
  }
}
</script>