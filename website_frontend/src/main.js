import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueCookies from 'vue-cookies'
import VueScrollTo from 'vue-scrollto'
import i18n from '@/components/locales/i18n.js'



// шрифты
import '@/assets/fonts/Roboto-Regular.ttf'
import '@/assets/fonts/Roboto-Bold.ttf'



const app = createApp(App)

app.use(VueCookies)
app.use(createPinia())
app.use(i18n)
app.provide('i18n', i18n)
app.use(router, axios)
app.directive('scroll-to', VueScrollTo)

app.mount('#app')


axios.defaults.headers.common['X-CSRFToken'] = VueCookies.get('csrftoken');



axios.defaults.baseURL = "http://127.0.0.1:8000"