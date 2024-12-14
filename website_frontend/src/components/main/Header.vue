<template>
  <header class="bg-myblack-2 w-screen text-mywhite-3 body-font" style="font-family: 'Roboto', sans-serif; font-weight: bold;">
    <div class="flex p-6 flex-col md:flex-row items-center h-20">
      <div class="flex items-center justify-start">
        <RouterLink to="/">
          <div class="text-2xl w-48 text-center">FAD GAMERS</div>
        </RouterLink>
      </div>
      <nav class="flex items-center text-lg justify-between ml-[74px] tracking-wider tablet-min:gap-2 tablet-max:gap-5 desktop-min:gap-10">
        <RouterLink to="/about" class="">ГЛАВНАЯ</RouterLink>
        <RouterLink to="/about" class="">ИГРЫ</RouterLink>
        <RouterLink to="/about" class="">НОВОСТИ</RouterLink>
        <RouterLink to="/about" class="">ЦЕНТР ПОДДЕРЖКИ</RouterLink>
        <RouterLink to="/about" class="">ДРУГОЕ</RouterLink>
      </nav>
      <div class="flex items-center justify-end gap-10 ml-auto">
        <RouterLink v-if="!userStore.user.access" to="/signup" class="hover:text-mywhite-5">Зарегистироваться</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/login" class="hover:text-mywhite-5">Авторизоваться</RouterLink>
        <button v-else @click="userStore.removeToken()" class="hover:text-mywhite-5">Выйти</button>
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

