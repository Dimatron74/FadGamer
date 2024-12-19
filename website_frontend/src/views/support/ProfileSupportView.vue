<template>
  <div class="container mx-auto p-4 text-mywhite-3">
    <h2 class="text-3xl font-bold mb-4">Ваши запросы в поддержку</h2>
    <button class="bg-blue-500 hover:bg-blue-700 text-mywhite-3 font-bold py-2 px-4 rounded" @click="updateSupportRequests">Обновить</button>
    <ul class="space-y-4 mt-4">
      <li v-for="request in supportRequests" :key="request.id" class="p-4 rounded bg-myblack-3 shadow-lg shadow-myblack-3">
        <h3 class="text-xl font-semibold">{{ request.question }}</h3>
        <p class="mb-2">Текст: {{ request.text }}</p>
        <p class="mb-2">Ответ: {{ request.answer || 'Пока нет ответа' }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const supportRequests = ref([]);
const updateSupportRequests = () => {
  axios.get(`/admin_panel/cms/api/support_requests/?user=${userStore.user.id}`)
    .then(response => {
      supportRequests.value = response.data;
    })
    .catch(error => {
      console.error("Ошибка получения запросов:", error);
    });
}

onMounted(() => {
  updateSupportRequests();
});
</script>

