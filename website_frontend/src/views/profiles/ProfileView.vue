<script setup>
import { ref, computed, watchEffect } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useTicketStore } from '@/stores/useTicketStore'

const router = useRouter()

// Пользователь из стора
const props = defineProps({
  userStore: {
    type: Object,
    required: true
  }
})

// Активная вкладка
const activeTab = ref('account')

// Выход из аккаунта
const removeToken = () => {
  props.userStore.removeToken()
  router.push('/')
}

const ticketStore = useTicketStore()
const { filteredTickets, loading } = storeToRefs(ticketStore)

// Автоматически загружаем тикеты при переключении на вкладку "support"
watchEffect(() => {
  if (activeTab.value === 'support') {
    if (!ticketStore.tickets.length) {
      ticketStore.fetchTickets()
    }
  }
})

// Все вкладки
const allTabs = [
  { id: 'account', label: 'Учётная запись' },
  { id: 'games', label: 'Все игры' },
  { id: 'promo', label: 'Активировать промокод' },
  { id: 'support', label: 'Запросы в техподдержку' },
  { id: 'admin', label: 'Админ панель' }
]

// Фильтруем вкладки: показываем "админ" только для is_staff
const tabs = computed(() => {
  return allTabs.filter(tab => {
    if (tab.id === 'admin') {
      return props.userStore.user.is_staff === true
    }
    return true
  })
})

</script>

<script>
export default {
  methods: {
    statusText(status) {
      switch (status) {
        case 'open': return 'Открыт'
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

<template>
  <div class="container mx-auto p-4 max-w-6xl">
    <h1 class="text-3xl font-bold mb-6 text-white relative z-10">Профиль</h1>

    <!-- Основной Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Карточка профиля (фиксированная) -->
      <div
        class="
          lg:col-span-1
          bg-myblack-3 rounded-lg shadow-xl p-5 top-24 self-start
          border border-myblack-2
        "
      >
        <!-- Фото профиля -->
        <div class="flex justify-center mb-4">
          <div class="w-20 h-20 rounded-full overflow-hidden bg-myblack-5 flex items-center justify-center">
            <span class="text-mywhite-1 text-2xl font-semibold"> {{ userStore.user.name?.charAt(0) || '?' }} </span>
          </div>
        </div>

        <!-- Никнейм и UID -->
        <div class="text-center mb-6">
          <h2 class="text-xl font-bold text-mywhite-5">{{ userStore.user.name }}</h2>
          <p class="text-sm text-mywhite-2 truncate">UID: {{ userStore.user.uid }}</p>
        </div>

        <!-- Меню навигации по профилю -->
        <ul class="space-y-2">
          <li v-for="tab in tabs" :key="tab.id">
            <button
              @click="activeTab = tab.id"
              :class="[
                'w-full text-left px-4 py-2 rounded-md transition-all',
                activeTab === tab.id
                  ? 'bg-mypurple-4 text-mywhite-5 font-medium'
                  : 'hover:bg-myblack-2 text-mywhite-3'
              ]"
            >
              {{ tab.label }}
            </button>
          </li>
        </ul>

        <!-- Выход -->
        <div class="mt-6 pt-4 border-t border-myblack-1">
          <button
            @click="removeToken"
            class="w-full bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded"
          >
            Выйти
          </button>
        </div>
      </div>

      <!-- Контентная часть -->
      <div class="lg:col-span-3 space-y-6">
        <!-- Учётная запись -->
        <div v-if="activeTab === 'account'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Учётная запись</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-mywhite-2 text-sm mb-1">Email</label>
              <div class="flex items-center justify-between">
                <p class="text-mywhite-4">{{ userStore.user.email }}</p>
                <button class="text-mypurple-5 hover:text-mypurple-2 text-sm underline">Изменить</button>
              </div>
            </div>
            <hr class="border-myblack-2" />
            <div>
              <label class="block text-mywhite-2 text-sm mb-1">Пароль</label>
              <div class="flex items-center justify-between">
                <p class="text-mywhite-4">•••••••••••</p>
                <button class="text-mypurple-4 hover:text-mypurple-2 text-sm">Изменить</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Игры -->
        <div v-if="activeTab === 'games'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Все игры</h2>
          <p class="text-mywhite-3">Информация о ваших играх пока недоступна.</p>
        </div>

        <!-- Промокод -->
        <div v-if="activeTab === 'promo'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Активировать промокод</h2>
          <form class="space-y-4">
            <input
              type="text"
              placeholder="Введите промокод"
              class="w-full bg-myblack-2 text-mywhite-4 placeholder-mywhite-2 border-none rounded-md px-4 py-2 focus:ring-2 focus:ring-mypurple-4"
            />
            <button
              type="submit"
              class="w-full bg-mypurple-4 hover:bg-mypurple-3 text-white font-bold py-2 px-4 rounded"
            >
              Активировать
            </button>
          </form>
        </div>

        <!-- Техподдержка -->
        <div v-if="activeTab === 'support'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Запросы в техподдержку</h2>

          <!-- Список тикетов -->
          <div class="space-y-4">
            <div
              v-for="ticket in filteredTickets"
              :key="ticket.id"
              class="bg-myblack-2 rounded-lg p-4 border border-myblack-4 hover:border-mypurple-4 transition-all cursor-pointer"
              @click="$router.push(`/profile/support/${ticket.id}`)"
            >
              <div class="flex justify-between items-start">
                <div>
                  <h3 class="font-medium text-mywhite-5">{{ ticket.title }}</h3>
                  <p class="text-mywhite-2 text-sm line-clamp-1 mt-1">{{ ticket.description }}</p>
                </div>
                <span :class="statusClass(ticket.status)" class="px-2 py-1 text-xs rounded-full font-medium">
                  {{ statusText(ticket.status) }}
                </span>
              </div>

              <div class="mt-2 flex justify-between text-xs text-mywhite-1">
                <span>TICKET-{{ ticket.id }}</span>
                <span>Сообщений: {{ ticket.messages_count }}</span>
              </div>
            </div>

            <!-- Сообщение, если нет запросов -->
            <div v-if="filteredTickets.length === 0 && !loading" class="text-center text-mywhite-2 py-4">
              У вас пока нет активных запросов
            </div>

            <!-- Индикатор загрузки -->
            <div v-if="loading" class="text-center text-mywhite-2 py-4">Загрузка...</div>
          </div>

          <!-- Кнопка "Посмотреть все" -->
          <div class="mt-6 text-right">
            <RouterLink to="/profile/support" class="text-mypurple-4 hover:text-mypurple-3 font-medium">
              Посмотреть все запросы →
            </RouterLink>
          </div>
        </div>

        <!-- Админ панель -->
        <div v-if="activeTab === 'admin' && userStore.user.is_staff" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Админ панель</h2>
          <RouterLink to="/admin" class="hover:text-mywhite-5">Войти</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>