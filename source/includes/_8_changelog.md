## Список последних изменений

### XX-04-2025
#### Изменено
- Массовые операции теперь работают на всех страницах где поддерживаются [кастомные кнопки](#kastomnye-knopki)

### 07-04-2025
#### Добавлено
- В эндпоинт [запроса обработки нажатия на кнопку](#obrabotka-nazhatiq-na-kastomnuu-knopku) добавлена возможность открытия кастомного модального окна (`action=ShowPopup`).
- В [кастомные кнопки](#kastomnye-knopki) в списках добавлена возможность отправки более 100 позиций.

### 01-04-2025
#### Добавлено
- В эндпоинт [получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte) в теле ответа добавлено поле access.

### 10-03-2025
#### Добавлено
- В [дескриптор решений](#deskriptor-resheniq) добавлены новые точки встраивания кастомных кнопок: `document.customerorder.list`, `document.demand.list`, `document.purchaseorder.list`.

### 17-02-2025
#### Добавлено
- В [REST-эндпоинты на стороне МоегоСклада](#rest-andpointy-na-storone-moegosklada) добавлен новый эндпоинт для [частичного изменения настроек лояльности](#chastichnoe-izmenenie-nastroek-loql-nosti).

### 10-02-2025
#### Добавлено
- В [дескриптор решений](#deskriptor-resheniq) добавлены новые точки встраивания кастомных кнопок: список Платежей (`document.finance.list`).

### 28-01-2025
#### Добавлено
- В [дескриптор решений](#deskriptor-resheniq) добавлены новые точки встраивания кастомных кнопок: список Контрагентов (`entity.counterparty.list`).

### 27-01-2025
#### Добавлено
- В личном кабинете добавлена вкладка для [просмотра истории модерации](#prosmotr-istorii-moderacii).

### 21-01-2025
#### Добавлено
- Отправка события `TariffChanged` при [продлении пробного периода](#prodlenie-probnogo-perioda).

### 11-12-2024
#### Добавлено
- В [дескрипторе решений](#deskriptor-resheniq) добавлена возможность указания прав для работы с дополнительными полями: `useOwnAttributeMetadata` и `useAllAttributeMetadata`.

### 09-12-2024
#### Добавлено
- Поддержка [встраивания видео в инструкции](#vstraiwanie-wideo-w-instrukcii).

### 03-12-2024
#### Добавлено
- В [дескриптор решений](#deskriptor-resheniq) добавлены новые точки встраивания кнопок: карточки Товара, Услуги, Комплекта, Модификации и Группы товаров.

### 21-11-2024
#### Добавлено
- В [дескриптор решений](#deskriptor-resheniq) добавлены новые точки встраивания кнопок: документы Отгрузка, Счет покупателю, Заказ поставщику, Розничная продажа и карточка Контрагента.

### 11-11-2024
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Поддержка [кастомных кнопок](#kastomnye-knopki) (`<buttons>`).

### 30-10-2024
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Поддержка [стандартных диалогов](#standartnye-dialogi) (`<standard-dialogs/>`) в главном iframe решения и модальных окнах.

### 09-10-2024
#### Добавлено
- В [дескрипторе решений](#deskriptor-resheniq) добавлена возможность указания прав для работы с веб-хуками: `useOwnWebhooks` и `useAllWebhooks`.

### 20-08-2024
#### Добавлено
- В тело запроса при [Активация решения на аккаунте](#rest-andpointy-na-storone-razrabotchika-reshenij) добавлен атрибут `subscription.partner`.
- В тело ответа при [Получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte) добавлен атрибут `subscription.partner`.

### 08-08-2024
#### Добавлено
- В URL запроса [Получение контекста пользователя для решений с iframe-частью, кастомными модальными окнами и виджетами](#poluchenie-kontexta-pol-zowatelq-dlq-reshenij-s-iframe-chast-u-kastomnymi-modal-nymi-oknami-i-widzhetami) добавлены новые параметры: appUid и appId.

### 08-05-2024
#### Добавлено
- В [дескрипторе решений](#deskriptor-resheniq) добавлена возможность указания блока `loyaltyApi`.

### 06-05-2024
#### Добавлено
- В тело запроса при [Активация решения на аккаунте](#rest-andpointy-na-storone-razrabotchika-reshenij) добавлена новая причина активации (`"cause": "Autoprolongation"`).

### 23-04-2024
#### Изменено
- Прекращена поддержка дескрипторов версий 1.x.x.

### 02-04-2024
#### Добавлено
- Возможность получения [шаблонов](#osobennosti-dostupa-k-nekotorym-funkciqm-json-api-1-2) документов по токену решения.

### 07-03-2024
#### Добавлено
- В тело запроса при [Активация решения на аккаунте](#rest-andpointy-na-storone-razrabotchika-reshenij) добавлен атрибут `subscription.notForResale`.
- В тело ответа при [Получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte) добавлен атрибут `subscription.notForResale`.

### 19-01-2024
#### Добавлено
- В тело запроса при [Активация решения на аккаунте](#rest-andpointy-na-storone-razrabotchika-reshenij) добавлен атрибут `subscription.expiryMoment`.
- В тело ответа при [Получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte) добавлен атрибут `subscription.expiryMoment`.

### 27-09-2023
#### Добавлено
- В тело запроса при [Активация решения на аккаунте](#rest-andpointy-na-storone-razrabotchika-reshenij) добавлен атрибут `subscription.tariffName` (название тарифа) и информация о новой причине активации (`"cause": "TariffChanged"`).
- В тело ответа при [Получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte) добавлен атрибут `subscription.tariffName` (название тарифа).

### 19-09-2023
#### Изменено
- В [дескрипторе решений](#deskriptor-resheniq) в качестве значения блока `access.resource` можно указывать [https://api.moysklad.ru/api/remap/1.2](https://api.moysklad.ru/api/remap/1.2).

### 06-09-2023
#### Добавлено
- В тело запроса при [активации решения на аккаунте](#aktiwaciq-resheniq-na-akkaunte) добавлена информация о подписке (атрибут `subscription`).

### 30-08-2023
#### Изменено
- Базовый URL REST-эндпоинтов vendor API (`MARKETPLACE-ENDPOINT`) сменился на [https://apps-api.moysklad.ru/api/vendor/1.0](https://apps-api.moysklad.ru/api/vendor/1.0).
- Для запросов к vendor API необходимо использовать сжатие (заголовок `Accept-Encoding`)
- URL личного кабинета разработчика сменился на [https://apps.moysklad.ru/cabinet](https://apps.moysklad.ru/cabinet).

### 23-11-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Розничном возврате, Внесении и Выплате денег.
- Поддержка дополнительного поля типа справочник [[Товар]](https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-rabota-s-dopolnitel-nymi-polqmi) в протоколе [change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta).

### 18-11-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Розничной продаже.

### 09-11-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Возврате покупателя.

### 12-10-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Списании и Счете покупателю.

### 06-09-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Счете поставщика.

### 23-08-2022
#### Изменено
- Прекращена поддержка [типа решений](#tipy-reshenij-dlq-kataloga-reshenij) iframe.
 
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
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Отгрузке, Перемещении и Оприходовании.

### 07-07-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) и [validation-feedback](#validaciq-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Счете покупателю.

### 04-07-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Приемке.

### 20-05-2022
#### Добавлено
- Поддержка полей `incomingDate` и `incomingNumber` для протокола change-handler в [Приемке](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka).

### 20-04-2022
#### Изменено
- Требования к [иконкам решений](#trebowaniq-k-ikonkam-reshenij).

### 04-03-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Поддержка [протокола навигации](#protokol-nawigacii) (`<navigation-service/>`) в главном iframe решения и модальных окнах.  

### 27-01-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Гибкие права решений](#blok-access) — поддержка права видеть себестоимость, цену закупки и прибыль товаров <viewProductCostAndProfit/>.

### 21-01-2022
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Товаре, Модификации, Услуге, Комплекте, Группе товаров. 

### 21-12-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) на странице создания в Перемещении, Списании и Оприходовании. Поддержка протокола валидации на страницах создания и редактирования Перемещения, Списания и Оприходования.

### 16-12-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) на странице создания в Приемке и Отгрузке. Поддержка протокола валидации на страницах создания и редактирования Приемки и Отгрузки.

### 10-12-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Перемещении, Списании и Оприходовании.

### 29-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Приемке.

### 24-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) на странице создания в Заказе покупателя. Поддержка протокола валидации при создании Заказа покупателя.

### 19-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Поддержка протокола валидации при редактировании Заказа покупателя.

### 17-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Поддержка [селектора групп товаров](#selektor-gruppy-towarow) (`<good-folder-selector/>`) в главном iframe решения и модальных окнах.

### 11-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол change-handler](#poluchenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Отгрузке.

### 01-11-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол update-provider](#izmenenie-sostoqniq-redaktiruemogo-ob-ekta) для виджетов в Заказе покупателя.

### 21-10-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Протокол навигации](#protokol-nawigacii) в виджетах.

### 07-10-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Возвратах покупателя и в Возвратах поставщику.

### 16-09-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Перемещении, Списании, Оприходовании, Внутреннем заказе, Инвентаризации.

### 30-08-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Гибкие права решений](#blok-access).

### 10-08-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Стандартные диалоги.

### 13-05-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  Протокол change-handler для [виджетов](#vidzhety) в Заказе покупателя.

### 21-01-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Розничной продаже, Входящем и Исходящем платеже, Приходном и Расходном ордере.

### 13-01-2021
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Кастомные модальные окна](#kastomnye-modal-nye-okna) в виджетах.

### 04-12-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Счете поставщика, Заказе поставщику, Заказе на производство, Приемке.

### 30-11-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) с поддержкой протокола dirty-state.

### 13-11-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) с поддержкой протокола save-handler.

### 10-11-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в новой карточке Контрагента.

### 09-11-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Счете покупателю.

### 22-10-2020
#### Добавлено
- [VendorApi 1.0](#vendor-api-1-0):
  Новый эндпоинт на стороне МоегоСклада: [Получение статуса решения на аккаунте](#poluchenie-statusa-resheniq-na-akkaunte).

### 08-10-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) с поддержкой селектора групп товаров.

### 22-09-2020
#### Изменено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в Заказе покупателя и Отгрузке.

### 18-08-2020
#### Добавлено
- Версия 2 [дескриптора решений](#deskriptor-resheniq):
  [Виджеты](#vidzhety) в карточке контрагента.
