<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 min-h-screen">
    <RouterLink to="/admin/support" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H17a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd" />
    </svg>
    Назад к запросам
    </RouterLink>
    <!-- Заголовок -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-mywhite-5">{{ ticket.title }}</h1>
      <div class="mt-2 flex flex-wrap items-center gap-4 text-sm">
        <span class="font-medium">Автор: {{ ticket.author.name }}</span>
        <span class="text-mywhite-2">UID: {{ ticket.author.uid }}</span>
        <span :class="statusClass()" class="px-3 py-1 rounded-full text-xs font-medium ml-auto">
          {{ statusText() }}
        </span>
        <span class="text-mywhite-1">ID: {{ ticket.id }}</span>
      </div>
      <!-- Барьер между заголовком и чатом -->
      <div class="border-t border-myblack-4 mt-6"></div>
    </div>

    <!-- Чат -->
    <div class="max-w-4xl mx-auto space-y-6">
      <div v-for="(msg, index) in messagesWithFirstMessage" :key="index" class="flex">
        <!-- Сообщение от пользователя -->
        <div v-if="msg.user === 'user'" class="w-full md:w-8/12">
          <div class="bg-myblack-3 border border-myblack-4 rounded-lg p-4 mb-2">
            <p class="text-mywhite-2 whitespace-pre-line">{{ msg.text }}</p>
          </div>
          <div class="text-xs text-mywhite-1 pl-2">{{ formatTime(msg.time) }}</div>
        </div>

        <!-- Сообщение от сотрудника или бота -->
        <div v-else class="w-full md:w-8/12 ml-auto">
          <div class="bg-mypurple-4 text-white rounded-lg p-4 mb-2">
            <p class="whitespace-pre-line">{{ msg.text }}</p>
          </div>
          <div class="text-xs text-mywhite-1 text-right pr-2">{{ formatTime(msg.time) }}</div>
        </div>
      </div>

      <!-- Форма ответа -->
      <form @submit.prevent="sendMessage" class="mt-10 max-w-4xl mx-auto">
        <div class="flex items-center gap-2">
          <textarea
            v-model="newMessage"
            placeholder="Введите ваш ответ..."
            rows="3"
            class="
              flex-1 bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4 transition-colors
              resize-none
            "
            required
          ></textarea>
          <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md">
            Отправить
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()

// Пример данных (позже заменишь на API)
const ticket = ref({
  id: route.params.id || 'TICKET-001',
  title: 'Не могу войти в аккаунт',
  author: {
    name: 'Dimatron',
    uid: '100000002'
  },
  status: 'open',
  description: 'При попытке входа выходит ошибка "Неверный пароль", хотя я уверен, что он правильный.',
  messages: [
    {
      user: 'bot',
      text: 'Добрый день! Пожалуйста, проверьте правильность ввода email и пароля.',
      time: new Date().toISOString()
    },
    {
      user: 'staff',
      text: 'Может быть, вы используете копипаст? Иногда вставляются лишние символы.',
      time: new Date().toISOString()
    }
  ]
})

// Список сообщений + первое сообщение из description
const messagesWithFirstMessage = computed(() => {
  const firstMessage = {
    user: 'user',
    text: ticket.value.description,
    time: new Date().toISOString()
  }

  return [firstMessage, ...ticket.value.messages]
})

// Вспомогательные функции
function statusText() {
  switch (ticket.value.status) {
    case 'open': return 'Открыт'
    case 'in_progress': return 'В работе'
    case 'closed': return 'Закрыт'
    default: return 'Неизвестный'
  }
}

function statusClass() {
  switch (ticket.value.status) {
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

function formatTime(time) {
  const date = new Date(time)
  return date.toLocaleString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Отправка нового сообщения
const newMessage = ref('')
function sendMessage() {
  if (!newMessage.value.trim()) return

  messagesWithFirstMessage.value.push({
    user: 'staff',
    text: newMessage.value.trim(),
    time: new Date().toISOString()
  })

  newMessage.value = ''
}
</script>