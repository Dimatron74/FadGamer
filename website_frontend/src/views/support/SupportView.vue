<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6">
    <!-- Заголовок -->
    <h1 class="text-3xl font-bold text-mywhite-5 mb-8">Техническая поддержка</h1>

    <!-- Фильтры -->
    <div class="flex flex-wrap gap-4 mb-6">
      <select v-model="selectedStatus" class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none">
        <option value="">Все статусы</option>
        <option value="open">Открытые</option>
        <option value="in_progress">В работе</option>
        <option value="closed">Закрытые</option>
      </select>

      <input
        type="text"
        placeholder="Поиск по запросам..."
        v-model="searchQuery"
        class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none w-full md:w-auto flex-1"
      />
    </div>

    <!-- Кнопка создания нового тикета -->
    <div class="mb-6">
      <button
        @click="$router.push('/profile/support/new')"
        class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md transition-colors"
      >
        Создать новый запрос
      </button>
    </div>

    <!-- Список запросов -->
    <div class="space-y-4">
      <div
        v-for="ticket in filteredTickets"
        :key="ticket.id"
        class="ticket-item"
      >
        <div
          class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300 cursor-pointer"
          @click="$router.push(`/profile/support/${ticket.id}`)"
        >
          <div class="flex justify-between items-start">
            <div class="w-full">
              <h2 class="text-lg font-semibold text-mywhite-5">{{ ticket.title }}</h2>
              <p class="text-mywhite-2 mt-1 line-clamp-2">{{ ticket.description }}</p>
            </div>
            <div class="flex-shrink-0 ml-4">
              <span :class="statusClass(ticket.status)" class="px-3 py-1 text-xs rounded-full font-medium">
                {{ statusText(ticket.status) }}
              </span>
            </div>
          </div>

          <div class="mt-3 flex justify-between text-sm">
            <span class="text-mywhite-1">ID запроса: TICKET-{{ ticket.id }}</span>
            <span class="text-mywhite-2">Сообщений: {{ ticket.messages_count }}</span>
          </div>
        </div>
      </div>

      <!-- Сообщение, если нет запросов -->
      <div v-if="filteredTickets.length === 0 && !loading" class="text-center text-mywhite-2 py-6">
        У вас пока нет активных запросов
      </div>

      <!-- Индикатор загрузки -->
      <div v-if="loading" class="text-center text-mywhite-2 py-6">Загрузка...</div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'
import { useTicketStore } from '@/stores/useTicketStore'

const ticketStore = useTicketStore()
const { filteredTickets, loading, selectedStatus, searchQuery } = storeToRefs(ticketStore)

onMounted(async () => {
  await ticketStore.fetchTickets()
})
</script>

<script>
export default {
  methods: {
    statusText(status) {
      switch (status) {
        case 'open': return 'Ожидает ответа'
        case 'in_progress': return 'В работе'
        case 'closed': return 'Закрыт'
        default: return 'Неизвестный'
      }
    },
    statusClass(status) {
      switch (status) {
        case 'open':
          return 'bg-green-900/30 text-green-400'
        case 'in_progress':
          return 'bg-blue-900/30 text-blue-400'
        case 'closed':
          return 'bg-gray-700 text-gray-300'
        default:
          return 'bg-red-900/30 text-red-400'
      }
    }
  }
}
</script>