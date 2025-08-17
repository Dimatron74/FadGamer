<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter, RouterView, RouterLink } from 'vue-router'
import { watch, ref } from 'vue'

const userStore = useUserStore()
const router = useRouter()

// Реактивно следим за is_staff
watch(
  () => userStore.user.is_staff,
  async (newIsStaff) => {
    if (newIsStaff === false) {
      console.warn('Права администратора потеряны. Перенаправление...')
      await router.push('/')
    }
  },
  { immediate: true } // Проверяем сразу при монтировании
)

const menuItems = [
  { label: 'Главная', route: '/admin' },
  {
    label: 'Аккаунты',
    icon: '👥',
    children: [
      { label: 'Пользователи', route: '/admin/users' },
      { label: 'Блокировки', route: '/admin/blocked' },
    ]
  },
  { label: 'Посты', route: '/admin/news', icon: '📰' },
  { label: 'Тех. Поддержка', route: '/admin/support', icon: '💬' },
  { label: 'Промокоды', route: '/admin/promocodes', icon: '🎟️' },
  {
    label: 'Обращения',
    icon: '📨',
    route: '/admin/contacts'
  },
  {
    label: 'Статистика',
    icon: '📊',
    children: [
      { label: 'Общая статистика', route: '/admin/stats/general' },
      { label: 'Активность', route: '/admin/stats/activity' },
      { label: 'Графики', route: '/admin/stats/charts' }
    ]
  },
  { label: 'Настройки', route: '/admin/settings', icon: '⚙️' },
]

// Активное меню
const activeMenu = ref(null)

// Открытие/закрытие меню
function toggleMenu(index) {
  if (activeMenu.value === index) {
    activeMenu.value = null
  } else {
    activeMenu.value = index
  }
}

// Проверяет, является ли текущий маршрут активным
const isActiveRoute = (route) => {
  return router.currentRoute.value.path === route
}
</script>

<template>
  <div class="bg-myblack-2 text-mywhite-3 min-h-screen flex flex-co">
    <!-- Основной контент -->
    <main class="flex-1 flex flex-col md:flex-row">
      <!-- Левое меню -->
      <aside class="w-full md:w-64 bg-myblack-2 border-b md:border-b-0 md:border-r border-myblack-3 p-5">
        <!-- Логотип / Заголовок -->
        <div class="flex items-center gap-2 mb-8">
          <div class="w-10 h-10 rounded-lg bg-mypurple-4 flex items-center justify-center text-white font-bold">A</div>
          <h2 class="text-xl font-bold text-mywhite-5 tracking-tight">Админ панель</h2>
        </div>

        <!-- Меню -->
        <ul class="space-y-1">
          <li v-for="(item, index) in menuItems" :key="index">
            <!-- Пункт с подменю -->
            <div v-if="item.children">
              <button
                @click="toggleMenu(index)"
                class="group w-full flex items-center justify-between px-4 py-3 rounded-md transition-all duration-300 text-mywhite-3 hover:bg-mypurple-4 hover:text-white"
                :class="{ 'bg-mypurple-5 text-white': activeMenu === index }"
              >
                <div class="flex items-center">
                  <span class="mr-3 text-mypurple-4 group-hover:text-white transition-colors">{{ item.icon }}</span>
                  {{ item.label }}
                </div>
                <svg
                  :class="['w-4 h-4 text-mypurple-2 transform transition-transform duration-300', { 'rotate-180': activeMenu === index }]"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>

              <!-- Подменю -->
              <ul v-show="activeMenu === index" class="mt-1 ml-8 space-y-1">
                <li v-for="(child, childIndex) in item.children" :key="childIndex">
                  <RouterLink
                    :to="child.route"
                    class="block px-3 py-2 rounded-md text-sm text-mywhite-2 hover:bg-myblack-1 hover:text-mywhite-5"
                    :class="{ 'bg-myblack-1 text-white': isActiveRoute(child.route) }"
                  >
                    {{ child.label }}
                  </RouterLink>
                </li>
              </ul>
            </div>

            <!-- Обычный пункт -->
            <div v-else>
              <RouterLink
                :to="item.route"
                class="group relative flex items-center px-4 py-3 rounded-md transition-all duration-300 text-mywhite-3 hover:bg-mypurple-4 hover:text-white"
                :class="{ 'bg-mypurple-5 text-white': isActiveRoute(item.route) }"
              >
                <!-- Акцент слева -->
                <span
                  class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity bg-mypurple-4"
                ></span>

                <!-- Иконка -->
                <span class="mr-3 text-mypurple-4 group-hover:text-white transition-colors">{{ item.icon }}</span>

                <!-- Текст -->
                {{ item.label }}

                <!-- Стрелочка справа -->
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="ml-auto w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity text-mypurple-2"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </RouterLink>
            </div>
          </li>
        </ul>
      </aside>

      <!-- Контентная область -->
      <section class="flex-1 p-6 bg-myblack-2">
        <div>
          <RouterView />
        </div>
      </section>
    </main>
  </div>
</template>