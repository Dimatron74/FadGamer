<template>
  <div class="container mx-auto p-4 space-y-12 text-mywhite-1">


    <!-- Слайдер игр -->
    <GameSlider />

    <!-- Блок новостей -->
    <NewsSection />

    <!-- Блок формы обратной связи -->
    <ContactForm />
  </div>
</template>

<script setup>
import GameSlider from '@/components/games/GameSlider.vue';
import NewsSection from '@/components/news/NewsSection.vue';
import ContactForm from '@/views/main/ContactForm.vue';
</script>