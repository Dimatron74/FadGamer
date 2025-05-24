<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 min-h-screen">

    <!-- Заголовок -->
    <h1 class="text-3xl font-bold text-mywhite-5 mb-8">Промокоды</h1>

    <!-- Фильтры -->
    <div class="flex flex-wrap gap-4 mb-6 items-end">
    <select v-model="selectedStatus" class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none">
        <option value="">Все статусы</option>
        <option value="active">Активные</option>
        <option value="expired">Истекшие</option>
        <option value="used">Использованные</option>
        <option value="inactive">Неактивные</option>
    </select>

    <select v-model="selectedGame" class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none">
        <option value="">Все игры</option>
        <option value="game1">Игра 1</option>
        <option value="game2">Игра 2</option>
    </select>

    <input
        type="text"
        placeholder="Поиск по названию..."
        v-model="searchQuery"
        class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none w-full md:w-auto flex-1"
    />

    <!-- Кнопка создания -->
    <div class="ml-auto">
        <RouterLink to="/admin/promocodes/create" class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md inline-flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 010 2h-3v3a1 1 0 01-2 0v-3H5a1 1 0 010-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Создать промокод
        </RouterLink>
    </div>
    </div>

    <!-- Карточки -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="code in filteredPromoCodes" :key="code.code" class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 cursor-pointer transition duration-300" @click="openModal(code)">
        <h2 class="text-xl font-semibold text-mywhite-5">{{ code.code }}</h2>
        <p class="mt-2 text-mywhite-2">Статус: {{ statusText(code.status) }}</p>
        <p class="mt-1 text-mywhite-2">Игра: {{ gameText(code.game) }}</p>
        <p class="mt-1 text-mywhite-1 text-sm">Создан: {{ formatDate(code.created_at) }}</p>
        <p v-if="code.expires_at" class="mt-1 text-mywhite-1 text-sm">Истекает: {{ formatDate(code.expires_at) }}</p>
      </div>
    </div>

    <!-- Пустой результат -->
    <div v-if="filteredPromoCodes.length === 0" class="text-center text-mywhite-2 py-6">
      Промокоды не найдены
    </div>

    <!-- Модальное окно -->
    <PromoCodeModal v-if="selectedPromoCode" :promo-code="selectedPromoCode" @close="selectedPromoCode = null"/>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter, RouterView, RouterLink } from 'vue-router'
import { watch, ref, computed } from 'vue'
import PromoCodeModal from '@/components/admin/PromoCodeModal.vue'

const promoCodes = ref([
  {
    code: 'SUMMER2025',
    status: 'active',
    game: 'game1',
    created_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + 10 * 24 * 60 * 60 * 1000).toISOString(), // через 10 дней
    author: { name: 'Dimatron', uid: '100000002' },
    bonuses: [
      { type: 'coins', amount: 50 },
      { type: 'skin', amount: 1 }
    ],
    conditions: [
      { type: 'coins', value: 100 },
      { type: 'level', value: 10 }
    ]
  },
  {
    code: 'WINTER2025',
    status: 'expired',
    game: 'game2',
    created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // месяц назад
    expires_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 дней назад
    author: { name: 'Bot', uid: 'system' },
    bonuses: [
      { type: 'premium', amount: null }, // премиум аккаунт (без количества)
      { type: 'access', amount: null }  // доступ к мероприятию
    ],
    conditions: [
      { type: 'event', value: null },   // событие не требует значения
      { type: 'item', value: null }     // наличие предмета
    ]
  }
])

// Фильтрация
const selectedStatus = ref('')
const selectedGame = ref('')
const searchQuery = ref('')

const filteredPromoCodes = computed(() => {
  return promoCodes.value.filter(code => {
    const matchesStatus = selectedStatus.value ? code.status === selectedStatus.value : true
    const matchesGame = selectedGame.value ? code.game === selectedGame.value : true
    const matchesSearch = code.code.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesStatus && matchesGame && matchesSearch
  })
})

// Вспомогательные функции
function statusText(status) {
  switch (status) {
    case 'active': return 'Активный'
    case 'expired': return 'Истёк'
    case 'used': return 'Использован'
    default: return 'Неизвестный'
  }
}

function gameText(game) {
  return game === 'game1' ? 'Игра 1' : game === 'game2' ? 'Игра 2' : 'Любая игра'
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU')
}

// Открытие модального окна
const selectedPromoCode = ref(null)
function openModal(code) {
  selectedPromoCode.value = code
}
</script>