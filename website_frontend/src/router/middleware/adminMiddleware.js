// src/router/middleware/adminMiddleware.js

import { useUserStore } from '@/stores/user'

export const adminMiddleware = async (to, from, next) => {
    const userStore = useUserStore()

    if (!userStore.user.isAuthenticated) {
        return next('/login')
    }

    try {
        // Обновляем данные пользователя
        await userStore.fetchUserInfo()
    } catch (e) {
        console.warn('Не удалось обновить данные пользователя', e)
    }

    // Проверяем права
    if (userStore.user.is_staff !== true) {
        return next('/')
    }

    return next()
}