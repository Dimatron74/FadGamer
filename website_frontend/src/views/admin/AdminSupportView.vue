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

    <!-- Список запросов -->
    <div class="space-y-4">
      <div
        v-for="(ticket, index) in filteredTickets"
        :key="ticket.id"
        class="ticket-item"
      >
        <div
          class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300 cursor-pointer"
          @click="$router.push(`/admin/support/${ticket.id}`)"
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
            <span class="text-mywhite-1">ID: {{ ticket.id }}</span>
            <span class="text-mywhite-2">Сообщений: {{ ticket.messages.length }}</span>
          </div>
        </div>
      </div>

      <!-- Сообщение, если нет запросов -->
      <div v-if="filteredTickets.length === 0" class="text-center text-mywhite-2 py-6">
        Нет активных запросов
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Пример данных
const tickets = ref([
  {
    id: 'TICKET-001',
    title: 'Не могу войти в аккаунт',
    description: 'При попытке входа выходит ошибка "Неверный пароль", хотя я уверен, что он правильный.',
    status: 'open',
    messages: [
      { user: 'user', text: 'Привет, не могу войти в аккаунт...' },
      { user: 'bot', text: 'Добрый день! Пожалуйста, проверьте правильность ввода email и пароля.' }
    ]
  },
  {
    id: 'TICKET-002',
    title: 'Ошибка при активации промокода',
    description: 'При попытке активировать промокод система говорит, что он недействителен. Но я уверен, что код верный.',
    status: 'in_progress',
    messages: [
      { user: 'user', text: 'Промокод не работает!' },
      { user: 'bot', text: 'Мы уже смотрим ваш запрос...' }
    ]
  },
  {
    id: 'TICKET-003',
    title: 'Проблема с оплатой',
    description: 'Оплата прошла успешно, но игра не активировалась. Прошло уже больше часа.',
    status: 'closed',
    messages: [
      { user: 'user', text: 'Платформа не активировала игру после покупки' },
      { user: 'bot', text: 'Игра была активирована вручную. Приносим свои извинения за задержку.' }
    ]
  }
])

// Фильтрация
const selectedStatus = ref('')
const searchQuery = ref('')

const filteredTickets = computed(() => {
  return tickets.value.filter(ticket => {
    const matchesStatus = selectedStatus.value ? ticket.status === selectedStatus.value : true
    const matchesSearch = searchQuery.value
      ? ticket.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        ticket.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      : true
    return matchesStatus && matchesSearch
  })
})

// Вспомогательные функции
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