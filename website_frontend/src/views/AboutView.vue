<script setup>
import { useUserStore } from '@/stores/user'
import { ref } from 'vue';

const userStore = useUserStore()

const favoriteGenre = ref('');
const surveySubmitted = ref(false);

function submitSurvey() {
  surveySubmitted.value = true;
}
</script>



<template>
  <div class="about bg-gray-900 py-20">
    <div class="container mx-auto px-6 md:px-12">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-yellow-500">FadGamer</h1>
        <p class="text-xl text-gray-300">Компания по разработке игр</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12 mt-12">
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-bold text-yellow-500">Наша история</h2>
          <p class="text-gray-300">Мы - команда увлечённых разработчиков игр, которые любят создавать игры для Windows и Android с использованием Godot и Unity.</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-bold text-yellow-500">Наша миссия</h2>
          <p class="text-gray-300">Наша миссия - создавать игры, которые интересны, сложны и визуально привлекательны. Мы стремимся сделать игры доступными для всех, независимо от уровня навыков или платформы.</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-bold text-yellow-500">Наши достижения</h2>
          <p class="text-gray-300">Мы гордимся тем, что наши игры получили множество наград и признаний в индустрии. Наша команда постоянно работает над улучшением качества и инновациями.</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg">
          <h2 class="text-2xl font-bold text-yellow-500">Наши планы</h2>
          <p class="text-gray-300">Мы планируем расширять нашу команду и выходить на новые рынки, чтобы предложить ещё больше удивительных игровых впечатлений нашим пользователям. В приоритете - рынки СНГ и Китая.</p>
        </div>
        <div class="bg-gray-800 p-6 rounded-lg" v-if="userStore.user.access">
          <h2 class="text-2xl font-bold text-yellow-500">Интерактивный опрос</h2>
          <p class="text-gray-300">Какой ваш любимый жанр игр?</p>
          <ul class="text-gray-300">
            <li><input type="radio" id="rpg" value="RPG" v-model="favoriteGenre"> <label for="rpg">RPG</label></li>
            <li><input type="radio" id="fps" value="FPS" v-model="favoriteGenre"> <label for="fps">FPS</label></li>
            <li><input type="radio" id="strategy" value="Strategy" v-model="favoriteGenre"> <label for="strategy">Strategy</label></li>
          </ul>
          <button @click="submitSurvey" class="mt-4 bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">Проголосовать</button>
          <p v-if="surveySubmitted" class="mt-4 text-green-500">Спасибо за участие! Ваш любимый жанр: {{ favoriteGenre }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

