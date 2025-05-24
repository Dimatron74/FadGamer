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
          <p class="text-mywhite-5">{{ promoCode.author.name }} ({{ promoCode.author.uid }})</p>
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
              <li v-for="(bonus, i) in promoCode.bonuses" :key="i">{{ bonus.type }}: {{ bonus.amount || 'Не указано' }}</li>
            </ul>
          </details>
        </div>

        <!-- Условия активации -->
        <div>
          <details class="bg-myblack-4 p-4 rounded-md">
            <summary class="cursor-pointer text-mywhite-3">Условия активации</summary>
            <ul class="mt-2 list-disc pl-5 space-y-1 text-mywhite-2">
              <li v-for="(cond, i) in promoCode.conditions" :key="i">{{ cond.type }}: {{ cond.value || 'Не указано' }}</li>
            </ul>
          </details>
        </div>

        <!-- Кнопки действий -->
        <div v-if="isActionAllowed" class="flex gap-4 mt-6">
          <button @click="endPromoCode" class="bg-myred-2 hover:bg-myred-1 text-white px-4 py-2 rounded-md">
            Завершить
          </button>
          <button @click="deletePromoCode" class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-md">
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  promoCode: {
    type: Object,
    required: true
  }
})

const BONUS_TYPES = {
  coins: { label: 'Монеты', hasAmount: true },
  premium: { label: 'Премиум аккаунт', hasAmount: false },
  access: { label: 'Доступ к мероприятию', hasAmount: false },
  skin: { label: 'Скин', hasAmount: true }
}

const CONDITION_TYPES = {
  coins: { label: 'Минимум монет', hasValue: true },
  level: { label: 'Минимум уровень', hasValue: true },
  event: { label: 'Доступ к событию', hasValue: false },
  item: { label: 'Наличие предмета', hasValue: false }
}

const emit = defineEmits(['close'])

const statusText = computed(() => {
  switch (props.promoCode.status) {
    case 'active': return 'Активный'
    case 'expired': return 'Истёк'
    case 'used': return 'Использован'
    default: return 'Неизвестный'
  }
})

const gameText = computed(() => {
  return props.promoCode.game === 'game1' ? 'Игра 1' : props.promoCode.game === 'game2' ? 'Игра 2' : 'Любая игра'
})

const isActionAllowed = computed(() => props.promoCode.status !== 'expired' && props.promoCode.status !== 'used')

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('ru-RU')
}

function endPromoCode() {
  // Логика завершения промокода
  console.log('Завершить промокод:', props.promoCode.code)
}

function deletePromoCode() {
  // Логика удаления промокода
  console.log('Удалить промокод:', props.promoCode.code)
}

function handleOutsideClick(e) {
  if (e.target.classList.contains('modal')) {
    emit('close')
  }
}

function formatBonus(bonus) {
  if (!bonus || !bonus.type) return 'Неизвестный бонус'

  const config = BONUS_TYPES[bonus.type] || { label: 'Неизвестный тип', hasAmount: false }

  if (config.hasAmount && bonus.amount !== undefined) {
    return `${config.label}: ${bonus.amount}`
  } else if (config.hasAmount === false) {
    return config.label
  }

  return 'Некорректный бонус'
}
</script>