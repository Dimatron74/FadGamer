<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from '../icons/IconDocumentation.vue'
import ToolingIcon from '../icons/IconTooling.vue'
import EcosystemIcon from '../icons/IconEcosystem.vue'
import CommunityIcon from '../icons/IconCommunity.vue'
import SupportIcon from '../icons/IconSupport.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>Документация</template>

    <p>
      Здесь вы можете найти информацию о том, как работает наша студия, как мы создаем игры, как мы общаемся между собой
    </p>

  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <ToolingIcon />
    </template>
    <template #heading>Инструменты</template>

    <p>
      Мы используем
      <a href="https://www.blender.org/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Blender</a>,
      <a href="https://unity.com/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Godot</a>,
      <a href="https://pixso.net" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Pixso</a>,
      и 
      <a href="https://code.visualstudio.com/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">VSCode</a>
    </p>
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <EcosystemIcon />
    </template>
    <template #heading>Экосистема</template>

    <p>
      Мы используем
      <a href="https://pinia.vuejs.org/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Pinia</a>,
      <a href="https://router.vuejs.org/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Vue Router</a>,
      <a href="https://test-utils.vuejs.org/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Vue Test Utils</a>,
      <a href="https://github.com/vuejs/devtools" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Vue Dev Tools</a>
    </p>

  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>Сообщество</template>

    <p>
      Если у вас есть вопросы, вы можете задать их на
      <a href="https://www.youtube.com/c/FadGamer/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">нашем YouTube канале</a>,
      <a href="https://vk.com/fadgamer" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">группе VK</a>,
      <a href="https://discord.gg/4PZ4S6rS" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">Telegram</a>
      или
      <a href="https://www.twitch.tv/fadgamer" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">BiliBili</a>
    </p>
  </WelcomeItem>

  <WelcomeItem v-if="userStore.user.access">
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Вы авторизированы!</template>

    Вы действительно авторизированы. Приветствуем вас, {{ userStore.user.name }},
    <a href="https://vuejs.org/sponsor/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">поэтому станьте ближе к нам</a>!
  </WelcomeItem>
  <WelcomeItem v-else>
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Войдите в систему</template>

    <RouterLink to="/login" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Авторизоваться</RouterLink>
  </WelcomeItem>
</template>
