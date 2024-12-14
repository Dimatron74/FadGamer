import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/main/HomeView.vue'
import SignupView from '@/views/profiles/SignupView.vue'
import LoginView from '@/views/profiles/LoginView.vue'
import ProfileView from '@/views/profiles/ProfileView.vue'
import authMiddleware from './middleware/authMiddleware'

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
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      beforeEnter: authMiddleware,
    },
  ],
})

export default router
