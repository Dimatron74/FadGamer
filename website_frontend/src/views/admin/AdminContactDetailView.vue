<template>
  <div class="bg-myblack-2 p-6 rounded-lg shadow-md">
    <RouterLink to="/admin/contacts" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd"
          d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H17a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z"
          clip-rule="evenodd" />
      </svg>
      Назад к обращениям
    </RouterLink>
    <h2 class="text-2xl font-bold mb-4 text-mywhite-5">Запрос связи</h2>
    <div class="mb-4">
        <p class="text-mywhite-2"><strong>Автор:</strong> 
            {{ request.name || 'Не указан' }}
            <span v-if="!request.user" class="text-yellow-500 text-sm ml-1">(Гость)</span>
        </p>

        <p class="text-mywhite-2"><strong>Email:</strong> 
            {{ request.email?.email || request.guest_email || '-' }}
        </p>

        <p class="text-mywhite-2"><strong>Тема:</strong> {{ request.subject }}</p>
        <p class="text-mywhite-2 mt-2"><strong>Сообщение:</strong></p>
        <p class="bg-myblack-3 p-3 rounded mt-1">{{ request.message }}</p>
    </div>
    <div v-if="request.admin_response" class="mt-6">
      <p class="text-mywhite-2"><strong>Ответ:</strong></p>
      <p class="bg-myblack-3 p-3 rounded mt-1">{{ request.admin_response }}</p>
    </div>
    <div v-else class="mt-6">
      <label for="response" class="block text-mywhite-2 mb-1">Ответ администратора</label>
      <textarea v-model="responseText" id="response" rows="5" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4"></textarea>
      <button @click="sendResponse" class="mt-2 bg-mypurple-4 hover:bg-mypurple-5 text-myblack-1 px-4 py-2 rounded font-semibold transition duration-300">
        Отправить ответ
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import AdminService from '@/services/AdminService'
import { send_company_email } from '@/services/EmailService' // Подключаем сервис

const route = useRoute()
const router = useRouter()
const requestId = route.params.id
const request = ref({})
const responseText = ref('')

onMounted(async () => {
  try {
    const res = await AdminService.getContactRequest(route.params.id)
    request.value = res.data
  } catch (err) {
    alert('Не удалось загрузить обращение.')
  }
})

const sendResponse = async () => {
  try {
    await AdminService.sendResponse(request.value.id, {
      admin_response: responseText.value,
      is_resolved: true
    })

    // Теперь отправляем email
    const recipient = request.value.guest_email || request.value.email?.email
    if (recipient) {
      const success = send_company_email(
        recipient,
        'contact_response',
        { response: responseText.value }
      )

      if (success) {
        alert('Ответ успешно отправлен!')
      } else {
        alert('Письмо не отправлено, но ответ сохранён')
      }
    }
    router.push('/admin/contacts')

  } catch (err) {
    alert('Ошибка при отправке ответа.')
  }
}
</script>