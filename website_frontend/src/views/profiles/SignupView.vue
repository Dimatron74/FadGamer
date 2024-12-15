<template>
    <div class="container mx-auto p-4">
        <div class="flex justify-center">
            <div class="w-1/2 bg-myblack-3 rounded-lg shadow-lg p-4">
                <div class="text-3xl font-bold mb-4">Регистрация</div>

                <form v-on:submit.prevent="submitForm" class="space-y-4">
                    <div class="flex flex-col">
                        <label for="name" class="">Никнейм</label>

                        <input id="name" type="text" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="form.name" required autofocus>
                    </div>

                    <div class="flex flex-col">
                        <label for="email" class="">Email</label>

                        <input id="email" type="email" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="form.email" required>
                    </div>

                    <div class="flex flex-col">
                        <label for="password" class="">Пароль</label>

                        <input id="password" type="password" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="form.password" required>
                    </div>

                    <div class="flex flex-col">
                        <label for="password_confirm" class="">Повторите пароль</label>

                        <input id="password_confirm" type="password" class="border-2 bg-myblack-2 border-myblack-4 text-mywhite-3 rounded p-2 w-full focus:border-myblack-5 transition duration-300 outline-none" v-model="form.password_confirm" required>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>
                    </template>

                    <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Зарегистироваться
                    </button>
                </form>
            </div>
        </div>
    </div>

</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            form: {
                name: '',
                email: '',
                password: '',
                password_confirm: '',
            },
            errors: [],
        }
    },

    methods: {
    submitForm() {
        this.errors = []
        if (this.form.name === '') {
        this.errors.push('Name is required')
        }

        if (this.form.email === '') {
        this.errors.push('Email is required')
        }

        if (this.form.password === '') {
        this.errors.push('Password is required')
        }

        if (this.form.password !== this.form.password_confirm) {
        this.errors.push('Passwords do not match')
        }

        if (this.errors.length === 0) {
        axios
            .post('/profiles/signup/', this.form)
            .then(res => {
            if (res.data.message === 'success') {
                // this.toastStore.showToast(5000, 'Registration successful', 'bg-green-500')

                this.form.email = ''
                this.form.name = ''
                this.form.password = ''
                this.form.password_confirm = ''

                this.$router.push('/login')
            } else {
                // this.toastStore.showToast(5000, 'Registration failed', 'bg-red-500')
                console.log('error form')
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

