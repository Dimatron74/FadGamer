// src/services/ticketService.js

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
  getTickets() {
    return apiClient.get('/support/tickets/')
  },

  getTicket(ticketId) {
    return apiClient.get(`/support/tickets/${ticketId}/`)
  },

  getMessages(ticketId) {
    return apiClient.get(`/support/tickets/${ticketId}/messages/`)
  },

  sendMessage(ticketId, messageData) {
    return apiClient.post(`/support/tickets/${ticketId}/messages/`, messageData)
  },

  updateTicketStatus(ticketId, status) {
    return apiClient.patch(`/support/tickets/${ticketId}/`, { status })
  }
}