<template>
  <div class="bg-myblack-2 text-mywhite-3 p-6 min-h-screen">
    <!-- Назад -->
    <RouterLink to="/admin/promocodes" class="inline-flex items-center text-mywhite-3 hover:text-mypurple-5 mb-6 transition">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
      </svg>
      Назад к списку
    </RouterLink>

    <!-- Форма -->
    <div class="max-w-3xl mx-auto bg-myblack-3 p-6 rounded-lg shadow-md border border-myblack-4">
      <h2 class="text-2xl font-bold text-mywhite-5 mb-6">{{ isNewPromo ? 'Создание промокода' : 'Редактирование промокода' }}</h2>
      <form @submit.prevent="submitForm" class="space-y-6">

        <!-- Название промокода -->
        <div>
          <label class="block text-mywhite-2 mb-2">Название промокода</label>
          <input v-model="form.code" type="text"
                 class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
                 :disabled="!isNewPromo">
        </div>

        <!-- Статус -->
        <div>
          <label class="block text-mywhite-2 mb-2">Статус</label>
          <select v-model="form.status" @change="onStatusChange"
                  class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
            <option value="active">Активный</option>
            <option value="inactive">Неактивный</option>
          </select>
        </div>

        <!-- Сервис -->
        <div>
          <label class="block text-mywhite-2 mb-2">Сервис</label>
          <select v-model="form.service_id" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
                  :disabled="!isNewPromo">
            <option v-for="service in services" :key="service.id" :value="service.id">{{ service.name }}</option>
          </select>
        </div>

        <!-- Количество активаций -->
        <div>
          <label class="block text-mywhite-2 mb-2">Максимальное количество активаций (необязательно)</label>
          <input v-model.number="form.max_activations" type="number" min="1"
                 class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
                 :disabled="!isNewPromo">
        </div>

        <!-- Даты -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-mywhite-2 mb-2">Дата активации</label>
            <input 
              v-model="form.created_at"
              type="datetime-local"
              :class="[
                'w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2',
                form.status === 'inactive' ? 'cursor-text editable' : 'opacity-70'
              ]"
              :readonly="form.status === 'active'"
            />
          </div>
          <div>
            <label class="block text-mywhite-2 mb-2">Дата истечения (необязательно)</label>
            <input 
              v-model="form.expires_at"
              type="datetime-local"
              class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2 editable"
            />
          </div>
        </div>

        <!-- Бонусы -->
        <div>
          <label class="block text-mywhite-2 mb-2">Бонусы</label>
          <div v-for="(bonus, index) in form.bonuses" :key="index" class="flex gap-2 mb-2">
            <select v-model="bonus.type_id" class="flex-1 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
                    :disabled="!isNewPromo">
              <option v-for="bt in bonusTypes" :key="bt.id" :value="bt.id">
                {{ bt.name }}
              </option>
            </select>
            <input 
              v-if="getHasAmount(bonus.type_id)"
              v-model.number="bonus.amount" 
              type="number" 
              placeholder="Кол-во" 
              class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
              :disabled="!isNewPromo"
            >
            <span v-else class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2 text-xs text-center">—</span>
            <button @click="removeBonus(index)" type="button" class="text-red-500 ml-2">×</button>
          </div>
          <button @click="addBonus" type="button" class="mt-2 text-mypurple-4 hover:text-mypurple-2"
                  :disabled="!isNewPromo">
            ➕ Добавить бонус
          </button>
        </div>

        <!-- Кнопка сохранения -->
        <div class="mt-6">
          <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md">
            {{ isNewPromo ? 'Создать' : 'Сохранить' }} промокод
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import promoCodeService from '@/services/promoCodeService'

const router = useRouter()
const route = useRoute()

// Определяем, новая это запись или редактирование
const isNewPromo = ref(!route.params.id)

const services = ref([])
const bonusTypes = ref([])

// Получаем список сервисов (игр)
onMounted(async () => {
  try {
    const [servicesRes, bonusTypesRes] = await Promise.all([
      promoCodeService.getServices(),
      promoCodeService.getBonusTypes()
    ])
    services.value = servicesRes.data
    bonusTypes.value = bonusTypesRes.data

    // Если это редактирование — загружаем данные
    if (!isNewPromo.value && route.params.id) {
      try {
        const response = await promoCodeService.getPromoCode(route.params.id)
        const data = response.data

        form.value = {
          code: data.code,
          status: data.status,
          service_id: data.service.id,
          created_at: formatDateTimeLocal(data.created_at),
          expires_at: data.expires_at ? formatDateTimeLocal(data.expires_at) : '',
          max_activations: data.max_activations || null,
          bonuses: data.bonuses.map(b => ({
            type_id: b.bonus_type.id,
            amount: b.amount
          }))
        }
      } catch (e) {
        console.error('Ошибка при загрузке промокода:', e)
        alert('Не удалось загрузить промокод')
        router.push('/admin/promocodes')
      }
    }
  } catch (e) {
    console.error('Ошибка при загрузке данных:', e)
  }
})

function formatDateTimeLocal(dateString) {
  if (!dateString) return ''

  const date = new Date(dateString)

  // Получаем компоненты локального времени
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0') // Месяцы с 0
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')

  return `${year}-${month}-${day}T${hours}:${minutes}`
}

// Форма
const form = ref({
  code: '',
  status: 'active',
  service_id: null,
  created_at: formatDateTimeLocal(new Date()),
  expires_at: '',
  max_activations: null,
  bonuses: [{ type_id: '', amount: null }]
})

function addBonus() {
  form.value.bonuses.push({ type_id: '', amount: null })
}

function removeBonus(index) {
  form.value.bonuses.splice(index, 1)
}

function getHasAmount(typeId) {
  const type = bonusTypes.value.find(bt => bt.id === typeId)
  return type?.is_amount || false
}

function onStatusChange() {
  if (form.value.status === 'active') {
    form.value.created_at = formatDateTimeLocal(new Date())
  }
}

async function submitForm() {
  try {
    // Преобразуем бонусы
    const bonusData = form.value.bonuses.map(bonus => ({
      bonus_type_id: bonus.type_id,
      amount: bonus.amount || null
    }))
    const payload = {
      code: form.value.code,
      status: form.value.status,
      service_id: form.value.service_id,
      created_at: form.value.created_at,
      expires_at: form.value.expires_at || undefined,
      max_activations: form.value.max_activations || undefined,
      bonuses: bonusData
    }

    if (isNewPromo.value) {
      await promoCodeService.createPromoCode(payload)
    } else {
      await promoCodeService.updatePromoCode(route.params.id, payload)
    }

    await router.push('/admin/promocodes')
  } catch (e) {
    console.error('Ошибка при сохранении промокода:', e)
    alert('Не удалось сохранить промокод')
  }
}
</script>