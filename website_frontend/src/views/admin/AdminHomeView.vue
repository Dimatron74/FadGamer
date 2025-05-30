<template>
  <div class="bg-myblack-2 p-6 rounded-lg shadow-md">
    <h1 class="text-3xl font-bold text-mywhite-5 mb-8">Панель администратора</h1>

    <!-- Статистика / Инфо блок -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
      <!-- Карточка 1 -->
      <div class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-mywhite-2">Активные пользователи</h3>
          <span class="text-mypurple-5 text-xl">👥</span>
        </div>
        <p class="text-3xl font-bold text-mywhite-5 mt-2">2</p>
        <p class="text-sm text-mywhite-1 mt-1">+100% за неделю</p>
      </div>

      <!-- Карточка 2 -->
      <div class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-mywhite-2">Промокоды</h3>
          <span class="text-mypurple-5 text-xl">🎟️</span>
        </div>
        <p class="text-3xl font-bold text-mywhite-5 mt-2">4</p>
        <p class="text-sm text-mywhite-1 mt-1">Из них 3 активны</p>
      </div>

      <!-- Карточка 3 -->
      <div class="bg-myblack-3 rounded-lg shadow-md p-5 border border-myblack-4 hover:border-mypurple-4 transition-all duration-300">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold text-mywhite-2">Техподдержка</h3>
          <span class="text-mypurple-5 text-xl">💬</span>
        </div>
        <p class="text-3xl font-bold text-mywhite-5 mt-2">12</p>
        <p class="text-sm text-mywhite-1 mt-1">Новых обращений</p>
      </div>
    </div>

    <!-- Блок информации -->
    <div class="bg-myblack-3 rounded-lg shadow-md p-6">
      <p class="text-mywhite-2 mb-4">Добро пожаловать в админ-панель, {{ userStore.user.name }}!</p>
      <p class="text-mywhite-1 text-sm">Email: {{ userStore.user.email }}</p>

      <div class="mt-6">
        <h2 class="text-xl font-semibold text-mywhite-3 mb-3">Функции админки</h2>
        <ul class="space-y-2 text-mywhite-2">
          <li class="flex items-center gap-2">
            <span class="text-mypurple-4">•</span> Управление промокодами
          </li>
          <li class="flex items-center gap-2">
            <span class="text-mypurple-4">•</span> ИИ-поддержка
          </li>
          <li class="flex items-center gap-2">
            <span class="text-mypurple-4">•</span> Статистика пользователей
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>