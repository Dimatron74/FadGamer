// src/services/ContactService.js

import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
})

// Перехватчик для добавления токена (если есть)
apiClient.interceptors.request.use(async config => {
  const userStore = useUserStore()
  if (userStore.user.isAuthenticated) {
    if (!userStore.user.access) {
      try {
        await userStore.refreshToken()
      } catch (e) {
        console.warn('Не удалось обновить токен — запрос будет отправлен без авторизации')
      }
    }
    config.headers.Authorization = `Bearer ${userStore.user.access}`
  } else {
    // Неавторизированный пользователь — убираем заголовок Authorization
    delete config.headers.Authorization
  }
  return config
})

export default {
  submitContactRequest(data) {
    return apiClient.post('contact/submit/', data)
  },
}