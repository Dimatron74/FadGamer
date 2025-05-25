<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 max-w-2xl mx-auto">
    <RouterLink to="/profile/support" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd"
          d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H17a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z"
          clip-rule="evenodd" />
      </svg>
      Назад
    </RouterLink>

    <h1 class="text-2xl font-bold text-mywhite-5 mb-6">Создать новый запрос</h1>

    <form @submit.prevent="submitTicket" class="space-y-4">
      <div>
        <label class="block text-mywhite-2 mb-1">Заголовок</label>
        <input
          v-model="formData.title"
          type="text"
          required
          class="w-full bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4"
        />
      </div>

      <div>
        <label class="block text-mywhite-2 mb-1">Описание проблемы</label>
        <textarea
          v-model="formData.description"
          rows="6"
          required
          class="w-full bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4"
        ></textarea>
      </div>

      <div>
        <label class="block text-mywhite-2 mb-1">Сервис</label>
        <select
          v-model="formData.service"
          required
          class="w-full bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4"
        >
          <option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
        </select>
      </div>

      <div>
        <label class="block text-mywhite-2 mb-1">Категория</label>
        <select
          v-model="formData.category"
          required
          class="w-full bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4"
        >
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>

      <button
        type="submit"
        class="mt-4 bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md"
      >
        Отправить запрос
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const formData = ref({
  title: '',
  description: '',
  service: null,
  category: null
})

const services = ref([])
const categories = ref([])

// Загрузка сервисов и категорий
async function loadServicesAndCategories() {
  try {
    const serviceRes = await axios.get('/support/services/')
    const categoryRes = await axios.get('/support/categories/')

    services.value = serviceRes.data
    categories.value = categoryRes.data
  } catch (e) {
    console.error('Не удалось загрузить данные')
  }
}

loadServicesAndCategories()

async function submitTicket() {
  if (!formData.value.title.trim() || !formData.value.description.trim()) {
    alert('Заполните заголовок и описание')
    return
  }

  if (!formData.value.service || !formData.value.category) {
    alert('Выберите сервис и категорию')
    return
  }

  const finalData = {
    title: formData.value.title,
    description: formData.value.description,
    service: formData.value.service,
    category: formData.value.category
  }

  try {
    const res = await axios.post('/support/tickets/', finalData)
    router.push(`/profile/support/${res.data.id}`)
  } catch (e) {
    console.error('Ошибка при создании тикета', e)

    if (e.response?.data) {
      const errors = Object.entries(e.response.data)
        .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
        .join('\n')

      alert(`Ошибка при создании тикета:\n${errors}`)
    } else {
      alert('Не удалось создать тикет')
    }
  }
}
</script>