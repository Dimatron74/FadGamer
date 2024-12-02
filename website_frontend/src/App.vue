<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { ref, onMounted, watchEffect } from 'vue'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'

  const userStore = useUserStore()

  const userAccess = ref(userStore.user.access)

  watchEffect(() => {
    const token = userAccess.value
    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
    console.log('Ватч вызов', token)
  })

  onMounted(() => {
    userStore.initStore()
  })
</script>

<template>
  <header class="bg-black bg-opacity-90 text-white body-font">
    <div class="container mx-3 flex flex-wrap p-3 flex-col md:flex-row items-center">
      <RouterLink to="/" class="mr-5 hover:text-gray-900">
        <span class="ml-3 text-xl">FadGamer</span>
      </RouterLink>
      <nav class="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-700	flex flex-wrap items-center text-base justify-center">
        <RouterLink to="/about" class="mr-5 hover:text-gray-900">О нас</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/signup" class="mr-5 hover:text-gray-900">Зарегистироваться</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/login" class="mr-5 hover:text-gray-900">Авторизоваться</RouterLink>
        <button v-else @click="userStore.removeToken()" class="mr-5 hover:text-gray-900">Выйти</button>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<!-- <script>
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'

  export default {
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    beforeCreate() {
      this.userStore = useUserStore()
      this.userStore.initStore()

      const token = this.userStore.user.access
      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token
      } else {
        axios.defaults.headers.common['Authorization'] = ''
      }

    },
}
</script> -->