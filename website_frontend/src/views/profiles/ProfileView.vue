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
  <div class="container mx-auto p-4">
    <div class="w-full bg-myblack-3 rounded-lg shadow-lg p-4">
      <div class="text-3xl font-bold mb-4">{{ $t('profile.profileuser') }}</div>
      
      <div class="flex flex-col space-y-4">
        <div class="flex items-center">
          <label class="w-1/3" for="username">UUID:</label>
          <div class="w-2/3">{{ userStore.user.id }}</div>
        </div>

        <div class="flex items-center">
          <label class="w-1/3" for="username">{{$t('profile.nickname')}}</label>
          <div class="w-2/3">{{ userStore.user.name }}</div>
        </div>
        
        <div class="flex items-center">
          <label class="w-1/3" for="email">{{ $t('profile.email') }}</label>
          <div class="w-2/3">{{ userStore.user.email }}</div>
        </div>

        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4 max-w-fit">
          {{$t('profile.edit_profile')}}
        </button>
        <button @click="router.push('/promo')" class="bg-mypurple-5 hover:bg-mypurple-2 text-white font-bold py-2 px-4 rounded mt-4 max-w-fit">
          Активировать промокод
        </button>
        <button @click="showSupports = !showSupports" class="bg-myred-5 hover:bg-myred-2 text-white font-bold py-2 px-4 rounded mt-4 max-w-fit">Отобразить запросы в поддержку</button>
        <div class="h-16"></div>
        <button @click="removeToken()" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-4 max-w-fit">{{$t('auth.logout')}}</button>
      </div>
    </div>
    <div v-if="showSupports">
      <ProfileSupportView />
    </div>
  </div>
</template>

