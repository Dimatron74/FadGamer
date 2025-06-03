// src/services/GamesService.js
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Перехватчик для добавления токена
apiClient.interceptors.request.use(async config => {
  const userStore = useUserStore()
  // Если нет access-токена — пытаемся обновить его
  if (!userStore.user.access) {
    try {
      await userStore.refreshToken()
    } catch (e) {
      console.error('Не удалось обновить токен')
      return Promise.reject(e)
    }
  }
  // Добавляем заголовок авторизации
  config.headers.Authorization = `Bearer ${userStore.user.access}`
  return config
})

export default {
  getGames() {
    return apiClient.get('/games/')
  },
  getGame(slug) {
    return apiClient.get(`/games/${slug}/`)
  }
}