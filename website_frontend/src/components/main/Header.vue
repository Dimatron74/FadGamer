<template>
  <header class="bg-black bg-opacity-90 text-white body-font" style="font-family: 'Roboto', sans-serif; font-weight: bold;">
    <div class="w-full flex p-6 flex-col md:flex-row items-center h-20">
      <div class="flex items-center justify-start">
        <RouterLink to="/">
          <div class="text-2xl w-48 text-center">FAD GAMERS</div>
        </RouterLink>
      </div>
      <nav class="flex items-center text-lg justify-between gap-10 ml-[74px] tracking-wider">
        <RouterLink to="/about" class="hover:text-gray-900">ГЛАВНАЯ</RouterLink>
        <RouterLink to="/about" class=" hover:text-gray-900">ИГРЫ</RouterLink>
        <RouterLink to="/about" class=" hover:text-gray-900">НОВОСТИ</RouterLink>
        <RouterLink to="/about" class=" hover:text-gray-900">ЦЕНТР ПОДДЕРЖКИ</RouterLink>
        <RouterLink to="/about" class=" hover:text-gray-900">ДРУГОЕ</RouterLink>
      </nav>
      <div class="flex items-center justify-end gap-10 ml-auto">
        <RouterLink v-if="!userStore.user.access" to="/signup" class=" hover:text-gray-900">Зарегистироваться</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/login" class=" hover:text-gray-900">Авторизоваться</RouterLink>
        <button v-else @click="userStore.removeToken()" class=" hover:text-gray-900">Выйти</button>
      </div>
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