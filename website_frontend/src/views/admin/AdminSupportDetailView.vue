<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 min-h-screen">
    <RouterLink to="/admin/support" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
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
      <!-- Заголовок -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-mywhite-5">{{ ticket.title }}</h1>
        <div class="mt-2 flex flex-wrap items-center gap-4 text-sm">
          <span class="font-medium">Автор: {{ ticket.user?.nickname || '—' }}</span>
          <span class="text-mywhite-2">UID: {{ ticket.user?.uid || '—' }}</span>
        </div>

        <div class="mt-2 flex flex-wrap items-center gap-4 text-sm">
          <span class="font-medium">Сервис: {{ ticket.service_name }}</span>
          <span class="text-mywhite-2">Категория: {{ ticket.category_name }}</span>
          
          <!-- Статус -->
          <span :class="statusClass()" class="px-3 py-1 rounded-full text-xs font-medium ml-auto">
            {{ statusText() }}
          </span>
          <span class="text-mywhite-1">ID: {{ ticket.id }}</span>

          <!-- Кнопка только для закрытия -->
          <button
            v-if="ticket.status !== 'closed'"
            @click="changeStatus('closed')"
            class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-1 rounded text-sm"
          >
            Закрыть запрос
          </button>
        </div>

        <div class="border-t border-myblack-4 mt-6"></div>
      </div>

      <!-- Чат -->
      <div class="max-w-4xl mx-auto space-y-6">
        <div v-for="(msg, index) in messagesWithFirstMessage" :key="index" class="flex flex-col">
          <!-- Первое сообщение (описание тикета) -->
          <div v-if="index === 0" class="w-full md:w-8/12 self-start">
            <div class="relative bg-myblack-3 rounded-lg p-4 mb-1">
              <div class="absolute left-0 top-0 bottom-0 w-1 bg-myred-4"></div>
              <p class="text-mywhite-2 whitespace-pre-line pl-4">{{ msg.text }}</p>
            </div>
            <div class="text-xs text-mywhite-1 pl-6 mt-1">{{ formatTime(msg.created_at) }}</div>
          </div>

          <!-- Сообщение от пользователя -->
          <div v-else-if="msg.sender_type === 'user'" class="w-full md:w-8/12 self-start">
            <div class="bg-myblack-3 rounded-lg p-4 mb-1">
              <p class="text-mywhite-2 whitespace-pre-line">{{ msg.text }}</p>
            </div>
            <div class="text-xs text-mywhite-1 pl-4 mt-1">{{ formatTime(msg.created_at) }}</div>
          </div>

          <!-- Сообщение от сотрудника или бота -->
          <div v-else class="w-full md:w-8/12 self-end">
            <!-- Автор -->
            <div v-if="msg.author" class="text-right text-xs text-mywhite-1 pr-2 mb-1">
              {{ msg.author.nickname }}
            </div>
            <div v-if="msg.sender_type == 'ai'" class="text-right text-xs text-mywhite-1 pr-2 mb-1">
              Искусственный Интеллект Qwen3
            </div>

            <!-- Тело сообщения -->
            <div
              class="bg-mypurple-4 text-white rounded-lg p-4 mb-1"
              :class="{ 'opacity-50 line-through': msg.is_deleted }"
            >
              <p class="whitespace-pre-line">{{ msg.text }}</p>
            </div>

            <!-- Время и действия -->
            <div class="text-xs text-mywhite-1 text-right pr-2 mt-1">
              <span>{{ formatTime(msg.created_at) }}</span>
              <span v-if="msg.is_deleted" class="ml-4 italic">[удалено]</span>
              <button
                v-else
                @click="deleteMessage(msg.id)"
                class="ml-4 text-red-400 hover:text-red-300 transition-colors"
              >
                Удалить
              </button>
            </div>
          </div>
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
              flex-1 bg-myblack-3 border border-myblack-4 rounded-md p-3 text-mywhite-3 focus:outline-none focus:border-mypurple-4 transition-colors resize-none
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ticketService from '@/services/ticketService'

const route = useRoute()
const ticketId = route.params.id

// Состояние
const loading = ref(true)
const error = ref(null)
const ticket = ref(null)
const messages = ref([])
const newMessage = ref('')

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
  }
}

onMounted(fetchTicketAndMessages)

// ==== Вычисляемые свойства ====
const messagesWithFirstMessage = computed(() => {
  if (!ticket.value || !ticket.value.description) return []

  const firstMessage = {
    sender_type: 'user',
    text: ticket.value.description,
    created_at: ticket.value.created_at,
    is_deleted: false
  }

  return [firstMessage, ...(messages.value || [])]
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
      sender_type: 'staff'
    })

    // Добавляем новое сообщение в список
    messages.value.push(res.data)
    newMessage.value = ''
    await autoUpdateStatus()
  } catch (err) {
    console.error('Ошибка при отправке сообщения:', err)
    alert('Не удалось отправить сообщение')
  }
}

// ==== Изменение статуса ====
async function changeStatus(newStatus) {
  try {
    const res = await ticketService.updateTicketStatus(ticketId, newStatus)
    ticket.value.status = res.data.status
  } catch (err) {
    console.error(err)
  }
}

// ==== Удаление сообщения ====
async function deleteMessage(messageId) {
  try {
    await ticketService.deleteMessage(ticketId, messageId)
    messages.value = messages.value.map(msg =>
      msg.id === messageId ? { ...msg, is_deleted: true } : msg
    )
    await autoUpdateStatus()
  } catch (err) {
    alert('Ошибка при удалении сообщения')
    console.error(err)
  }
}

const lastSenderType = computed(() => {
  if (messages.value.length === 0) return null
  return messages.value[messages.value.length - 1]?.sender_type
})

onMounted(async () => {
  await fetchTicketAndMessages()
  autoUpdateStatus()
})

function autoUpdateStatus() {
  // Получаем список всех сообщений без описания
  const validMessages = messages.value.filter(msg => !msg.is_deleted)

  // Последнее непрочитанное сообщение
  const lastValidMessage = [...validMessages].pop()

  if (!lastValidMessage && ticket.value.status !== 'closed') {
    changeStatus('open')
    return
  }

  const senderType = lastValidMessage?.sender_type

  if (senderType === 'user' && ticket.value.status !== 'closed') {
    changeStatus('open')
  } else if (['staff', 'ai'].includes(senderType) && ticket.value.status !== 'closed') {
    changeStatus('in_progress')
  }
}
</script>