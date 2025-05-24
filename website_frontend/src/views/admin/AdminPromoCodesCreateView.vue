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
      <h2 class="text-2xl font-bold text-mywhite-5 mb-6">Создание промокода</h2>

      <form @submit.prevent="submitForm" class="space-y-6">
        <div>
          <label class="block text-mywhite-2 mb-2">Название промокода</label>
          <input v-model="form.code" type="text" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2" required>
        </div>

        <div>
          <label class="block text-mywhite-2 mb-2">Статус</label>
          <select v-model="form.status" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
            <option value="active">Активный</option>
            <option value="inactive">Неактивный</option>
          </select>
        </div>

        <div>
          <label class="block text-mywhite-2 mb-2">Выберите игру</label>
          <select v-model="form.game" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
            <option value="game1">Игра 1</option>
            <option value="game2">Игра 2</option>
          </select>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-mywhite-2 mb-2">Дата активации</label>
            <input v-model="form.created_at" type="datetime-local" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
          </div>
          <div>
            <label class="block text-mywhite-2 mb-2">Дата истечения (необязательно)</label>
            <input v-model="form.expires_at" type="datetime-local" class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
          </div>
        </div>

        <!-- Автор заполняется автоматически -->
        <div>
          <label class="block text-mywhite-2 mb-2">Автор</label>
          <input :value="userStore.user.name" disabled class="w-full bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2 opacity-70">
        </div>

        <!-- Бонусы -->
        <div>
        <label class="block text-mywhite-2 mb-2">Бонусы</label>
        <div v-for="(bonus, index) in form.bonuses" :key="index" class="flex gap-2 mb-2">
            <select v-model="bonus.type" class="flex-1 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
            <option v-for="(item, key) in BONUS_TYPES" :key="key" :value="key">
                {{ item.label }}
            </option>
            </select>
            <input 
            v-if="BONUS_TYPES[bonus.type]?.hasAmount" 
            v-model.number="bonus.amount" 
            type="number" 
            placeholder="Кол-во" 
            class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
            >
            <span v-else class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2 text-xs text-center">—</span>
            <button @click="removeBonus(index)" type="button" class="text-red-500 ml-2">×</button>
        </div>
        <button @click="addBonus" type="button" class="mt-2 text-mypurple-4 hover:text-mypurple-2">
            ➕ Добавить бонус
        </button>
        </div>

        <!-- Условия активации -->
        <div>
        <label class="block text-mywhite-2 mb-2">Условия активации</label>
        <div v-for="(condition, index) in form.conditions" :key="index" class="flex gap-2 mb-2">
            <select v-model="condition.type" class="flex-1 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2">
            <option v-for="(item, key) in CONDITION_TYPES" :key="key" :value="key">
                {{ item.label }}
            </option>
            </select>
            <input 
            v-if="CONDITION_TYPES[condition.type]?.hasValue" 
            v-model.number="condition.value" 
            type="number" 
            placeholder="Значение" 
            class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2"
            >
            <span v-else class="w-32 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded p-2 text-xs text-center">—</span>
            <button @click="removeCondition(index)" type="button" class="text-red-500 ml-2">×</button>
        </div>
        <button @click="addCondition" type="button" class="mt-2 text-mypurple-4 hover:text-mypurple-2">
            ➕ Добавить условие
        </button>
        </div>

        <!-- Кнопка сохранения -->
        <div class="mt-6">
          <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-3 text-white px-4 py-2 rounded-md">
            Сохранить промокод
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const form = ref({
  code: '',
  status: 'active',
  game: 'game1',
  created_at: new Date().toISOString().slice(0, 16),
  expires_at: '',
  bonuses: [{ type: 'coins', amount: 50, noAmount: false }],
  conditions: [{ type: 'coins', value: 100, noValue: false }]
})

function addBonus() {
  form.value.bonuses.push({ type: '', amount: null })
}

function removeBonus(index) {
  form.value.bonuses.splice(index, 1)
}

function addCondition() {
  form.value.conditions.push({ type: '', value: null })
}

function removeCondition(index) {
  form.value.conditions.splice(index, 1)
}

const BONUS_TYPES = {
  coins: { label: 'Монеты', hasAmount: true },
  premium: { label: 'Премиум аккаунт', hasAmount: false }, // например, без количества
  access: { label: 'Доступ к мероприятию', hasAmount: false },
  skin: { label: 'Скин', hasAmount: true }
}

const CONDITION_TYPES = {
  coins: { label: 'Минимум монет', hasValue: true },
  level: { label: 'Минимум уровень', hasValue: true },
  event: { label: 'Доступ к событию', hasValue: false },
  item: { label: 'Наличие предмета', hasValue: false }
}
</script>