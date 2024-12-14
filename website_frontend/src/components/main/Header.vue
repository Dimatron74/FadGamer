<template>
  <header class="bg-myblack-2 text-mywhite-3 body-font" style="font-family: 'Roboto', sans-serif; font-weight: bold;">
    <div class="flex p-6 flex-col md:flex-row items-center h-20">
      <div class="flex items-center justify-start">
        <RouterLink to="/">
          <div class="text-2xl w-48 text-center">FAD GAMERS</div>
        </RouterLink>
      </div>
      <nav class="flex items-center text-lg justify-between ml-[74px] tracking-wider gap-2 tablet-max:gap-5 desktop-min:gap-10">
        <RouterLink to="/" class="hover:text-mywhite-5">ГЛАВНАЯ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5">ИГРЫ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5">НОВОСТИ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5">ЦЕНТР ПОДДЕРЖКИ</RouterLink>
        <div @click="toggleDropdown" class="relative z-10">
          <span class="cursor-pointer hover:text-mywhite-5">ДРУГОЕ</span>
          <div v-if="dropdownOpen" class="absolute bg-myblack-2 shadow-lg mt-2">
            <RouterLink to="/promo" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3">Активировать промокод</RouterLink>
            <RouterLink to="" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3">О компании</RouterLink>
            <RouterLink to="" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3">Сотрудничество</RouterLink>
          </div>
        </div>
      </nav>
      <div class="flex items-center justify-end gap-10 ml-auto">
        <RouterLink v-if="!userStore.user.access" to="/signup" class="hover:text-mywhite-5">Зарегистироваться</RouterLink>
        <RouterLink v-if="!userStore.user.access" to="/login" class="hover:text-mywhite-5">Авторизоваться</RouterLink>
        <RouterLink v-else to="/profile" class="hover:text-mywhite-5">ПРОФИЛЬ</RouterLink>
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
  },
  data() {
    return {
      dropdownOpen: false
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    }
  }
}
</script>

