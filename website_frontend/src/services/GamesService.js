// src/services/GamesService.js
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const apiClient = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})



export default {
  getGames() {
    return apiClient.get('/games/')
  },
  getGame(slug) {
    return apiClient.get(`/games/${slug}/`)
  }
}