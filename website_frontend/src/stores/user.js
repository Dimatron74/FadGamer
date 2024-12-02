import axios from "axios"
import { defineStore } from 'pinia'

axios.defaults.baseURL = 'http://127.0.0.1:8000'

export const useUserStore = defineStore({
    id: "user",
    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
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
                this.user.id = localStorage.getItem('user.id')
                this.user.email = localStorage.getItem('user.email')   
                this.user.name = localStorage.getItem('user.name')
                this.user.refresh = localStorage.getItem('user.refresh')  
                
                this.refreshToken()

                console.log('Initialize user: ', this.user)
            } else {
                console.log('Тут пусто походу', this.user)
            }
        },

        setToken(data) {
            console.log('setToken', data)
            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', this.user.access)
            localStorage.setItem('user.refresh', this.user.refresh)
        },

        removeToken() {
            console.log('removeToken')

            this.user.access = null
            this.user.refresh = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.email = null
            this.user.name = null

            localStorage.removeItem('user.access')
            localStorage.removeItem('user.refresh')
            localStorage.removeItem('user.id')
            localStorage.removeItem('user.email')
            localStorage.removeItem('user.name')
        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.id = user.id
            this.user.email = user.email
            this.user.name = user.name

            localStorage.setItem('user.id', this.user.id)
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