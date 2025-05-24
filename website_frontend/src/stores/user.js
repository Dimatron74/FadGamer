import axios from "axios"
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export const useUserStore = defineStore('user', () => {
    // State
    const user = ref({
        isAuthenticated: false,
        uid: null,
        name: null,
        email: null,
        refresh: null,
        access: null,
        is_staff: false,
    })

    const token = ref(localStorage.getItem('token') || null)

    // Methods

    async function initStore() {
        const access = localStorage.getItem('user.access')

        if (access) {
            user.value.access = access
            user.value.isAuthenticated = true
            user.value.uid = localStorage.getItem('user.uid')
            user.value.email = localStorage.getItem('user.email')
            user.value.name = localStorage.getItem('user.name')
            user.value.is_staff = JSON.parse(localStorage.getItem('user.is_staff') || 'false')
            user.value.refresh = localStorage.getItem('user.refresh')

            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access

            try {
                await refreshToken()
            } catch (e) {
                console.warn("Не удалось обновить токен")
            }
        } else {
            console.log('Пользователь не определён', user.value)
        }
    }

    function setToken(data) {
        user.value.access = data.access
        user.value.refresh = data.refresh
        user.value.isAuthenticated = true

        localStorage.setItem('user.access', data.access)
        localStorage.setItem('user.refresh', data.refresh)
    }

    function removeToken() {
        user.value.access = null
        user.value.refresh = null
        user.value.isAuthenticated = false
        user.value.uid = null
        user.value.email = null
        user.value.name = null
        user.value.is_staff = false

        const keys = Object.keys(localStorage)
        keys.forEach(key => {
            if (key.startsWith('user.')) {
                localStorage.removeItem(key)
            }
        })

        axios.defaults.headers.common['Authorization'] = ''
    }

    function setUserInfo(userInfo) {
        console.log('setUserInfo', userInfo)

        user.value.uid = userInfo.uid
        user.value.email = userInfo.email
        user.value.name = userInfo.name
        user.value.is_staff = Boolean(userInfo.is_staff)

        localStorage.setItem('user.uid', user.value.uid)
        localStorage.setItem('user.email', user.value.email)
        localStorage.setItem('user.name', user.value.name)
        localStorage.setItem('user.is_staff', user.value.is_staff)

        console.log('User: ', user.value)
    }

    async function refreshToken() {
        try {
            const res = await axios.post('/profiles/api/refresh/', {
                refresh: user.value.refresh
            })

            user.value.access = res.data.access
            localStorage.setItem('user.access', res.data.access)

            axios.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access

            return res.data.access // ✅ возвращаем новый токен
        } catch (err) {
            console.error(err)
            removeToken()
            throw err
        }
    }

    async function fetchUserInfo() {
        try {
            const res = await axios.get('/profiles/me/')
            setUserInfo(res.data)
            console.log('Обновленные данные пользователя:', res.data)
        } catch (err) {
            console.error('Ошибка при обновлении данных пользователя', err)
        }
    }

    // Computed-like через computed()
    const isAdmin = computed(() => user.value.is_staff)
    const isLoggedIn = computed(() => user.value.isAuthenticated)

    return {
        user,
        token,

        initStore,
        setToken,
        removeToken,
        setUserInfo,
        refreshToken,
        fetchUserInfo,

        isAdmin,
        isLoggedIn,
    }
})