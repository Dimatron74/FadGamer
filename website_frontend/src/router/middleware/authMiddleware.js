import { useUserStore } from '@/stores/user'

export default function authMiddleware(to, from, next) {
  const userStore = useUserStore()
  if (!userStore.user.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
}