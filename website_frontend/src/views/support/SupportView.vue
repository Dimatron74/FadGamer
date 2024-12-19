<template>
  <div class="container mx-auto px-6 md:px-12">
    <h1 class="text-4xl font-bold">Страница поддержки</h1>
    <form @submit.prevent="sendRequest" class="space-y-4">
      <div class="flex flex-col">
        <label for="question" class="text-xl">Вопрос:</label>
        <input id="question" type="text" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="question" required autofocus />
      </div>

      <div class="flex flex-col">
        <label for="text" class="text-xl">Текст:</label>
        <textarea id="text" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="text" required></textarea>
      </div>

      <button type="submit" class="bg-myblack-5 text-mywhite-3 rounded p-2 w-full hover:bg-myblack-4 transition duration-300">Отправить</button>
    </form>

    <button @click="toggleFaqVisible" class="bg-myblack-5 text-mywhite-3 rounded p-2 w-full hover:bg-myblack-4 transition duration-300 mt-12">Показать FAQ</button>

    <div v-if="faqVisible" class="mt-12 space-y-6">
      <h2 class="text-3xl font-bold">Часто задаваемые вопросы</h2>
      <div v-for="faq in faqs" :key="faq.id" class="bg-myblack-3 p-4 rounded-lg">
        <h3 class="text-2xl block text-mywhite-5">Вопрос:</h3>
        <p class="text-lg mt-2 text-mywhite-2">{{ faq.question }}</p>
        <h3 class="text-2xl mt-4 block text-mywhite-5">Ответ:</h3>
        <p class="text-lg mt-2 text-mywhite-2">{{ faq.answer }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'


const router = useRouter()
const userStore = useUserStore()
const question = ref('');
const text = ref('');
const faqVisible = ref(false);
const faqs = ref([
  { id: 1, question: 'Как выйти из аккаунта?', answer: 'В профиле кнопка "Выйти"' },
]);

function sendRequest() {
  console.log('Валуе', question.value)
  axios.post('/support/request/', { question: question.value, text: text.value, user: userStore.user.id })
    .then(response => {
      console.log('Успех')
      router.push('/')
    })
    .catch(error => {
      console.log('Ошибка', error)
    });
}

function toggleFaq(id) {
  faqVisible.value = !faqVisible.value;
}

function toggleFaqVisible() {
  faqVisible.value = !faqVisible.value;
}
</script>

