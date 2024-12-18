<script setup>
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { vOnClickOutside } from '@vueuse/components'

// onMounted(() => {
//   document.querySelector('.more-button').addEventListener('click', function () {
//     document.querySelector('.list-container').classList.toggle('active');
//   });
// //   document.addEventListener('click', (event) => {
// //     const listContainer = document.querySelector('.list-container');
// //     if (!listContainer.contains(event.target)) {
// //       listContainer.classList.remove('active');
// //     }
// //   });
// });

const { t, locale } = useI18n(); 

// Функция для смены языка
function switchLanguage(event) {
  const target = event.target.closest('.more-button-list-item');
  let newLocale;
  if (target.dataset.lang === 'ru') {
    newLocale = 'ru';
  } else if (target.dataset.lang === 'en') {
    newLocale = 'en';
  } else if (target.dataset.lang === 'cn') {
    newLocale = 'cn';
  } else if (target.dataset.lang === 'hi') {
    newLocale = 'hi';
  }
  locale.value = newLocale;  // Меняем язык с помощью vue-i18n
  localStorage.setItem('lang', newLocale);  // Сохраняем выбранный язык в localStorage
  console.log('Язык изменён на', newLocale);
}


const ignoreElRef = ref()
const closeList = [
  (ev) => {
    isOpen.value = false
    ignoreElRef.value.blur();
  },
  { ignore: [ignoreElRef] },
]

const isOpen = ref(false);
function toggleList() {
  isOpen.value = !isOpen.value;
}
</script>

<template>
  <div class="list-container" :class="{'active': isOpen}">
    <button class="more-button" aria-label="Menu Button" @click="toggleList" ref="ignoreElRef">
      <!-- <div class="menu-icon-wrapper">
        <div class="menu-icon-line half first"></div>
        <div class="menu-icon-line"></div>
        <div class="menu-icon-line half last"></div>
      </div> -->
      <svg width="40.296265" height="40.000000" viewBox="0 0 40.2963 40" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <circle cx="20.14815" cy="20" r="18" fill="#CCCCCC"/>
        <defs/>
        <path id="Vector" d="M20.14 0C9.01 0 0 8.95 0 20C0 31.04 9.01 40 20.14 40C31.27 40 40.29 31.04 40.29 20C40.29 8.95 31.27 0 20.14 0ZM34.77 22.12L33.16 21.33C32.82 21.19 32.53 20.95 32.33 20.65L30.91 18.54C30.49 17.91 30.49 17.09 30.91 16.46L32.46 14.16C32.64 13.89 32.89 13.67 33.18 13.52C33.72 13.26 34.3 13.1 34.9 13C35.92 15.12 36.51 17.49 36.51 20C36.51 20.98 36.41 21.94 36.24 22.88L34.77 22.12ZM13.81 5.01L14.55 5.71C14.92 6.07 15.34 6.36 15.81 6.59C16.08 6.73 16.41 6.76 16.71 6.67C17.26 6.51 17.63 6.01 17.62 5.44C17.63 4.94 18 4.52 18.5 4.47C18.7 4.45 18.9 4.44 19.1 4.42C19.38 4.41 19.65 4.51 19.85 4.71L21.77 6.61C22.26 7.1 22.26 7.89 21.77 8.38L20.59 9.55C20.34 9.8 20.34 10.19 20.59 10.44L20.96 10.8C21.2 11.05 21.2 11.44 20.96 11.69L20.33 12.31C20.21 12.43 20.05 12.5 19.88 12.5L19.18 12.5C19.01 12.5 18.85 12.57 18.73 12.67L17.96 13.43C17.76 13.62 17.71 13.92 17.83 14.16L19.06 16.6C19.1 16.68 19.13 16.78 19.13 16.88C19.13 17.22 18.85 17.5 18.5 17.5L18.05 17.5C17.9 17.5 17.75 17.45 17.64 17.35L16.91 16.71C16.57 16.42 16.11 16.33 15.68 16.47L13.23 17.28C13 17.36 12.81 17.53 12.7 17.74C12.46 18.2 12.64 18.77 13.11 19L13.98 19.44C14.72 19.8 15.54 20 16.37 20C17.19 20 18.14 22.13 18.88 22.5L24.14 22.5C24.81 22.49 25.45 22.76 25.92 23.23L27 24.29C27.45 24.74 27.7 25.35 27.7 25.98C27.7 26.95 27.31 27.88 26.62 28.56C26.31 28.86 25.99 29.18 25.73 29.44C25.5 29.67 25.33 29.96 25.24 30.28C25.12 30.72 25.02 31.16 24.87 31.59L23.75 34.85C23.6 35.48 23.08 35.95 22.44 36.07C22.33 36.08 22.22 36.1 22.11 36.12C22.07 36.12 22.03 36.13 21.99 36.13C21.93 36.14 21.86 36.14 21.8 36.14C20.88 36.14 20.14 35.41 20.14 34.57L20.14 33.55C20.28 32.57 19.54 30.72 18.36 29.55C17.89 29.01 17.55 28.37 17.62 27.71L17.62 25.21C17.63 24.3 17.13 23.47 16.33 23.03C15.2 22.41 13.59 21.54 12.49 20.99C11.59 20.53 10.75 19.96 10 19.28L9.94 19.23C9.4 18.75 8.92 18.2 8.51 17.6C7.94 16.77 6.63 14.84 5.71 13.49C5.58 13.31 5.52 13.1 5.43 12.92C7.16 9.38 10.14 6.55 13.81 5.01Z" fill="#383B40" fill-opacity="1.000000" fill-rule="nonzero"/>
      </svg>
    </button>
    <ul class="more-button-list" v-on-click-outside="closeList">
      <li class="more-button-list-item" @click="switchLanguage" data-lang="ru">
        <span>Русский</span>
      </li>
      <li class="more-button-list-item" @click="switchLanguage" data-lang="en">
        <span>English</span>
      </li>
      <li class="more-button-list-item" @click="switchLanguage" data-lang="cn">
        <span>中文</span>
      </li>
      <li class="more-button-list-item" @click="switchLanguage" data-lang="hi">
        <span>हिन्दी</span>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>

