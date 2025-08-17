<!-- ProfileView.vue -->

<script setup>
import SupportTicketList from '@/components/support/SupportTicketList.vue'
import PromoCodeActivation from '@/components/profiles/PromoCodeActivation.vue'
import AccountSettings from '@/components/profiles/AccountSettings.vue'
import AvatarEdit from '@/components/profiles/AvatarEdit.vue'
import UserProductsList from '@/components/profiles/UserProductsList.vue'
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
  <div class="min-h-screen bg-myblack-1">
    <!-- Шапка профиля -->
    <header class="bg-myblack-3 border-b border-myblack-2/70">
      <div class="container mx-auto max-w-6xl px-6 py-8">
        <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <!-- Левая часть: аватар + имя -->
          <div class="flex items-center gap-5">
            <!-- Важно: задаём размеры через class, чтобы AvatarEdit подстроился и не «ломал» круг -->
            <AvatarEdit class="w-24 h-24 sm:w-28 sm:h-28 rounded-full overflow-hidden ring-2 ring-mypurple-4 shadow-md shrink-0" />
            <div class="min-w-0">
              <h1 class="text-2xl sm:text-3xl font-extrabold text-mywhite-5 break-words">
                {{ userStore.user.name }}
              </h1>
              <p class="text-sm text-mywhite-2 mt-1">
                UID: <span class="font-mono">{{ userStore.user.uid }}</span>
              </p>
            </div>
          </div>

          <!-- Правая часть: действия -->
          <div class="flex items-center gap-3">
            <button
              @click="removeToken"
              class="inline-flex items-center justify-center px-5 py-2 rounded-lg bg-myred-2 hover:bg-myred-1 text-white font-semibold shadow transition
                     focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-0 focus-visible:ring-mypurple-4"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Табы (липкие, скроллятся по X на мобилке) -->
    <nav
      class="sticky top-0 z-30 bg-myblack-2/95 backdrop-blur border-b border-myblack-2"
      role="tablist"
      aria-label="Навигация по разделам профиля"
    >
      <div class="container mx-auto max-w-6xl px-6">
        <div class="flex gap-1 overflow-x-auto whitespace-nowrap py-2">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :aria-selected="activeTab === tab.id"
            role="tab"
            class="relative px-4 py-2 rounded-lg text-sm font-medium transition
                   focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-mypurple-4"
            :class="activeTab === tab.id
              ? 'text-mywhite-5 bg-myblack-3 shadow-inner'
              : 'text-mywhite-3 hover:text-mywhite-5 hover:bg-myblack-3/60'"
          >
            {{ tab.label }}
            <!-- Индикатор активного таба -->
            <span
              v-if="activeTab === tab.id"
              class="absolute inset-x-2 -bottom-[6px] h-[2px] rounded bg-mypurple-4"
              aria-hidden="true"
            />
          </button>
        </div>
      </div>
    </nav>

    <!-- Контент -->
    <main class="container mx-auto max-w-6xl px-6 py-8 space-y-8">
      <!-- Учётная запись -->
      <section
        v-if="activeTab === 'account'"
        role="tabpanel"
        class="bg-myblack-3 rounded-2xl shadow-lg p-6 border border-myblack-2"
      >
        <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Учётная запись</h2>
        <AccountSettings />
      </section>

      <!-- Игры -->
      <section
        v-if="activeTab === 'games'"
        role="tabpanel"
        class="bg-myblack-3 rounded-2xl shadow-lg p-6 border border-myblack-2"
      >
        <h2 class="text-xl font-semibold text-mywhite-5">Ваши игры</h2>
        <UserProductsList />
      </section>

      <!-- Промокод -->
      <section
        v-if="activeTab === 'promo'"
        role="tabpanel"
        class="bg-myblack-3 rounded-2xl shadow-lg p-6 border border-myblack-2"
      >
        <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Активация промокода</h2>
        <PromoCodeActivation />
      </section>

      <!-- Техподдержка -->
      <section
        v-if="activeTab === 'support'"
        role="tabpanel"
        class="bg-myblack-3 rounded-2xl shadow-lg p-6 border border-myblack-2"
      >
        <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Запросы в техподдержку</h2>
        <SupportTicketList
          :filtered-tickets="filteredTickets"
          :loading="loading"
        />
        <div class="mt-6 text-right">
          <RouterLink
            to="/profile/support"
            class="text-mypurple-5 hover:text-mypurple-3 font-medium underline decoration-mypurple-5/40 underline-offset-4"
            @click="scrollToTop"
          >
            Посмотреть все →
          </RouterLink>
        </div>
      </section>

      <!-- Админ панель -->
      <section
        v-if="activeTab === 'admin' && userStore.user.is_staff"
        role="tabpanel"
        class="bg-myblack-3 rounded-2xl shadow-lg p-6 border border-myblack-2"
      >
        <h2 class="text-xl font-semibold text-mywhite-5 mb-4">Админ панель</h2>
        <RouterLink
          to="/admin"
          class="inline-flex items-center gap-2 text-mypurple-5 hover:text-mypurple-3 font-medium"
        >
          Перейти в админку →
        </RouterLink>
      </section>
    </main>
  </div>
</template>


