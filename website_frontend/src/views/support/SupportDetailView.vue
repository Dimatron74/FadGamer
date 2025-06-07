<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 min-h-screen">
    <!-- Кнопка "Назад" -->
    <RouterLink to="/profile/support" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd"
          d="M9.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L7.414 9H17a1 1 0 110 2H7.414l2.293 2.293a1 1 0 010 1.414z"
          clip-rule="evenodd" />
      </svg>
      Назад к запросам
    </RouterLink>

    <!-- Индикатор загрузки -->
    <div v-if="loading" class="text-center py-10">Загрузка...</div>
    <div v-else-if="error" class="text-red-500 text-center py-10">{{ error }}</div>
    <div v-else>
      <!-- Заголовок тикета -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-mywhite-5">{{ ticket.title }}</h1>
        <div class="mt-2 flex flex-wrap items-center gap-4 text-sm">
          <span class="font-medium">Сервис: {{ ticket.service_name }}</span>
          <span class="text-mywhite-2">Категория: {{ ticket.category_name }}</span>
          <span :class="statusClass()" class="px-3 py-1 rounded-full text-xs font-medium ml-auto">
            {{ statusText() }}
          </span>
          <span class="text-mywhite-1">ID: {{ ticket.id }}</span>
          <button
            v-if="ticket.status !== 'closed'"
            @click="changeStatus('closed')"
            class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-1 rounded text-sm"
          >
            Отключить ИИ
          </button>
        </div>
        <div class="border-t border-myblack-4 mt-6"></div>
      </div>

      <!-- Чат с отдельной прокруткой -->
      <div class="max-w-4xl mx-auto h-[60vh] overflow-y-auto pr-2 chat-container" ref="chatContainer">
        <div v-for="(msg, index) in messagesWithFirstMessage" :key="index" class="flex flex-col mb-4">
          <!-- Сообщение от пользователя -->
          <div v-if="msg.sender_type === 'user'" class="w-full md:w-8/12 self-end">

            <div class="bg-mypurple-4 text-white rounded-lg p-4 mb-1">
              <p class="whitespace-pre-line">{{ msg.text }}</p>
            </div>
            <div class="text-xs text-mywhite-1 text-right pr-2 mt-1">
              {{ formatTime(msg.created_at) }}
            </div>
          </div>

          <!-- Сообщение от ИИ или сотрудника -->
          <div v-else class="w-full md:w-8/12 self-start">
            <div v-if="msg.sender_type == 'ai'" class="text-left text-xs text-mywhite-1 mb-1 pl-2">
              Искусственный Интеллект Qwen3
            </div>
            <div class="bg-myblack-3 rounded-lg p-4 mb-1">
              <p class="text-mywhite-2 whitespace-pre-line">{{ msg.text }}</p>
            </div>
            <div class="text-xs text-mywhite-1 pl-2 mt-1">
              {{ formatTime(msg.created_at) }}
            </div>
          </div>
        </div>
      </div>

      <!-- Форма отправки сообщения -->
      <form @submit.prevent="sendMessage" class="mt-6 max-w-4xl mx-auto" v-if="ticket.status !== 'closed'">
        <div class="flex items-center gap-2">
          <textarea
            v-model="newMessage"
            placeholder="Введите ваш ответ..."
            rows="3"
            class="
              flex-1 bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4 transition-colors resize-none
            "
            required
          ></textarea>
          <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md">
            Отправить
          </button>
        </div>
      </form>

      <!-- Блок при закрытом тикете -->
      <div v-else class="mt-10 text-center text-mywhite-2">
        Этот тикет закрыт. Вы не можете отправлять новые сообщения.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ticketService from '@/services/ticketService'

const route = useRoute()
const router = useRouter()
const ticketId = route.params.id

// Состояние
const loading = ref(true)
const error = ref(null)
const ticket = ref(null)
const messages = ref([])
const newMessage = ref('')
const chatContainer = ref(null)
let pollingInterval = ref(null)

// ==== Получение данных ====
async function fetchTicketAndMessages() {
  try {
    const [ticketRes, messagesRes] = await Promise.all([
      ticketService.getTicket(ticketId),
      ticketService.getMessages(ticketId)
    ])
    ticket.value = ticketRes.data
    messages.value = messagesRes.data
  } catch (err) {
    console.error(err)
    error.value = 'Не удалось загрузить данные тикета'
  } finally {
    loading.value = false
    await nextTick()
    scrollToBottom()
  }
}

// ==== Обновление статуса тикета ====
async function refreshTicketStatus() {
  try {
    const res = await ticketService.getTicket(ticketId)
    ticket.value.status = res.data.status
  } catch (err) {
    console.error('Ошибка при обновлении статуса:', err)
  }
}

// ==== Монтирование ====
onMounted(async () => {
  await fetchTicketAndMessages()
  await refreshTicketStatus()
  await nextTick()
  scrollToBottom()
  startPolling() // ✅ Запуск опроса при входе на страницу
})

// ==== Вычисляемые свойства ====
const messagesWithFirstMessage = computed(() => {
  if (!ticket.value || !ticket.value.description) return []
  const firstMessage = {
    sender_type: 'user',
    text: ticket.value.description,
    created_at: ticket.value.created_at,
    is_deleted: false
  }
  const validMessages = messages.value.filter(msg => !msg.is_deleted)
  return [firstMessage, ...validMessages]
})

function statusText() {
  switch (ticket.value.status) {
    case 'open': return 'Ожидает ответа'
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

// ==== Отправка сообщения ====
async function sendMessage() {
  if (!newMessage.value.trim()) return
  try {
    const res = await ticketService.sendMessage(ticketId, {
      text: newMessage.value.trim(),
      sender_type: 'user'
    })
    // Добавляем новое сообщение в список
    messages.value.push(res.data)
    newMessage.value = ''
    await nextTick()
    scrollToBottom()
    await refreshTicketStatus()
    // Запускаем опрос сервера на наличие ответа ИИ
    startPolling()
  } catch (err) {
    console.error('Ошибка при отправке сообщения:', err)
    alert('Не удалось отправить сообщение')
  }
}

// ==== Прокрутка вниз ====
function scrollToBottom() {
  const container = chatContainer.value
  if (container) {
    container.scrollTop = container.scrollHeight
  }
}

// ==== Опрос сервера на наличие новых сообщений ====
async function pollForNewMessages() {
  try {
    const res = await ticketService.getMessages(ticketId)
    const latestMessages = res.data.filter(msg => !msg.is_deleted)
    if (latestMessages.length > messages.value.length) {
      messages.value = latestMessages
      await nextTick()
      scrollToBottom()
      await refreshTicketStatus()
    }
  } catch (err) {
    console.error('Ошибка при опросе новых сообщений:', err)
  }
}

function startPolling() {
  stopPolling()
  pollingInterval.value = setInterval(pollForNewMessages, 8000)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

// ==== Автоостановка опроса при выходе из компонента ====
onBeforeUnmount(() => {
  stopPolling()
})
</script>

<style scoped>
.chat-container::-webkit-scrollbar {
  width: 6px;
}
.chat-container::-webkit-scrollbar-track {
  background: #1f1f1f;
}
.chat-container::-webkit-scrollbar-thumb {
  background: #5e5e5e;
  border-radius: 3px;
}
</style>