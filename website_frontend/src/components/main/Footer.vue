<template>
  <footer class="fixed bottom-0 left-0 right-0 bg-black text-white p-4">
    <div class="container mx-auto">
      <div class="flex justify-between items-center">
        <div class="text-sm">
          &copy; 2024 FadGamers. All rights reserved.
        </div>
        <nav class="space-x-4">
          <RouterLink to="/about" class="hover:text-gray-400">О нас</RouterLink>
          <RouterLink to="/contact" class="hover:text-gray-400">Контакты</RouterLink>
          <RouterLink to="/privacy" class="hover:text-gray-400">Политика конфиденциальности</RouterLink>
        </nav>
      </div>
    </div>
  </footer>
</template>


<script>
export default {
  props: {
    userStore: {
      type: Object,
      required: true
    }
  }
}
</script>