// src/stores/useTicketStore.js

import { defineStore } from 'pinia'
import ticketApi from '@/services/ticketService'

export const useTicketStore = defineStore('ticket', {
  state: () => ({
    tickets: [],
    loading: false,
    error: null,
    selectedStatus: '',
    searchQuery: ''
  }),

  actions: {
    async fetchTickets() {
      this.loading = true
      this.error = null
      try {
        const res = await ticketApi.getTickets()
        this.tickets = res.data
      } catch (err) {
        this.error = 'Не удалось загрузить тикеты'
        console.error(err)
      } finally {
        this.loading = false
      }
    },

    setSelectedStatus(status) {
      this.selectedStatus = status
    },

    setSearchQuery(query) {
      this.searchQuery = query
    }
  },

  getters: {
    filteredTickets: (state) => {
      return state.tickets.filter((ticket) => {
        const matchesStatus = state.selectedStatus ? ticket.status === state.selectedStatus : true
        const matchesSearch = state.searchQuery
          ? ticket.title.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
            ticket.description.toLowerCase().includes(state.searchQuery.toLowerCase())
          : true
        return matchesStatus && matchesSearch
      })
    }
  }
})