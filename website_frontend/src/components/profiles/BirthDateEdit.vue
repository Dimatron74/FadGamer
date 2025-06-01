<!-- src/components/profiles/BirthDateEdit.vue -->

<template>
  <div class="bg-myblack-3 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Дата рождения</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Отображение текущей даты или форма редактирования -->
    <div v-if="!isEditing" class="text-mywhite-4 mt-1">
      {{ formattedBirthDate || 'Не указана' }}
    </div>

    <!-- Форма изменения даты рождения -->
    <div v-show="isEditing" class="space-y-2">
      <input 
        v-model="birthDate" 
        type="date" 
        class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
        :class="{ 'border-red-500': errorMessage }"
      />

      <p v-if="errorMessage" class="text-xs text-red-500">{{ errorMessage }}</p>

      <button 
        @click="saveBirthDate" 
        :disabled="isLoading"
        class="bg-mypurple-4 hover:bg-mypurple-3 text-white py-1 px-3 rounded text-sm disabled:opacity-50"
      >
        {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import profileService from '@/services/profileService'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isEditing = ref(false)
const birthDate = ref(userStore.user.birth_date || '')
const errorMessage = ref('')
const isLoading = ref(false)

// Форматируем дату для отображения (например: "1 января 2000")
const formattedBirthDate = computed(() => {
  if (!userStore.user.birth_date) return null
  const date = new Date(userStore.user.birth_date)
  const options = { day: 'numeric', month: 'long', year: 'numeric' }
  return date.toLocaleDateString('ru-RU', options)
})

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс формы при отмене
    birthDate.value = userStore.user.birth_date || ''
    errorMessage.value = ''
  }
}

async function saveBirthDate() {
  errorMessage.value = ''

  if (!birthDate.value) {
    errorMessage.value = 'Выберите дату рождения'
    return
  }

  // Проверяем корректность даты
  const selectedDate = new Date(birthDate.value)
  const today = new Date()
  const minAgeDate = new Date(today.getFullYear() - 150, today.getMonth(), today.getDate())
  const maxAgeDate = new Date(today.getFullYear() - 13, today.getMonth(), today.getDate())

  if (selectedDate > today) {
    errorMessage.value = 'Дата рождения не может быть в будущем'
    return
  }

  if (selectedDate > maxAgeDate) {
    errorMessage.value = 'Вы должны быть старше 13 лет'
    return
  }

  if (selectedDate < minAgeDate) {
    errorMessage.value = 'Дата рождения слишком ранняя'
    return
  }

  isLoading.value = true

  try {
    await profileService.updateProfile({
      birth_date: birthDate.value
    })

    // Обновляем данные пользователя
    await userStore.fetchUserInfo()

    isEditing.value = false
    alert('Дата рождения успешно обновлена')
  } catch (err) {
    console.error('Ошибка при обновлении даты рождения:', err)
    errorMessage.value = 'Не удалось сохранить дату рождения'
  } finally {
    isLoading.value = false
  }
}
</script>