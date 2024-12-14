<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const removeToken = () => {
    router.push('/')
    userStore.removeToken()
}
</script>

<template>
  <div class="container mx-auto p-4">
    <div class="w-full bg-white rounded-lg shadow-lg p-4">
      <div class="text-3xl font-bold mb-4">Профиль пользователя</div>
      
      <div class="flex flex-col space-y-4">
        <div class="flex items-center">
          <label class="w-1/3 text-gray-700" for="username">UUID:</label>
          <div class="w-2/3">{{ userStore.user.id }}</div>
        </div>

        <div class="flex items-center">
          <label class="w-1/3 text-gray-700" for="username">Никнейм:</label>
          <div class="w-2/3">{{ userStore.user.name }}</div>
        </div>
        
        <div class="flex items-center">
          <label class="w-1/3 text-gray-700" for="email">Email:</label>
          <div class="w-2/3">{{ userStore.user.email }}</div>
        </div>

        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">
          Редактировать профиль
        </button>
        <button @click="removeToken()" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-4">Выйти</button>
      </div>
    </div>
  </div>
</template>
