<!-- components/profiles/AccountSettings.vue -->
<template>
  <div class="space-y-6">
    <EmailEdit />
    <PasswordEdit />
    <NicknameEdit />
    <PhoneEdit />
    <BirthDateEdit />
  </div>
</template>

<script setup>
import EmailEdit from './EmailEdit.vue'
import PasswordEdit from './PasswordEdit.vue'
import NicknameEdit from './NicknameEdit.vue'
import PhoneEdit from './PhoneEdit.vue'
import BirthDateEdit from './BirthDateEdit.vue'
</script>