import { createI18n } from 'vue-i18n';
import en from './en.json';
import ru from './ru.json';
import cn from './zh-CN.json';
import hi from './hi.json';

const messages = { en, ru, cn, hi };

const i18n = createI18n({
  locale: 'ru', // язык по умолчанию
  fallbackLocale: 'en', // язык на случай отсутствия перевода
  legacy: false,
  globalInjection: true,
  messages,
});

export default i18n;
