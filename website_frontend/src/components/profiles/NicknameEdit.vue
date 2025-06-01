<!-- src/components/profiles/NicknameEdit.vue -->

<template>
  <div class="bg-myblack-4 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Никнейм</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Отображение текущего никнейма или форма редактирования -->
    <div v-if="!isEditing" class="text-mywhite-4 mt-1">
      {{ userStore.user.name || 'Не указан' }}
    </div>

    <!-- Форма изменения никнейма -->
    <div v-show="isEditing" class="space-y-2">
      <input 
        v-model="nickname" 
        type="text" 
        placeholder="Новый никнейм" 
        class="w-full px-3 py-2 bg-myblack-5 border border-myblack-2 rounded text-white"
        :class="{ 'border-red-500': errorMessage }"
      />

      <p v-if="errorMessage" class="text-xs text-red-500">{{ errorMessage }}</p>

      <button 
        @click="saveNickname" 
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
const nickname = ref(userStore.user.name || '')
const errorMessage = ref('')
const isLoading = ref(false)

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    nickname.value = userStore.user.name || ''
    errorMessage.value = ''
  }
}

async function saveNickname() {
  errorMessage.value = ''

  const value = nickname.value.trim()

  if (!value) {
    errorMessage.value = 'Никнейм не может быть пустым'
    return
  }

  if (value.length < 3 || value.length > 30) {
    errorMessage.value = 'Никнейм должен содержать от 3 до 30 символов'
    return
  }

  if (value === userStore.user.name) {
    errorMessage.value = 'Это текущий никнейм'
    return
  }

  isLoading.value = true

  try {
    await profileService.updateProfile({
      nickname: value
    })

    // Обновляем данные пользователя
    await userStore.fetchUserInfo()
    nickname.value = userStore.user.name

    isEditing.value = false
    alert('Никнейм успешно изменён')
  } catch (err) {
    console.error('Ошибка при обновлении никнейма:', err)
    if (err.response?.data?.error) {
      errorMessage.value = err.response.data.error
    } else {
      errorMessage.value = 'Не удалось сохранить никнейм'
    }
  } finally {
    isLoading.value = false
  }
}
</script>