* { box-sizing: border-box; }

$body-bg: red;
$button-bg: black;
$list-bg: #222326;
$text-color: #E6E6E6;
$text-color-hover: #FFFFFF;
$menu-icon-transition: transform 300ms cubic-bezier(0.52, -0.80, 0.52, 0.52);

.list-container {
  position: absolute;
  
  &.active {
    .more-button-list {
       opacity: 1;
       transform: scale(1);
    }
    
    .more-button-list-item {
      animation: fadeInItem .6s .2s forwards;
      
      &:nth-child(2) { animation-delay: .4s; }
      &:nth-child(3) { animation-delay: .6s; }
      &:nth-child(4) { animation-delay: .8s; }
    }
    
    .more-button {
      animation: onePulse .6s forwards linear;
    }
    
    .menu-icon-wrapper {
      transform: rotate(-45deg);
    }
    
    .menu-icon-line {
      &.first {
        transform: rotate(-90deg) translateX(1px);
      }
      
      &.last {
        transform: rotate(-90deg) translateX(-1px);
      }
    }
  }
}

.more-button {
  box-shadow: 0px 0px 0px 4px #333333;
  border-radius: 50%;
  width: 100%;
  height: 100%;
  padding: 10px;
  border: none;
  cursor: pointer;
  transition: .2s ease-in;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 2;
  
  &:hover {
    box-shadow: 0px 0px 0px 8px rgba(218, 0, 55, 0.16);
  }
  
  &:focus { outline: 0; }
  
  &-list {
    background-color: $list-bg;
    border-radius: 8px;
    list-style-type: none;
    width: 140px;
    height: 170px;
    box-shadow: 0px 0px 4px 4px rgba(218, 0, 55, 0.16);
    padding: 0;
    padding: 6px;
    position: absolute;
    right: 45px;
    bottom: 35px;
    opacity: 0;
    transform: scale(0);
    transform-origin: bottom right;
    transition : all .3s ease .1s;
    
    li { opacity: 0; }
  }
  
  &-list-item {
    display: flex;
    align-items: center;
    color: $text-color;
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    position: relative;
    transition: .2s ease-in;
    transform: translatex(-10px);
    
    &:hover { color: $text-color-hover; }
    
    &:after {
      content: '';
      position: absolute;
      height: 1px;
      width: calc(100% - 24px);
      left: 12px;
      bottom: 0;
      background-color: rgba(218, 0, 55, 0.1);
    }
    &:last-child:after { display: none; }
    
    svg {
      width: 18px;
      height: 18px;
    }
    
    span {
      display: inline-block;
      line-height: 20px;
      font-size: 14px;
      margin-left: 8px;
    }
  }
}

@keyframes onePulse {
  0% {
    box-shadow: 0px 0px 0px 0px rgba(218, 0, 55, 0.3);
  }
  
  50% {
    box-shadow: 0px 0px 0px 12px rgba(218, 0, 55, 0.1)
  }
  
  100% {
    box-shadow: 0px 0px 0px 4px rgba(218, 0, 55, 0.16);
  }
}

@keyframes fadeInItem {
  100% {
    transform: translatex(0px);
    opacity: 1;
  }
}

.menu-icon-wrapper {
  border-radius: 2px;
  width: 20px;
  height: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: transform 330ms ease-out;
}

.menu-icon-line {
  background-color: #fff;
  border-radius: 2px;
  width: 100%;
  height: 2px;
  
  &.half { width: 50%;}
  
  &.first {
    transition: $menu-icon-transition;
    transform-origin: right;
  }
  
  &.last {
    align-self: flex-end;
    transition: $menu-icon-transition;
    transform-origin: left;
  }
}
</style>

