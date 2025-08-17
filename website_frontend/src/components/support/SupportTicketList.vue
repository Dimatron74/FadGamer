<template>
  <div class="space-y-4">
    <RouterLink
      v-for="ticket in limitedTickets"
      :key="ticket.id"
      :to="`/profile/support/${ticket.id}`"
      class="
        bg-myblack-2 rounded-lg p-4 border border-myblack-4 hover:border-mypurple-4
        transition-all cursor-pointer block
      "
    >
      <div class="flex justify-between items-start">
        <div>
          <h3 class="font-medium text-mywhite-5">{{ ticket.title }}</h3>
          <p class="text-mywhite-2 text-sm line-clamp-1 mt-1">{{ ticket.description }}</p>
        </div>
        <div class="flex-shrink-0 ml-4">
          <span :class="statusClass(ticket.status)" class="px-3 py-1 text-xs rounded-full font-medium">
            {{ statusText(ticket.status) }}
          </span>
        </div>
      </div>

      <div class="mt-2 flex justify-between text-xs text-mywhite-1">
        <span>TICKET-{{ ticket.id }}</span>
        <span>Сообщений: {{ ticket.messages_count }}</span>
      </div>
    </RouterLink>

    <!-- Сообщение, если нет запросов -->
    <div v-if="filteredTickets.length === 0 && !loading" class="text-center text-mywhite-2 py-4">
      У вас пока нет активных запросов
    </div>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="text-center text-mywhite-2 py-4">Загрузка...</div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  filteredTickets: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()

// Ограничиваем вывод до 5 элементов
const limitedTickets = computed(() => {
  return props.filteredTickets.slice(0, 5)
})

function statusText(status) {
  switch (status) {
    case 'open': return 'Открыт'
    case 'in_progress': return 'В работе'
    case 'closed': return 'Закрыт'
    default: return 'Неизвестный'
  }
}

function statusClass(status) {
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
</script>