<template>
  <div class="flex justify-center">
    <div class="w-1/2 bg-white rounded-lg shadow-lg p-4">
      <div class="text-3xl font-bold mb-4">Авторизация</div>

      <form @submit.prevent="submitForm" class="space-y-4">
        <div class="flex flex-col">
          <label for="email" class="text-gray-700">Email</label>

          <input id="email" type="email" class="border border-gray-400 rounded p-2 w-full" v-model="form.email" required>
        </div>

        <div class="flex flex-col">
          <label for="password" class="text-gray-700">Пароль</label>

          <input id="password" type="password" class="border border-gray-400 rounded p-2 w-full" v-model="form.password" required>
        </div>

        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Авторизоваться
        </button>
      </form>

      <div class="mt-4 text-center">
        <RouterLink to="/signup" class="text-blue-500 hover:text-blue-700 underline">
          У вас ещё нет аккаунта? Зарегистрироваться
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'


export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: [],
        }
    },
    methods: {
        async submitForm() {
            this.errors = []
            if (this.form.email === '') {
                this.errors.push('Email is required')
            }

            if (this.form.password === '') {
                this.errors.push('Password is required')
            }

            if (this.errors.length === 0) {
                console.log('Форма ', this.form)
                await axios
                    .post('/profiles/login/', this.form)
                    .then(res => {
                      console.log("Токен из апи", res.data)
                      const refreshToken = res.data.refresh;
                      const accessToken = res.data.access;
                      // console.log(refreshToken, accessToken);
                      this.userStore.setToken({ access: accessToken, refresh: refreshToken });
                      axios.defaults.headers.common['Authorization'] = 'Bearer ' + accessToken;
                    })
                    .catch(err => {
                    console.log('error', err)
                    })

                await axios
                    .get('/profiles/me/')
                    .then(res => {
                        console.log('Пользователь', res.data)
                        if (this.userStore.user.isAuthenticated) {
                          this.userStore.setUserInfo(res.data)
                          this.$router.push('/')
                        }
                    })
                    .catch(err => {
                    console.log('error', err)
                    })
                }
            }
    }
}
</script>
