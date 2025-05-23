<script setup>
import { ref } from 'vue'
import axios from 'axios';
import { useRouter } from 'vue-router'
import ProfileSupportView from '@/views/support/ProfileSupportView.vue'

const { userStore } = defineProps({
  userStore: {
    type: Object,
    required: true
  }
});

const router = useRouter()

const removeToken = () => {
    router.push('/')
    userStore.removeToken()
}

const showSupports = ref(false)
</script>

<template>
  <div class="container mx-auto p-4 max-w-4xl">
    <div class="text-3xl font-bold mb-6 relative z-10">{{ $t('profile.profileuser') }}</div>
    
    <!-- Grid контейнер для карточек -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Карточка UID -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">UID</h3>
          <p class="text-white">{{ userStore.user.uid }}</p>
        </div>
        <div class="mt-auto flex justify-end">
          <button class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded">
            {{ $t('profile.uidcopy') }}
          </button>
        </div>
      </div>

      <!-- Карточка Никнейм -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">{{ $t('profile.nickname') }}</h3>
          <p class="text-white">{{ userStore.user.name }}</p>
        </div>
        <button class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded mt-4 w-full">
          {{ $t('profile.edit') }}
        </button>
      </div>

      <!-- Карточка Email -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">{{ $t('profile.email') }}</h3>
          <p class="text-white">{{ userStore.user.email }}</p>
        </div>
        <button class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded mt-4 w-full">
          {{ $t('profile.change') }}
        </button>
      </div>

      <!-- Карточка Промокод -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">Промокод</h3>
          <p class="text-white">Активировать бонус</p>
        </div>
        <button 
          @click="router.push('/promo')"
          class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded mt-4 w-full"
        >
          Активировать
        </button>
      </div>

      <!-- Карточка Поддержка -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">Поддержка</h3>
          <p class="text-white">Мои запросы</p>
        </div>
        <button 
          @click="showSupports = !showSupports"
          class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded mt-4 w-full"
        >
          Показать
        </button>
      </div>

      <!-- Карточка Выход -->
      <div class="bg-myblack-3 rounded-lg shadow-lg p-5 flex flex-col justify-between h-48">
        <div>
          <h3 class="text-lg font-semibold text-gray-300 mb-3">Аккаунт</h3>
          <p class="text-white">Завершить сессию</p>
        </div>
        <button 
          @click="removeToken()"
          class="bg-myred-2 hover:bg-myred-1 text-white font-bold py-2 px-4 rounded mt-4 w-full"
        >
          {{ $t('auth.logout') }}
        </button>
      </div>
    </div>

    <!-- Отображение поддержки -->
    <div v-if="showSupports" class="mt-6">
      <ProfileSupportView />
    </div>
  </div>
</template>