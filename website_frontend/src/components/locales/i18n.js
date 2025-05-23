import { createI18n } from 'vue-i18n';
import en from './en.json';
import ru from './ru.json';
import cn from './zh-CN.json';
import hi from './hi.json';

const messages = { en, ru, cn, hi };

const i18n = createI18n({
  locale: 'en', // язык по умолчанию
  fallbackLocale: 'ru', // язык на случай отсутствия перевода
  legacy: false,
  globalInjection: true,
  messages,
});

export default i18n;
