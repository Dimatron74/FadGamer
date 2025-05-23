import axios from "axios"
import { defineStore } from 'pinia'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export const useUserStore = defineStore({
    id: "user",
    state: () => ({
        user: {
            isAuthenticated: false,
            uid: null,
            name: null,
            email: null,
            refresh: null,
            access: null,
        },
        token: localStorage.getItem('token')
    }),
    actions: {
        initStore() {
            if (localStorage.getItem('user.access')) {
                this.user.access = localStorage.getItem('user.access')
                this.user.isAuthenticated = true
                this.user.uid = localStorage.getItem('user.uid')
                this.user.email = localStorage.getItem('user.email')   
                this.user.name = localStorage.getItem('user.name')
                this.user.refresh = localStorage.getItem('user.refresh')  
                
                this.refreshToken()

                console.log('Initialize user: ', this.user)
            } else {
                console.log('Пользователь не определён', this.user)
            }
        },

        setToken(data) {
            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', this.user.access)
            localStorage.setItem('user.refresh', this.user.refresh)
        },

        removeToken() {
            this.user.access = null
            this.user.refresh = null
            this.user.isAuthenticated = false
            this.user.uid = null
            this.user.email = null
            this.user.name = null

            // Очистка кеша
            const keys = Object.keys(localStorage)
            keys.forEach(key => {
                if (key.startsWith('user.')) {
                localStorage.removeItem(key)
                }
            })

            axios.defaults.headers.common['Authorization'] = ''
        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.uid = user.uid
            this.user.email = user.email
            this.user.name = user.name

            localStorage.setItem('user.uid', this.user.uid)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.name', this.user.name)

            console.log('User: ', this.user)
        },

        refreshToken() {
            axios.post('/profiles/api/refresh/', {
                refresh: this.user.refresh
            }).then(res => {
                console.log('Токен рефреш', this.user.refresh)
                console.log('Токен доступ', this.user.access)
                this.user.access = res.data.access

                localStorage.setItem('user.access', res.data.access)

                axios.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access
            }).catch(err => {
                console.log(err)

                this.removeToken()
            })
        },
    }  
})