<!-- src/components/profiles/EmailEdit.vue -->

<template>
  <div class="bg-myblack-3 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Email</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Форма редактирования -->
    <div v-show="isEditing && !showConfirmation" class="space-y-2">
      <input 
        v-model="newEmail" 
        type="email" 
        placeholder="Новый email" 
        class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
        :class="{ 'border-red-500': errorMessage }"
      />
      
      <p v-if="errorMessage" class="text-xs text-red-500">{{ errorMessage }}</p>

      <button 
        @click="saveEmail" 
        :disabled="isLoading"
        class="bg-mypurple-4 hover:bg-mypurple-3 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
      >
        {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </div>

    <!-- Форма ввода кода подтверждения -->
    <div v-show="showConfirmation" class="space-y-2">
      <p class="text-mywhite-3 text-sm">Введите код из письма, отправленного на {{ newEmail }}</p>
      <input 
        v-model="confirmationCode" 
        type="text" 
        placeholder="6-значный код" 
        maxlength="6"
        class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
        :class="{ 'border-red-500': errorMessage }"
      />
      
      <p v-if="errorMessage" class="text-xs text-red-500">{{ errorMessage }}</p>

      <button 
        @click="confirmCode" 
        :disabled="isLoading"
        class="bg-mypurple-4 hover:bg-mypurple-3 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
      >
        {{ isLoading ? 'Проверка...' : 'Подтвердить' }}
      </button>

      <button 
        @click="resendCode" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        Отправить код повторно
      </button>
    </div>

    <!-- Текстовое поле с текущим email -->
    <div v-show="!isEditing" class="text-mywhite-4 mt-1">
      {{ currentEmail || 'Не указан' }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import profileService from '@/services/profileService'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isEditing = ref(false)
const newEmail = ref('')
const confirmationCode = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const showConfirmation = ref(false)

// Получаем текущий email из стора
const currentEmail = ref(userStore.user.email || userStore.user.get_active_email)  // Адаптируйте, если email виртуальный

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    newEmail.value = ''
    confirmationCode.value = ''
    errorMessage.value = ''
    showConfirmation.value = false
  }
}

async function saveEmail() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!newEmail.value || !emailRegex.test(newEmail.value)) {
    errorMessage.value = 'Введите корректный email'
    return
  }

  if (newEmail.value === currentEmail.value) {
    errorMessage.value = 'Этот email уже используется'
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  try {
    await profileService.updateProfile({ email: newEmail.value })
    showConfirmation.value = true  // Показываем форму кода
  } catch (err) {
    console.error('Ошибка при обновлении email:', err)
    errorMessage.value = err.response?.data?.error || 'Не удалось изменить email. Попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}

async function confirmCode() {
  if (!confirmationCode.value || confirmationCode.value.length !== 6) {
    errorMessage.value = 'Введите 6-значный код'
    return
  }

  errorMessage.value = ''
  isLoading.value = true

  try {
    await profileService.confirmEmail({ code: confirmationCode.value, email: newEmail.value })
    // Обновляем данные пользователя
    await userStore.fetchUserInfo()
    currentEmail.value = userStore.user.email  // Или get_active_email
    isEditing.value = false
    showConfirmation.value = false
    newEmail.value = ''
    confirmationCode.value = ''
  } catch (err) {
    console.error('Ошибка при подтверждении:', err)
    errorMessage.value = err.response?.data?.error || 'Неверный код или ошибка. Попробуйте снова.'
  } finally {
    isLoading.value = false
  }
}

async function resendCode() {
  // Повторная отправка: Просто вызываем updateProfile снова
  await saveEmail()
  errorMessage.value = 'Код отправлен повторно'
}
</script>