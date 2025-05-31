// src/services/promoCodeService.js

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
  getPromoCodes() {
    return apiClient.get('/admin_panel/promocodes/')
  },
  createPromoCode(data) {
    return apiClient.post('/admin_panel/promocodes/', data)
  },
  updatePromoCode(id, data) {
    return apiClient.patch(`/admin_panel/promocodes/${id}/`, data)
  },
  deletePromoCode(id) {
    return apiClient.delete(`/admin_panel/promocodes/${id}/`)
  },
  getPromoCode(id) {
    return apiClient.get(`/admin_panel/promocodes/${id}/`)
  },
  getServices() {
    return apiClient.get('/admin_panel/promocodes/services/')
  },
  getBonusTypes() {
    return apiClient.get('/admin_panel/promocodes/bonus_types/')
  },
  activatePromoCode(data) {
    return apiClient.post('/admin_panel/promocodes/activate/', data)
  }
}