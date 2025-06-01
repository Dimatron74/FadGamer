<!-- components/profiles/AvatarEdit.vue -->
<template>
  <div class="relative group">
    <div class="w-20 h-20 rounded-full overflow-hidden bg-myblack-5 flex items-center justify-center cursor-pointer border border-myblack-2 group-hover:border-mypurple-4 transition-all">
      <img v-if="userStore.user.avatar" :src="userStore.user.avatar" alt="avatar" class="w-full h-full object-cover" />
      <span v-else class="text-mywhite-1 text-2xl font-semibold">{{ userStore.user.name?.charAt(0) || '?' }}</span>
    </div>
    <input type="file" accept="image/*" @change="onFileChange" ref="fileInput" hidden />
    <button @click="$refs.fileInput.click()" class="absolute rounded-full inset-0 flex items-center justify-center bg-black bg-opacity-50 opacity-0 group-hover:opacity-100 transition-opacity text-white text-sm">Сменить</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import profileService from '@/services/profileService'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const fileInput = ref(null)

async function onFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('avatar', file)

  try {
    const res = await profileService.uploadAvatar(formData)
    const avatarUrl = res.data.avatar_url
    userStore.user.avatar = avatarUrl
    localStorage.setItem('user.avatar', avatarUrl)
  } catch (err) {
    console.error('Ошибка при загрузке аватара:', err)
  }
}
</script>