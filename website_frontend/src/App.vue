<script setup>
  import { RouterView, RouterLink } from 'vue-router'
  import { ref, onMounted, watchEffect } from 'vue'
  import { useUserStore } from '@/stores/user'
  import axios from 'axios'
  import Header from '@/components/main/Header.vue'
  import Footer from '@/components/main/Footer.vue'
  import VueCookies from 'vue-cookies';

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
    axios.get('profiles/api/csrf-token/')
      .then(response => {
        VueCookies.set('csrftoken', response.data.csrf_token);
      })
      .catch(error => {
        console.error(error);
      });
  })
</script>



<template>
  <Header :user-store="userStore"/>
  <main class="bg-myblack-4 text-mywhite-5 min-h-screen flex flex-col justify-center" style="font-family: 'Roboto', sans-serif; font-weight: 400;" id="top">
    <RouterView :user-store="userStore" />
  </main>
  <Footer :user-store="userStore" style="font-family: 'Roboto', sans-serif; font-weight: 400;"/>
</template>