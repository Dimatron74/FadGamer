import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import HomeView from '@/views/main/HomeView.vue'
import SignupView from '@/views/profiles/SignupView.vue'
import LoginView from '@/views/profiles/LoginView.vue'
import ProfileView from '@/views/profiles/ProfileView.vue'
import PromoView from '@/views/profiles/PromoView.vue'
import SupportView from '@/views/support/SupportView.vue'
import AdminView from '@/views/admin/AdminView.vue'
import AdminSupportView from '@/views/admin/AdminSupportView.vue'
import AdminHomeView from '@/views/admin/AdminHomeView.vue'
import { noAuthMiddleware, authMiddleware } from './middleware/authMiddleware'
import { adminMiddleware } from './middleware/adminMiddleware'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/main/AboutView.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      beforeEnter: authMiddleware,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: authMiddleware,
    },
    {
      path: '/support',
      name: 'support',
      component: SupportView,
      beforeEnter: noAuthMiddleware,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      beforeEnter: noAuthMiddleware,
    },
    {
      path: '/promo',
      name: 'promo',
      component: PromoView,
      beforeEnter: noAuthMiddleware,
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      beforeEnter: adminMiddleware,
      children: [
        {
          path: '',
          name: 'admin-home',
          component: AdminHomeView
        },
        {
          path: 'support',
          name: 'admin-support',
          component: AdminSupportView
        },
        {
          path: 'users',
          name: 'admin-users',
          component: AdminHomeView
        },
        {
          path: 'blocked',
          name: 'admin-blocked',
          component: AdminHomeView
        },
        {
          path: 'roles',
          name: 'admin-roles',
          component: AdminHomeView
        },
        {
          path: 'posts',
          name: 'admin-posts',
          component: AdminHomeView
        },
        {
          path: 'promocodes',
          name: 'admin-promocodes',
          component: AdminHomeView
        },
        {
          path: 'stats/general',
          name: 'admin-stats-general',
          component: AdminHomeView
        },
        {
          path: 'stats/activity',
          name: 'admin-stats-activity',
          component: AdminHomeView
        },
        {
          path: 'stats/charts',
          name: 'admin-stats-charts',
          component: AdminHomeView
        },
        {
          path: 'settings',
          name: 'admin-settings',
          component: AdminHomeView
        },
      ]
    }
  ],
})

router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore()

    // Если маршрут требует админа
    if (to.meta.requiresAdmin) {
        if (!userStore.user.isAuthenticated) {
            next('/login')
            return
        }

        // Обновляем данные пользователя перед доступом
        await userStore.fetchUserInfo().catch(() => {
            console.warn("Не удалось обновить данные пользователя")
        })

        if (userStore.user.is_staff) {
            next()
        } else {
            next('/')
        }
    } else {
        next()
    }
})

export default router
