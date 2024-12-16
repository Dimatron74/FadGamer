<template>
  <footer class="bg-myblack-2 py-6 h-60 relative">
    <nav class="container mx-auto flex flex-col justify-center items-center text-mywhite-1">
      <ul class="flex items-center justify-center gap-5 text-sm pb-5">
        <li>
          <RouterLink to="/about" class="hover:text-mywhite-5" @click="scrollToTop">О компании</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">Сотрудничество</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">Политика конфиденциальности</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">Лицензионное соглашение</RouterLink>
        </li>
      </ul>
      <ul class="flex items-center justify-center gap-5 pb-[30px]">
        <li>
          <a href="" target="_blank" rel="noopener noreferrer">
            <IconTelegram />
          </a>
        </li>
        <li>
          <a href="" target="_blank" rel="noopener noreferrer">
            <IconVK />
          </a>
        </li>
        <li>
          <a href="" target="_blank" rel="noopener noreferrer">
            <IconYouTube />
          </a>
        </li>
        <li>
          <a href="" target="_blank" rel="noopener noreferrer">
            <IconDiscord />
          </a>
        </li>
        <li>
          <a href="" target="_blank" rel="noopener noreferrer">
            <IconX />
          </a>
        </li>
      </ul>
      <div class="text-3xl text-center pb-3" style="font-family: 'Roboto', sans-serif; font-weight: bold;">FAD GAMERS</div>
      <div class="mt-auto text-base text-gray-500">&copy; 2024 FadGamers. Все права защищены.</div>
    </nav>
    <button class="absolute right-4 bottom-4 bg-gray-700 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded" @click="switchLanguage(locale === 'ru' ? 'en' : 'ru')">
      {{ $t('navigation.language') }}
    </button>
  </footer>
</template>

<script setup>
import { watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';

// Иконки
import IconVK from "@/components/icons/IconVK.vue"
import IconDiscord from "@/components/icons/IconDiscord.vue"
import IconTelegram from "@/components/icons/IconTelegram.vue"
import IconX from "@/components/icons/IconX.vue"
import IconYouTube from "@/components/icons/IconYouTube.vue"

const props = defineProps({
  userStore: {
    type: Object,
    required: true
  }
});

function scrollToTop() {
  window.scrollTo(0,0);
}


const { t, locale } = useI18n(); 
// Функция для смены языка
function switchLanguage(language) {
  locale.value = language;  // Меняем язык с помощью vue-i18n
  localStorage.setItem('lang', language);  // Сохраняем выбранный язык в localStorage
  console.log('Язык изменён на', language);
}

watchEffect(() => {
  const lang = localStorage.getItem('lang');
  if (lang) {
    locale.value = lang;
  }
})
</script>
