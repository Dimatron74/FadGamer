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
        <option value="closed">Завершённые</option>
      </select>

      <select v-model="selectedGame" class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none">
        <option value="">Все игры</option>
        <option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
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
    <div v-if="loading" class="text-center text-mywhite-2 py-6">Загрузка...</div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="code in filteredPromoCodes" :key="code.id" class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 cursor-pointer transition duration-300" @click="openModal(code)">
        <h2 class="text-xl font-semibold text-mywhite-5">{{ code.code }}</h2>
        <p class="mt-2 text-mywhite-2">Статус: {{ statusText(code.status) }}</p>
        <p class="mt-1 text-mywhite-2">Игра: {{ gameText(code.service.id) }}</p>
        <p class="mt-1 text-mywhite-1 text-sm">Создан: {{ formatDate(code.created_at) }}</p>
        <p v-if="code.expires_at" class="mt-1 text-mywhite-1 text-sm">Истекает: {{ formatDate(code.expires_at) }}</p>
      </div>
    </div>

    <!-- Пустой результат -->
    <div v-if="!loading && filteredPromoCodes.length === 0" class="text-center text-mywhite-2 py-6">
      Промокоды не найдены
    </div>

    <!-- Модальное окно -->
    <PromoCodeModal v-if="selectedPromoCode" :promo-code="selectedPromoCode" @close="selectedPromoCode = null" @update="loadPromoCodes"/>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import PromoCodeModal from '@/components/admin/PromoCodeModal.vue'
import promoCodeService from '@/services/promoCodeService'

const loading = ref(true)
const promoCodes = ref([])
const services = ref([])

// Фильтрация
const selectedStatus = ref('')
const selectedGame = ref('')
const searchQuery = ref('')

// Подгрузка данных
onMounted(async () => {
  await loadPromoCodes()
})

async function loadPromoCodes() {
  try {
    const response = await promoCodeService.getPromoCodes()
    promoCodes.value = response.data

    // Получаем уникальные сервисы (игры)
    services.value = [...new Map(response.data.map(p => [p.service.id, p.service])).values()]

  } catch (error) {
    console.error('Ошибка при загрузке промокодов:', error)
  } finally {
    loading.value = false
  }
}

// Вспомогательные функции
function statusText(status) {
  switch (status) {
    case 'active': return 'Активный'
    case 'expired': return 'Истёк'
    case 'used': return 'Использованный'
    case 'inactive': return 'Неактивный'
    case 'closed': return 'Завершён'
    default: return 'Неизвестный'
  }
}

function gameText(serviceId) {
  const service = services.value.find(s => s.id === serviceId)
  return service ? service.name : 'Неизвестная игра'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU')
}

// Фильтрация
const filteredPromoCodes = computed(() => {
  console.log('Промо:', filteredPromoCodes)
  return promoCodes.value.filter(code => {
    const matchesStatus = selectedStatus.value ? code.status === selectedStatus.value : true
    const matchesGame = selectedGame.value ? code.service.id == selectedGame.value : true
    const matchesSearch = code.code.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesStatus && matchesGame && matchesSearch
  })
})

// Открытие модального окна
const selectedPromoCode = ref(null)
function openModal(code) {
  selectedPromoCode.value = code
}
</script>