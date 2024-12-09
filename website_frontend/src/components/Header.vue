<template>
  <header class="bg-black bg-opacity-90 text-white body-font">
    <div class="container mx-3 flex flex-wrap p-3 flex-col md:flex-row items-center">
      <RouterLink to="/" class="mr-5 hover:text-gray-900">
        <span class="ml-3 text-xl">FadGamers</span>
      </RouterLink>
      <nav class="md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-700	flex flex-wrap items-center text-base justify-center">
        <RouterLink to="/about" class="mr-5 hover:text-gray-900">О нас</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/signup" class="mr-5 hover:text-gray-900">Зарегистироваться</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/login" class="mr-5 hover:text-gray-900">Авторизоваться</RouterLink>
        <button v-else @click="userStore.removeToken()" class="mr-5 hover:text-gray-900">Выйти</button>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    userStore: {
      type: Object,
      required: true
    }
  }
}
</script>