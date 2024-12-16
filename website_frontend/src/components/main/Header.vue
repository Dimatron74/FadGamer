<template>
  <header class="bg-myblack-2 text-mywhite-3 body-font sticky" style="font-family: 'Roboto', sans-serif; font-weight: bold;">
    <div class="flex p-6 flex-col md:flex-row items-center h-20">
      <div class="flex items-center justify-start">
        <RouterLink to="/" @click="scrollToTop">
          <div class="text-2xl w-48 text-center">FAD GAMERS</div>
        </RouterLink>
      </div>
      <nav class="items-center text-lg justify-between ml-[74px] tracking-wider gap-2 hidden tablet-max:flex desktop-min:gap-10">
        <RouterLink to="/" class="hover:text-mywhite-5" @click="scrollToTop">ГЛАВНАЯ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5" @click="scrollToTop">ИГРЫ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5" @click="scrollToTop">НОВОСТИ</RouterLink>
        <RouterLink to="/about" class="hover:text-mywhite-5" @click="scrollToTop">ЦЕНТР ПОДДЕРЖКИ</RouterLink>
        <div @click="toggleDropdown" class="relative z-10">
          <span class="cursor-pointer hover:text-mywhite-5">ДРУГОЕ</span>
          <div v-if="dropdownOpen" class="absolute bg-myblack-2 shadow-lg mt-2">
            <RouterLink to="/promo" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3" @click="scrollToTop">Активировать промокод</RouterLink>
            <RouterLink to="/about" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3" @click="scrollToTop">О компании</RouterLink>
            <RouterLink to="" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-3" @click="scrollToTop">Сотрудничество</RouterLink>
          </div>
        </div>
      </nav>
      <div class="ml-auto">
        <RouterLink v-if="!userStore.user.access" to="/login" class="hover:text-mywhite-5 flex items-center gap-2" @click="scrollToTop">
          <span>ВОЙТИ</span>
          <IconProfile />
        </RouterLink>
        <RouterLink v-else to="/profile" class="hover:text-mywhite-5" @click="scrollToTop">ПРОФИЛЬ</RouterLink>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import IconProfile from "@/components/icons/IconProfile.vue";

const props = defineProps({
  userStore: {
    type: Object,
    required: true
  }
});

const dropdownOpen = ref(false);

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value;
}

function scrollToTop() {
  window.scrollTo(0,0);
}
</script>

<style scoped>
.sticky {
  position: fixed;
  top: 0;
  z-index: 1000;
  width: 100%;
}
</style>

