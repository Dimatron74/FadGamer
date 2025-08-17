<template>
  <footer class="bg-myblack-2 py-6 h-60 relative border-t-4 border-myblack-3 border-opacity-50">
    <nav class="container mx-auto flex flex-col justify-center items-center text-mywhite-1">
      <ul class="flex items-center justify-center gap-5 text-sm pb-5">
        <li>
          <RouterLink to="/about" class="hover:text-mywhite-5">{{ $t('navigation.about') }}</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">{{ $t('navigation.contact') }}</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">{{ $t('main.policy') }}</RouterLink>
        </li>
        <li>
          <RouterLink to="/" class="">{{ $t('main.license') }}</RouterLink>
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
      <div class="mt-auto text-base text-gray-500">&copy; 2025 FadGamers. {{ $t('main.copyright') }}</div>
    </nav>
    <IconChangeLang class="absolute right-4 bottom-4 font-bold py-2 px-4 rounded"/>
  </footer>
</template>

<script setup>
import { watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';
import IconChangeLang from "@/components/icons/IconChangeLang.vue";

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



const { t, locale } = useI18n(); 

// Функция для смены языка
function switchLanguage(language) {
  const currentLocale = locale.value;
  let newLocale;
  if (currentLocale === 'ru') {
    newLocale = 'en';
  } else if (currentLocale === 'en') {
    newLocale = 'cn';
  } else if (currentLocale === 'cn') {
    newLocale = 'hi';
  } else {
    newLocale = 'ru';
  }
  locale.value = newLocale;  // Меняем язык с помощью vue-i18n
  localStorage.setItem('lang', newLocale);  // Сохраняем выбранный язык в localStorage
  console.log('Язык изменён на', newLocale);
}

watchEffect(() => {
  const lang = localStorage.getItem('lang');
  if (lang) {
    locale.value = lang;
  }
})
</script>
