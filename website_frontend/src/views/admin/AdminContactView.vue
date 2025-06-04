<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6">
    <!-- Заголовок -->
    <h1 class="text-3xl font-bold text-mywhite-5 mb-8">Обращения пользователей</h1>

    <!-- Поиск и фильтры -->
    <div class="flex flex-wrap gap-4 mb-6">
      <select v-model="selectedStatus" class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none">
        <option value="">Все обращения</option>
        <option value="open">Не отвеченные</option>
        <option value="closed">Отвеченные</option>
      </select>
      <input
        type="text"
        placeholder="Поиск по теме или имени..."
        v-model="searchQuery"
        class="bg-myblack-3 border border-myblack-4 rounded-md px-4 py-2 text-mywhite-3 focus:outline-none w-full md:w-auto flex-1"
      />
    </div>

    <!-- Список обращений -->
    <div class="space-y-4">
      <div
        v-for="request in filteredRequests"
        :key="request.id"
        class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300 cursor-pointer"
        @click="$router.push(`/admin/contacts/${request.id}`)"
      >
        <div class="flex justify-between items-start">
          <div class="w-full">
            <h2 class="text-lg font-semibold text-mywhite-5">{{ request.subject }}</h2>
            <p class="text-mywhite-2 mt-1 line-clamp-2">{{ request.message }}</p>
            <div class="mt-2 flex items-center space-x-4 text-sm text-mywhite-2">
              <span>Автор: {{ request.name || 'Не указан' }} </span>
              <span>Email: {{ request.email?.email || request.guest_email || '-' }} </span>
              <span>Дата: {{ formatDate(request.created_at) }} </span>
            </div>
          </div>
          <div class="flex-shrink-0 ml-4">
            <span :class="statusClass(request.is_resolved)" class="px-3 py-1 text-xs rounded-full font-medium">
              {{ statusText(request.is_resolved) }}
            </span>
          </div>
        </div>
      </div>

      <!-- Сообщение, если нет обращений -->
      <div v-if="filteredRequests.length === 0 && !loading" class="text-center text-mywhite-2 py-6">
        Нет обращений
      </div>

      <!-- Индикатор загрузки -->
      <div v-if="loading" class="text-center text-mywhite-2 py-6">Загрузка...</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminService from '@/services/AdminService'

const router = useRouter()

// Данные
const contactRequests = ref([])
const loading = ref(false)
const selectedStatus = ref('')
const searchQuery = ref('')

// Фильтрация
const filteredRequests = computed(() => {
  return contactRequests.value.filter(request => {
    const matchesStatus = selectedStatus.value === '' ||
      (selectedStatus.value === 'open' && !request.is_resolved) ||
      (selectedStatus.value === 'closed' && request.is_resolved)

    const matchesSearch = searchQuery.value === '' ||
      request.subject.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (request.name && request.name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (request.user && request.user.nickname.toLowerCase().includes(searchQuery.value.toLowerCase()))

    return matchesStatus && matchesSearch
  })
})
console.log(filteredRequests)
// Статусы
function statusText(isResolved) {
  return isResolved ? 'Отвечено' : 'Не отвечено'
}

function statusClass(isResolved) {
  return isResolved
    ? 'bg-green-900/30 text-green-400'
    : 'bg-yellow-900/30 text-yellow-400'
}

// Формат даты
function formatDate(dateString) {
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// Загрузка данных
onMounted(async () => {
  loading.value = true
  try {
    const res = await AdminService.getContactRequests()
    contactRequests.value = res.data
  } catch (err) {
    console.error('Ошибка при загрузке обращений:', err)
  } finally {
    loading.value = false
  }
})
</script>