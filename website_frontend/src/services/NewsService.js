// services/newsService.js
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})



export default {
  getNews() {
    return apiClient.get('/news/')
  },
  getNewsBySlug(slug) {
    return apiClient.get(`/news/${slug}/`)
  }
}