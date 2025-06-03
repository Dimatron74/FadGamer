import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
  headers: {}
})

// Перехватчик для добавления токена
apiClient.interceptors.request.use(async config => {
  const userStore = useUserStore()
  if (!userStore.user.access) {
    try {
      await userStore.refreshToken()
    } catch (e) {
      console.error('Не удалось обновить токен')
      return Promise.reject(e)
    }
  }
  config.headers.Authorization = `Bearer ${userStore.user.access}`
  return config
})

export default {
  // Создание новости
  createNews(data) {
    return apiClient.post('/admin_panel/news/create/', data)
  },
  getNews(slug) {
    return apiClient.get(`/admin_panel/news/${slug}/edit/`)
  },
  updateNews(slug, data) {
    return apiClient.post(`/admin_panel/news/${slug}/edit/`, data)
  },
  getNewsList() {
    return apiClient.get('/admin_panel/news/list/')
  },
  // Удаление новости
  deleteNews(slug) {
    return apiClient.delete(`/admin_panel/news/${slug}/delete/`)
  }
}