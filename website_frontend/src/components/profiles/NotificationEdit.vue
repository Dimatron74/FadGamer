<!-- src/components/profiles/NotificationEdit.vue -->

<template>
  <div class="bg-myblack-3 p-4 rounded-lg space-y-2">
    <!-- Заголовок и кнопка -->
    <div class="flex justify-between items-center">
      <p class="text-mywhite-2">Настройки уведомлений</p>
      <button 
        @click="toggleEdit" 
        class="text-mypurple-5 hover:text-mypurple-3 text-sm underline"
      >
        {{ isEditing ? 'Отмена' : 'Изменить' }}
      </button>
    </div>

    <!-- Отображение текущего значения -->
    <div v-if="!isEditing" class="text-mywhite-4 mt-1">
      {{ $t(currentLabel) }}
    </div>

    <!-- Форма изменения уведомлений -->
    <div v-show="isEditing" class="space-y-2">
      <select
        v-model="selectedType"
        class="w-full px-3 py-2 bg-myblack-2 border border-myblack-4 text-mywhite-3 rounded"
      >
        <option v-for="option in notificationOptions" :key="option.value" :value="option.value">
          {{ $t(option.label) }}
        </option>
      </select>

      <button 
        @click="saveNotificationType" 
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
const selectedType = ref(userStore.user.notification_type)
const isLoading = ref(false)

// Опции для выбора (ключи для i18n)
const notificationOptions = [
  { value: 'all', label: 'profile.notifications.all' },
  { value: 'important', label: 'profile.notifications.important_only' },
  { value: 'none', label: 'profile.notifications.none' }
]

// Текст текущего выбранного значения
const currentLabel = computed(() => {
  const option = notificationOptions.find(o => o.value === userStore.user.notification_type)
  return option ? (option.label) : 'profile.notifications.unknown'
})

function toggleEdit() {
  isEditing.value = !isEditing.value
  if (!isEditing.value) {
    // Сброс при отмене
    selectedType.value = userStore.user.notification_type
  }
}

async function saveNotificationType() {
  if (selectedType.value === userStore.user.notification_type || isLoading.value) return

  isLoading.value = true

  try {
    await profileService.updateProfile({
      notification_type: selectedType.value
    })

    // Обновляем данные пользователя
    await userStore.fetchUserInfo()

    isEditing.value = false
    alert('Настройки уведомлений успешно изменены')
  } catch (err) {
    console.error('Ошибка при сохранении настроек уведомлений:', err)
    alert('Не удалось сохранить настройки уведомлений')
  } finally {
    isLoading.value = false
  }
}
</script>