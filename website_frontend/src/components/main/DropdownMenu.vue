<template>
  <div class="relative group">
    <button class="cursor-pointer hover:text-mywhite-5 focus:outline-none transition-colors duration-300">
      {{ label }}
    </button>

    <div class="absolute left-0 mt-2 w-48 bg-myblack-3 rounded-md shadow-lg hidden group-hover:block z-10">
      <ul>
        <li v-for="link in items" :key="link.to" class="block px-4 py-2 text-mywhite-3 hover:bg-myblack-4">
          <RouterLink :to="link.to" @click="scrollToTop">{{ link.label }}</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const router = useRouter()
const props = defineProps({
  label: String,
  items: Array,
  mobile: Boolean
})

const scrollToTop = () => {
  router.push(props.link)
}
</script>