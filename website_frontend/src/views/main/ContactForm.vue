<template>
  <section class="bg-myblack-2 p-6 rounded-lg shadow-md">
    <h2 class="text-3xl font-bold mb-4 text-mywhite-5">Связь с поддержкой</h2>
    <form @submit.prevent="submitRequest" class="space-y-4">
      <div v-if="!isLoggedIn">
        <label for="name" class="block text-mywhite-2 mb-1">Имя</label>
        <input v-model="form.name" type="text" id="name" placeholder="Ваше имя" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4" />
      </div>
      <div v-if="!isLoggedIn">
        <label for="email" class="block text-mywhite-2 mb-1">Email</label>
        <input v-model="form.email" type="email" id="email" placeholder="Ваш email" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4" />
      </div>
      <div>
        <label for="subject" class="block text-mywhite-2 mb-1">Тема</label>
        <input v-model="form.subject" type="text" id="subject" placeholder="Тема обращения" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4" />
      </div>
      <div>
        <label for="message" class="block text-mywhite-2 mb-1">Сообщение</label>
        <textarea v-model="form.message" id="message" rows="4" placeholder="Текст сообщения" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4"></textarea>
      </div>
      <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-5 text-myblack-1 px-6 py-2 rounded font-semibold transition duration-300">
        Отправить
      </button>
      <p v-if="successMessage" class="text-green-500">{{ successMessage }}</p>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import contactService from '@/services/ContactService'

const userStore = useUserStore()
const isLoggedIn = ref(userStore.user.isAuthenticated)

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const successMessage = ref('')
const errorMessage = ref('')

const submitRequest = async () => {
  try {
    const data = { ...form.value }
    if (!isLoggedIn.value) {
      // Только если пользователь не авторизован
      data.email = form.value.email
    } else {
      delete data.email // Удаляем, пусть бэкенд сам возьмёт из профиля
    }

    await contactService.submitContactRequest(data)
    successMessage.value = 'Запрос успешно отправлен!'
  } catch (err) {
    errorMessage.value = 'Ошибка при отправке запроса.'
  }
}
</script>