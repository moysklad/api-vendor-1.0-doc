## SDK для виджетов

Для упрощения работы с протоколами виджетов и сервисами хост-окна можно использовать **JS Widget SDK**. 
Данный SDK дает удобный API для запросов (request/response) и событий хоста, скрывая работу с `messageId`/`correlationId` и обработку ошибок `InvalidMessageError`.

Ссылка на репозиторий SDK:

- GitHub: [https://github.com/moysklad/js-widget-sdk](https://github.com/moysklad/js-widget-sdk)

Подробности и актуальные примеры смотрите в README репозитория.

**Подключение**:

```html
<script src="https://cdn.jsdelivr.net/npm/@moysklad/js-widget-sdk/dist/widget.min.js"></script>
```

Варианты фиксации версии:

- с фиксацией мажорной версии: `https://cdn.jsdelivr.net/npm/@moysklad/js-widget-sdk@1/dist/widget.min.js`
- с фиксацией конкретной версии: `https://cdn.jsdelivr.net/npm/@moysklad/js-widget-sdk@1.0.0/dist/widget.min.js`

**Быстрый старт**:

```js
const sdk = WidgetSDK.create({ debug: true });

sdk.onOpen((message) => {
  console.log('Open', message);
});

sdk.showDialog('Учетная запись будет удалена. Вы хотите продолжить?', [
  { name: 'Yes', caption: 'Да, удалить' },
  { name: 'No', caption: 'Нет' }
]).then((response) => {
  console.log('Dialog response', response);
});
```

Параметр `debug` используйте только при разработке. В продакшене его следует отключать.

**Соответствие протоколам** (используйте только при наличии поддержки в дескрипторе):

- `openFeedback()` — **open-feedback**
- `setDirty()` / `clearDirty()` — **dirty-state**
- `onChange()` + `validationFeedback()` — **change-handler** + **validation-feedback**
- `update()` — **update-provider**
- `showPopup()` / `closePopup()` — **popups**
- `selectGoodFolder()` — **good-folder-selector**
- `showDialog()` — **standard-dialogs**
- `navigateTo()` — **navigation-service**
- `requestUserContextToken()` — **user-context**

SDK рассчитан на работу в браузерном окружении (iframe) и не предназначен для использования на сервере.
Поддерживаются последние версии браузеров: Яндекс.Браузер, Chrome, Opera, Firefox, Safari.

Более подробный пример использования SDK можно увидеть в [демо-решениях](#/getting-started/demo-solutions#2-demo-resheniya).
