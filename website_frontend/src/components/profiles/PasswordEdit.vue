<!-- src/components/profiles/PasswordEdit.vue -->

<template>
  <div class="bg-myblack-3 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Пароль</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Форма изменения пароля -->
    <div v-show="isEditing" class="space-y-2">
      <!-- Старый пароль -->
      <div class="relative">
        <input 
          v-model="oldPassword" 
          :type="showOldPassword ? 'text' : 'password'" 
          placeholder="Старый пароль" 
          class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
          :class="{ 'border-red-500': errors.old_password }"
        />
        <button 
          type="button"
          @click="toggleShowOldPassword"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 text-mywhite-3 text-xs"
        >
          {{ showOldPassword ? 'Скрыть' : 'Показать' }}
        </button>
      </div>

      <!-- Новый пароль -->
      <div class="relative">
        <input 
          v-model="newPassword" 
          :type="showNewPassword ? 'text' : 'password'" 
          placeholder="Новый пароль" 
          class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
          :class="{ 'border-red-500': errors.new_password }"
        />
        <button 
          type="button"
          @click="toggleShowNewPassword"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 text-mywhite-3 text-xs"
        >
          {{ showNewPassword ? 'Скрыть' : 'Показать' }}
        </button>
      </div>

      <!-- Повторите пароль -->
      <div class="relative">
        <input 
          v-model="repeatPassword" 
          :type="showRepeatPassword ? 'text' : 'password'" 
          placeholder="Повторите пароль" 
          class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
          :class="{ 'border-red-500': errors.repeat_password }"
        />
        <button 
          type="button"
          @click="toggleShowRepeatPassword"
          class="absolute right-2 top-1/2 transform -translate-y-1/2 text-mywhite-3 text-xs"
        >
          {{ showRepeatPassword ? 'Скрыть' : 'Показать' }}
        </button>
      </div>

      <!-- Сообщения об ошибках -->
      <ul v-if="Object.keys(errors).length > 0" class="text-xs text-red-500 list-disc pl-5 space-y-1">
        <li v-for="(error, key) in errors" :key="key">{{ error }}</li>
      </ul>

      <!-- Кнопка сохранить -->
      <button 
        @click="savePassword" 
        :disabled="isLoading"
        class="bg-mypurple-4 hover:bg-mypurple-3 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
      >
        {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import profileService from '@/services/profileService'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isEditing = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const repeatPassword = ref('')
const errors = ref({})
const isLoading = ref(false)

// Переключатели отображения паролей
const showOldPassword = ref(false)
const showNewPassword = ref(false)
const showRepeatPassword = ref(false)

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    oldPassword.value = ''
    newPassword.value = ''
    repeatPassword.value = ''
    errors.value = {}
  }
}

function toggleShowOldPassword() {
  showOldPassword.value = !showOldPassword.value
}
function toggleShowNewPassword() {
  showNewPassword.value = !showNewPassword.value
}
function toggleShowRepeatPassword() {
  showRepeatPassword.value = !showRepeatPassword.value
}

async function savePassword() {
  errors.value = {}

  // Валидация полей
  if (!oldPassword.value.trim()) {
    errors.value.old_password = 'Введите текущий пароль'
  }

  if (!newPassword.value.trim()) {
    errors.value.new_password = 'Введите новый пароль'
  }

  if (newPassword.value !== repeatPassword.value) {
    errors.value.repeat_password = 'Пароли не совпадают'
  }

  if (Object.keys(errors.value).length > 0) return

  isLoading.value = true

  try {
    await profileService.updateProfile({
      old_password: oldPassword.value,
      new_password: newPassword.value
    })

    alert('Пароль успешно изменён')
    isEditing.value = false
  } catch (err) {
    console.error('Ошибка при смене пароля:', err)
    if (err.response?.data?.error) {
      alert(err.response.data.error)
    } else {
      alert('Не удалось изменить пароль. Попробуйте позже.')
    }
  } finally {
    isLoading.value = false
  }
}
</script>