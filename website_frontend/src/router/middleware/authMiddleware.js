import { useUserStore } from '@/stores/user'

export function noAuthMiddleware(to, from, next) {
  const userStore = useUserStore()
  if (!userStore.user.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
}

export function authMiddleware(to, from, next) {
  const userStore = useUserStore()
  if (userStore.user.isAuthenticated) {
    next({ name: 'profile' })
  } else {
    next()
  }
}
