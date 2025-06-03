import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// // Перехватчик для добавления токена
// apiClient.interceptors.request.use(async config => {
//   const userStore = useUserStore()
//   if (!userStore.user.access) {
//     try {
//       await userStore.refreshToken()
//     } catch (e) {
//       console.error('Не удалось обновить токен')
//       return Promise.reject(e)
//     }
//   }
//   config.headers.Authorization = `Bearer ${userStore.user.access}`
//   return config
// })

export default {
  getNews() {
    return apiClient.get('/news/')
  },
  getNewsBySlug(slug) {
    return apiClient.get(`/news/${slug}/`)
  }
}