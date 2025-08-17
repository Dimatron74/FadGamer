import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import HomeView from '@/views/main/HomeView.vue'
import SignupView from '@/views/profiles/SignupView.vue'
import LoginView from '@/views/profiles/LoginView.vue'
import ProfileView from '@/views/profiles/ProfileView.vue'
import SupportView from '@/views/support/SupportView.vue'
import SupportDetailView from '@/views/support/SupportDetailView.vue'
import NewTicketView from '@/views/support/NewTicketView.vue'
import AdminView from '@/views/admin/AdminView.vue'
import AdminSupportView from '@/views/admin/AdminSupportView.vue'
import AdminHomeView from '@/views/admin/AdminHomeView.vue'
import AdminSupportDetailView from '@/views/admin/AdminSupportDetailView.vue'
import AdminPromoCodesCreateView from '@/views/admin/AdminPromoCodesCreateView.vue'
import PromoCodeModal from '@/components/admin/PromoCodeModal.vue'
import AdminPromoCodesView from '@/views/admin/AdminPromoCodesView.vue'
import GamesView from '@/views/games/GamesView.vue'
import GameDetailView from '@/views/games/GameDetailView.vue'
import NewsListView from '@/views/news/NewsListView.vue'
import NewsDetailView from '@/views/news/NewsDetailView.vue'
import AdminNewsCreateView from '@/views/admin/AdminNewsCreateView.vue'
import AdminNewsEditView from '@/views/admin/AdminNewsEditView.vue'
import AdminNewsListView from '@/views/admin/AdminNewsListView.vue'
import AdminContactView from '@/views/admin/AdminContactView.vue'
import AdminContactDetailView from '@/views/admin/AdminContactDetailView.vue'

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
      path: '/profile/support',
      name: 'user-support',
      component: SupportView,
    },
    {
      path: '/profile/support/:id',
      name: 'user-support-detail',
      component: SupportDetailView,
    },
    {
      path: '/profile/support/new',
      name: 'user-support-new',
      component: NewTicketView,
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
        {
          path: 'support/:id',
          name: 'admin-support-detail',
          component: AdminSupportDetailView
        },
        {
          path: 'promocodes',
          name: 'admin-promocodes',
          component: AdminPromoCodesView
        },
        {
          path: 'promocodes/create',
          name: 'admin-promocodes-create',
          component: AdminPromoCodesCreateView
        },
        {
          path: 'promocodes/:code',
          name: 'admin-promocode-detail',
          component: PromoCodeModal
        },
        {
          path: 'news/create',
          name: 'admin-news-create',
          component: AdminNewsCreateView
        },
        {
          path: 'news/:slug/edit',
          name: 'admin-news-edit',
          component: AdminNewsEditView
        },
        {
          path: 'news',
          name: 'admin-news-list',
          component: AdminNewsListView,
        },
        {
          path: 'contacts',
          name: 'admin-contacts',
          component: AdminContactView,
        },
        {
          path: 'contacts/:id',
          name: 'admin-contacts-detail',
          component: AdminContactDetailView
        },
      ]
    },
    {
      path: '/games',
      name: 'games',
      component: GamesView
    },
    {
      path: '/games/:slug',
      name: 'game-detail',
      component: GameDetailView
    },
    {
      path: '/news',
      name: 'news-list',
      component: NewsListView
    },
    {
      path: '/news/:slug',
      name: 'news-detail',
      component: NewsDetailView
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    // Если есть сохранённая позиция (например, при "назад"), вернём её
    if (savedPosition) {
      return savedPosition
    } else {
      // Всегда скроллим в самый верх при обычной навигации
      return { left: 0, top: 0 }
    }
  }
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
