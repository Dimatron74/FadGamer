<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { ref, onMounted, watchEffect } from 'vue'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'
  import Header from '@/components/main/Header.vue'
  import Footer from '@/components/main/Footer.vue'

  const userStore = useUserStore()
  const userAccess = ref(userStore.user.access)

  // components: { Header, Footer, RouterView }

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
  <Header :user-store="userStore" />
  <RouterView />
  <Footer :user-store="userStore" />
</template>