<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-70 modal" @click.self="handleOutsideClick">
    <div class="bg-myblack-3 rounded-lg shadow-lg w-full max-w-3xl max-h-[90vh] overflow-y-auto mx-4">
      <!-- Заголовок -->
      <div class="flex justify-between items-center p-6 border-b border-myblack-4">
        <h2 class="text-2xl font-bold text-mywhite-5">Промокод: {{ promoCode.code }}</h2>
        <button @click="$emit('close')" class="text-mywhite-2 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Контент модального окна -->
      <div class="p-6 space-y-4">
        <!-- Информация -->
        <div>
          <label class="block text-mywhite-2 text-sm">Статус</label>
          <p class="text-mywhite-5">{{ statusText }}</p>
        </div>

        <div>
          <label class="block text-mywhite-2 text-sm">Игра</label>
          <p class="text-mywhite-5">{{ gameText }}</p>
        </div>

        <div>
          <label class="block text-mywhite-2 text-sm">Автор</label>
          <p class="text-mywhite-5">{{ promoCode.author?.nickname ? `${promoCode.author.nickname} (UID: ${promoCode.author.uid})` : '—' }}</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-mywhite-2 text-sm">Создан</label>
            <p class="text-mywhite-5">{{ formatDate(promoCode.created_at) }}</p>
          </div>
          <div v-if="promoCode.expires_at">
            <label class="block text-mywhite-2 text-sm">Истекает</label>
            <p class="text-mywhite-5">{{ formatDate(promoCode.expires_at) }}</p>
          </div>
        </div>

        <!-- Бонусы -->
        <div>
          <details class="bg-myblack-4 p-4 rounded-md">
            <summary class="cursor-pointer text-mywhite-3">Бонусы</summary>
            <ul class="mt-2 list-disc pl-5 space-y-1 text-mywhite-2">
              <li v-for="(bonus, i) in promoCode.bonuses" :key="i">
                {{ getBonusLabel(bonus) }}
              </li>
            </ul>
          </details>
        </div>

        <!-- Кнопки действий -->
        <div v-if="isActionAllowed" class="flex gap-4 mt-6">
          <button @click="deletePromoCode" class="bg-myred-2 hover:bg-myred-1 text-white px-4 py-2 rounded-md">
            Удалить
          </button>
          <button @click="endPromoCode" class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md">
            Завершить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'
import promoCodeService from '@/services/promoCodeService'

const props = defineProps({
  promoCode: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'update'])

// Отображение статуса
const statusText = computed(() => {
  switch (props.promoCode.status) {
    case 'active': return 'Активный'
    case 'expired': return 'Истёк'
    case 'used': return 'Использован'
    case 'inactive': return 'Неактивен'
    case 'closed': return 'Завершён'
    default: return 'Неизвестный'
  }
})

// Отображение игры
const gameText = computed(() => {
  return props.promoCode.service?.name || 'Неизвестная игра'
})

// Проверка доступности действий
const isActionAllowed = computed(() => props.promoCode.status !== 'expired' && props.promoCode.status !== 'used')

// Форматирование даты
function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('ru-RU')
}

// Получение имени бонуса — без BONUS_TYPES
function getBonusLabel(bonus) {
  if (!bonus.bonus_type) return 'Неизвестный тип'

  const name = bonus.bonus_type.name
  const amount = bonus.amount

  if (amount != null && amount !== undefined) {
    return `${name}: ${amount}`
  }

  return name
}

// Завершение промокода
async function endPromoCode() {
  try {
    await promoCodeService.updatePromoCode(props.promoCode.id, {
      status: 'closed'
    })
    emit('update')
    alert('Промокод завершён')
  } catch (e) {
    console.error('Ошибка при завершении промокода:', e)
    alert('Не удалось завершить промокод')
  }
}

// Удаление промокода
async function deletePromoCode() {
  if (!confirm('Вы уверены, что хотите удалить этот промокод?')) return

  try {
    await promoCodeService.deletePromoCode(props.promoCode.id)
    emit('update') // триггерим обновление
    alert('Промокод удалён')
    emit('close')
  } catch (e) {
    console.error('Ошибка при удалении промокода:', e)
    alert('Не удалось удалить промокод')
  }
}

function handleOutsideClick(e) {
  if (e.target.classList.contains('modal')) {
    emit('close')
  }
}
</script>