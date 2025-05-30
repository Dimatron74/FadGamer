<script setup>
import { ref } from 'vue'

// Данные для слайдера игр
const games = [
  { id: 1, title: "CyberQuest", image: "https://via.placeholder.com/600x400?text=CyberQuest" },
  { id: 2, title: "Galactic War", image: "https://via.placeholder.com/600x400?text=Galactic+War" },
  { id: 3, title: "Shadow Realm", image: "https://via.placeholder.com/600x400?text=Shadow+Realm" },
]

const currentGameIndex = ref(0)

const nextSlide = () => {
  currentGameIndex.value = (currentGameIndex.value + 1) % games.length
}

const prevSlide = () => {
  currentGameIndex.value = (currentGameIndex.value - 1 + games.length) % games.length
}

// Данные для новостей
const newsItems = [
  {
    id: 1,
    title: "Новость 1",
    description: "Краткое описание первой новости студии FagGamers.",
    image: "https://via.placeholder.com/300x200?text=News+1"
  },
  {
    id: 2,
    title: "Новость 2",
    description: "Краткое описание второй новости студии FagGamers.",
    image: "https://via.placeholder.com/300x200?text=News+2"
  },
  {
    id: 3,
    title: "Новость 3",
    description: "Краткое описание третьей новости студии FagGamers.",
    image: "https://via.placeholder.com/300x200?text=News+3"
  },
  {
    id: 4,
    title: "Новость 4",
    description: "Краткое описание четвёртой новости студии FagGamers.",
    image: "https://via.placeholder.com/300x200?text=News+4"
  },
  {
    id: 5,
    title: "Новость 5",
    description: "Краткое описание пятой новости студии FagGamers.",
    image: "https://via.placeholder.com/300x200?text=News+5"
  }
]

const activeNewsIndex = ref(0)

const setNewsIndex = (index) => {
  activeNewsIndex.value = index
}
</script>

<template>
  <div class="container mx-auto p-4 space-y-12 text-mywhite-1">
    <!-- Блок приветствия -->
    <div class="space-y-2">
      <h1 class="text-6xl font-black">{{ $t('global.welcome') }}</h1>
      <p class="text-2xl text-mywhite-2">{{ $t('global.welcome') }}</p>
    </div>

    <!-- Блок игр -->
    <section class="relative">
      <h2 class="text-3xl font-bold mb-4">Наши игры</h2>
      <div class="relative overflow-hidden rounded-lg shadow-lg">
        <img :src="games[currentGameIndex].image" :alt="games[currentGameIndex].title" class="w-full h-80 object-cover rounded-lg" />
        <button @click="prevSlide" class="absolute left-2 top-1/2 transform -translate-y-1/2 bg-mypurple-4 hover:bg-mypurple-5 text-myblack-1 p-2 rounded-full z-10">
          ❮
        </button>
        <button @click="nextSlide" class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-mypurple-4 hover:bg-mypurple-5 text-myblack-1 p-2 rounded-full z-10">
          ❯
        </button>
      </div>
      <div class="flex justify-center mt-2 space-x-2">
        <div v-for="(game, index) in games" :key="game.id"
             :class="['w-3 h-3 rounded-full', index === currentGameIndex ? 'bg-mypurple-4' : 'bg-mywhite-2']"
             @click="currentGameIndex = index"></div>
      </div>
    </section>

    <!-- Блок новостей -->
    <section>
      <h2 class="text-3xl font-bold mb-4">Новости</h2>
      <div class="flex flex-col md:flex-row gap-6 items-start">
        <img :src="newsItems[activeNewsIndex].image" alt="Preview" class="md:w-1/3 w-full rounded-lg object-cover h-64 md:h-auto" />
        <ul class="space-y-4 md:w-2/3">
          <li v-for="(item, index) in newsItems" :key="item.id"
              class="hover:text-mypurple-4 transition duration-300 cursor-pointer"
              @mouseenter="setNewsIndex(index)">
            <h3 class="text-xl font-semibold">{{ item.title }}</h3>
            <p class="text-mywhite-3">{{ item.description }}</p>
          </li>
        </ul>
      </div>
    </section>

    <!-- Блок формы обратной связи -->
    <section class="bg-myblack-2 p-6 rounded-lg shadow-md">
      <h2 class="text-3xl font-bold mb-4">Связь с поддержкой</h2>
      <form class="space-y-4">
        <div>
          <label for="name" class="block text-mywhite-2 mb-1">Имя</label>
          <input type="text" id="name" placeholder="Ваше имя" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4" />
        </div>
        <div>
          <label for="email" class="block text-mywhite-2 mb-1">Email</label>
          <input type="email" id="email" placeholder="Ваш email" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4" />
        </div>
        <div>
          <label for="message" class="block text-mywhite-2 mb-1">Сообщение</label>
          <textarea id="message" rows="4" placeholder="Текст сообщения" class="w-full bg-myblack-3 border border-myblack-4 rounded px-3 py-2 text-mywhite-1 focus:outline-none focus:border-mypurple-4"></textarea>
        </div>
        <button type="submit" class="bg-mypurple-4 hover:bg-mypurple-5 text-myblack-1 px-6 py-2 rounded font-semibold transition">
          Отправить
        </button>
      </form>
    </section>
  </div>
</template>