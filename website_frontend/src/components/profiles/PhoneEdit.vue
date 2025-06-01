<!-- src/components/profiles/PhoneEdit.vue -->

<template>
  <div class="bg-myblack-3 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Телефон</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Отображение текущего телефона или форма редактирования -->
    <div v-if="!isEditing" class="text-mywhite-4 mt-1">
      {{ userStore.user.phone_number || 'Не указан' }}
    </div>

    <!-- Форма изменения телефона -->
    <div v-show="isEditing" class="space-y-2">
      <input 
        v-model="phoneNumber" 
        type="tel" 
        placeholder="+7 (999) 999-99-99" 
        inputmode="numeric"
        pattern="[0-9+\s\-\(\)]*"
        maxlength="20"
        class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
        :class="{ 'border-red-500': errorMessage }"
      />

      <p v-if="errorMessage" class="text-xs text-red-500">{{ errorMessage }}</p>

      <button 
        @click="savePhoneNumber" 
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
const phoneNumber = ref(userStore.user.phone_number || '')
const errorMessage = ref('')
const isLoading = ref(false)

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    phoneNumber.value = userStore.user.phone_number || ''
    errorMessage.value = ''
  }
}

async function savePhoneNumber() {
  errorMessage.value = ''

  const value = phoneNumber.value.trim()

  if (value === userStore.user.phone_number) {
    errorMessage.value = 'Это текущий номер телефона'
    return
  }

  // Простая валидация формата телефона
  const phoneRegex = /^[\+]?[0-9\s\-()]{6,20}$/
  if (value && !phoneRegex.test(value)) {
    errorMessage.value = 'Введите корректный номер телефона'
    return
  }

  isLoading.value = true

  try {
    await profileService.updateProfile({
      phone_number: value || null
    })

    // Обновляем данные пользователя
    await userStore.fetchUserInfo()
    phoneNumber.value = userStore.user.phone_number

    isEditing.value = false
    alert('Номер телефона успешно обновлён')
  } catch (err) {
    console.error('Ошибка при обновлении номера телефона:', err)
    errorMessage.value = 'Не удалось сохранить номер телефона'
  } finally {
    isLoading.value = false
  }
}
</script>