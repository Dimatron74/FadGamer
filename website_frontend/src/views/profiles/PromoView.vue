<template>
  <div class="container mx-auto grid grid-cols-2 gap-4 p-4">
    <div class="bg-white rounded-lg shadow-lg p-4">
      <div class="text-3xl font-bold mb-4">Активация промокода</div>

      <div class="flex flex-col space-y-4">
        <div class="flex items-center">
          <label class="w-1/3 text-gray-700" for="promo">Промокод:</label>
          <input id="promo" type="text" class="border border-gray-400 rounded p-2 w-full">
        </div>

        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Активировать
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-4">
      <div class="text-3xl font-bold mb-4">Справка</div>

      <div class="space-y-4 text-gray-700">
        <p>Вас приветствует сервис FAD GAMERS. Мы рады, что вы заинтересовались нашей компанией.</p>
        <p>Введённый вами промокод будет активирован при нажатии кнопки "Активировать".</p>
        <p>Если у вас возникли вопросы, пожалуйста, <a href="https://www.youtube.com/c/FadGamer/" target="_blank" rel="noopener" class="text-blue-500 hover:text-blue-700 underline">напишите нам</a>.</p>
      </div>
    </div>
  </div>
</template>
