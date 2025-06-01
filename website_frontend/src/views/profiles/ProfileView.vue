<!-- ProfileView.vue -->

<script setup>
import SupportTicketList from '@/components/support/SupportTicketList.vue'
import PromoCodeActivation from '@/components/profiles/PromoCodeActivation.vue'
import AccountSettings from '@/components/profiles/AccountSettings.vue'
import AvatarEdit from '@/components/profiles/AvatarEdit.vue'
import { ref, computed, watchEffect } from 'vue'
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

// Используем ticketStore
const ticketStore = useTicketStore()

// Подключаем реактивные данные в setup
const { filteredTickets, loading } = storeToRefs(ticketStore)

// Флаг, показывает, загружали ли мы тикеты хотя бы раз
const hasLoadedSupportData = ref(false)

// Автоматически загружаем тикеты при первом переходе на вкладку "support"
watchEffect(() => {
  if (activeTab.value === 'support') {
    hasLoadedSupportData.value = true
    ticketStore.fetchTickets()
    console.log(ticketStore)
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

// Фильтруем вкладки: показываем "админ" только для staff
const tabs = computed(() => {
  return allTabs.filter(tab => {
    if (tab.id === 'admin') {
      return props.userStore.user.is_staff === true
    }
    return true
  })
})

function scrollToTop() {
  window.scrollTo(0,0);
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
          <AvatarEdit />
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
          <AccountSettings />
        </div>

        <!-- Игры -->
        <div v-if="activeTab === 'games'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Все игры</h2>
          <p class="text-mywhite-3">Информация о ваших играх пока недоступна.</p>
        </div>

        <!-- Промокод -->
        <div v-if="activeTab === 'promo'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Активировать промокод</h2>
          <PromoCodeActivation />
        </div>

        <!-- Техподдержка -->
        <div v-if="activeTab === 'support'" class="bg-myblack-3 rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Запросы в техподдержку</h2>

          <!-- Список тикетов -->
          <SupportTicketList
            :filtered-tickets="filteredTickets"
            :loading="loading"
          />

          <!-- Кнопка "Посмотреть все" -->
          <div class="mt-6 text-right">
            <RouterLink to="/profile/support" class="text-mypurple-4 hover:text-mypurple-3 font-medium" @click="scrollToTop">
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