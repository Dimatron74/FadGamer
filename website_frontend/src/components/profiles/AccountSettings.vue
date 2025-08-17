<!-- components/profiles/AccountSettings.vue -->
<template>
  <div class="space-y-3">
    <!-- Заголовок секции -->
    <div class="px-4">
      <h2 class="text-xl font-semibold text-mywhite-5 mb-1">Общие данные</h2>
      <p class="text-sm text-mywhite-2">Основные данные о вашем аккаунте</p>
    </div>

    <!-- Подраздел: Личные данные -->
    <div class="bg-myblack-3 p-6 rounded-lg shadow-md border border-myblack-3 ">
      <NicknameEdit />
      <EmailEdit />
      <PhoneEdit />
      <BirthDateEdit />
    </div>

    <!-- Заголовок секции -->
    <div class="px-4">
      <h2 class="text-xl font-semibold text-mywhite-5 mb-1">Безопасность</h2>
      <p class="text-sm text-mywhite-2">Изменение пароля и другие меры безопасности</p>
    </div>

    <!-- Подраздел: Безопасность -->
    <div class="bg-myblack-3 p-6 rounded-lg shadow-md border border-myblack-3">
      <PasswordEdit />
    </div>

    <!-- Заголовок секции -->
    <div class="px-4">
      <h2 class="text-xl font-semibold text-mywhite-5 mb-1">Настройки уведомлений</h2>
      <p class="text-sm text-mywhite-2">Выберите тип получаемых уведомлений</p>
    </div>

    <!-- Подраздел: Уведомления -->
    <div class="bg-myblack-3 p-6 rounded-lg shadow-md border border-myblack-3">
      <NotificationEdit />
    </div>
  </div>
</template>

<script setup>
import EmailEdit from './EmailEdit.vue'
import PasswordEdit from './PasswordEdit.vue'
import NicknameEdit from './NicknameEdit.vue'
import PhoneEdit from './PhoneEdit.vue'
import BirthDateEdit from './BirthDateEdit.vue'
import NotificationEdit from './NotificationEdit.vue'
</script>