## Список последних изменений

### 11-09-2023
#### Добавлено
- В тело запроса при [активации приложения на аккаунте](#aktiwaciq-prilozheniq-na-akkaunte) добавлена информация о новой причине актвации — смена тарифа (`"cause": "TariffChanged"`).

### 06-09-2023
#### Добавлено
- В тело запроса при [активации приложения на аккаунте](#aktiwaciq-prilozheniq-na-akkaunte) добавлена информация о подписке (атрибут `subscription`).

### 30-08-2023
#### Изменено
- Базовый URL REST-эндпоинтов vendor API (`MARKETPLACE-ENDPOINT`) сменился на [https://apps-api.moysklad.ru/api/vendor/1.0](https://apps-api.moysklad.ru/api/vendor/1.0).
- Для запросов к vendor API необходимо использовать сжатие (заголовок `Accept-Encoding`)
- URL личного кабинета разработчика сменился на [https://apps.moysklad.ru/cabinet](https://apps.moysklad.ru/cabinet).

### 23-11-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Розничном возврате, Внесении и Выплате денег.
- Поддержка дополнительного поля типа справочник [[Товар]](https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-rabota-s-dopolnitel-nymi-polqmi) в протоколе [change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta).

### 18-11-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Розничной продаже.

### 09-11-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Возврате покупателя.

### 12-10-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Списании и Счете покупателю.

### 06-09-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Счете поставщика.

### 23-08-2022
#### Изменено
- Прекращена поддержка [типа приложений](#tipy-prilozhenij-dlq-magazina-prilozhenij) iframe.
 
### 01-08-2022
#### Добавлено
- Поддержка накладных расходов (поле `overhead`) в протоколе update-provider в
  [Отгрузке](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-otgruzka),
  [Перемещении](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-peremeschenie) и
  [Оприходовании](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-oprihodowanie).

### 26-07-2022
#### Добавлено
- Поддержка накладных расходов (поле `overhead`) в протоколе update-provider в [Приемке](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka).

### 22-07-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Отгрузке, Перемещении и Оприходовании.

### 07-07-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Счете покупателю.

### 04-07-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Приемке.

### 20-05-2022
#### Добавлено
- Поддержка полей `incomingDate` и `incomingNumber` для протокола change-handler в [Приемке](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka).

### 20-04-2022
#### Изменено
- Требования к [иконкам приложений](#trebowaniq-k-ikonkam-prilozhenij).

### 04-03-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Поддержка [протокола навигации](#protokol-nawigacii) (`<navigation-service/>`) в главном iframe приложения и модальных окнах.  

### 27-01-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Гибкие права приложений](#blok-access) — поддержка права видеть себестоимость, цену закупки и прибыль товаров <viewProductCostAndProfit/>.

### 21-01-2022
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Товаре, Модификации, Услуге, Комплекте, Группе товаров. 

### 21-12-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) на странице создания в Перемещении, Списании и Оприходовании. Поддержка протокола валидации на страницах создания и редактирования Перемещения, Списания и Оприходования.

### 16-12-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) на странице создания в Приемке и Отгрузке. Поддержка протокола валидации на страницах создания и редактирования Приемки и Отгрузки.

### 10-12-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Перемещении, Списании и Оприходовании.

### 29-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Приемке.

### 24-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) на странице создания в Заказе покупателя. Поддержка протокола валидации при создании Заказа покупателя.

### 19-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Поддержка протокола валидации при редактировании Заказа покупателя.

### 17-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Поддержка [селектора групп товаров](#selektor-gruppy-towarow) (`<good-folder-selector/>`) в главном iframe приложения и модальных окнах.

### 11-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Отгрузке.

### 01-11-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Заказе покупателя.

### 21-10-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Протокол навигации](#protokol-nawigacii) в виджетах.

### 07-10-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Возвратах покупателя и в Возвратах поставщику.

### 16-09-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Перемещении, Списании, Оприходовании, Внутреннем заказе, Инвентаризации.

### 30-08-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Гибкие права приложений](#blok-access).

### 10-08-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Стандартные диалоги.

### 13-05-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Заказе покупателя.

### 21-01-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Розничной продаже, Входящем и Исходящем платеже, Приходном и Расходном ордере.

### 13-01-2021
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Кастомные модальные окна](#kastomnye-popapy-modal-nye-okna) в виджетах.

### 04-12-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Счете поставщика, Заказе поставщику, Заказе на производство, Приемке.

### 30-11-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) с поддержкой протокола dirty-state.

### 13-11-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) с поддержкой протокола save-handler.

### 10-11-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в новой карточке Контрагента.

### 09-11-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Счете покупателю.

### 22-10-2020
#### Добавлено
- [VendorApi 1.0](#vendor-api-1-0):
  Новый эндпоинт на стороне МоегоСклада: [Получение статуса приложения на аккаунте](#poluchenie-statusa-prilozheniq-na-akkaunte).

### 08-10-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) с поддержкой селектора групп товаров.

### 22-09-2020
#### Изменено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в Заказе покупателя и Отгрузке.

### 18-08-2020
#### Добавлено
- Версия 2 [дескриптора приложений](#deskriptor-prilozheniq):
  [Виджеты](#vidzhety) в карточке контрагента.
