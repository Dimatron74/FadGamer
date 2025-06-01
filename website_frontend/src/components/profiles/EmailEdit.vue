<!-- src/components/profiles/EmailEdit.vue -->

<template>
  <div class="bg-myblack-4 p-4 rounded-lg space-y-2">
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
    <div v-show="isEditing" class="space-y-2">
      <input 
        v-model="newEmail" 
        type="email" 
        placeholder="Новый email" 
        class="w-full px-3 py-2 bg-myblack-5 border border-myblack-2 rounded text-white"
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
const errorMessage = ref('')
const isLoading = ref(false)

// Получаем текущий email из стора
const currentEmail = ref(userStore.user.email)

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    newEmail.value = ''
    errorMessage.value = ''
  }
}

async function saveEmail() {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  // Валидация формата email
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
    
    // Обновляем данные пользователя
    await userStore.fetchUserInfo()
    currentEmail.value = userStore.user.email
    
    isEditing.value = false
    newEmail.value = ''
  } catch (err) {
    console.error('Ошибка при обновлении email:', err)
    errorMessage.value = 'Не удалось изменить email. Попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}
</script>