## Как создать и опубликовать решение


Для каталога решений МоегоСклада можно создать решение на любом языке программирования с использованием любых фреймворков. Допустимые типы решений: [серверные решения](#/app-types/app-types#3-servernye-resheniya), [телефония](#/app-types/app-types#3-telefoniya). 

Решения интегрируются с МоимСкладом с помощью различных API. 
Серверные решения могут использовать:

* [JSON API 1.2](https://dev.moysklad.ru/doc/api/remap/1.2) 
* [Loyalty API 1.0](https://dev.moysklad.ru/doc/api/loyalty/1.0) 
* [FiscalAPI 1.0](https://dev.moysklad.ru/doc/api/fiscal/1.0) 
* [QRPay API 1.0](https://dev.moysklad.ru/doc/api/qr-pay/1.0) 

Решения телефонии используют [Phone API 1.0](https://dev.moysklad.ru/doc/api/phone/1.0). 
Процесс создания решений телефонии описан в [Сценарии работы с Phone API 1.0](https://dev.moysklad.ru/doc/api/phone/1.0/#%D1%81%D1%86%D0%B5%D0%BD%D0%B0%D1%80%D0%B8%D0%B9-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B). 

Пошаговый процесс создания серверных решений рассмотрим ниже.

1. Создайте бизнес-логику решения на сервере.

2. Создайте черновик решения в [личном кабинете разработчика](#/cabinet/developer-cabinet#1-lichnyj-kabinet-razrabotchika), используя один из примеров [дескриптора](#/developer-guide/solution-descriptor#2-deskriptor-resheniya). После создания черновика вы получите appId, appUid, secret key, необходимые для работы с Vendor API.

3. Реализуйте эндпоинты согласно спецификации [Vendor API 1.0](#/vendor-api/authentication#1-vendor-api-10), чтобы обрабатывать [события](#/vendor-api/vendor-endpoints#2-rest-endpointy-na-storone-razrabotchika-reshenij) решения. При установке и возобновлении решения МойСклад передает [токен для доступа](#/developer-guide/json-api-token-access#2-dostup-po-tokenu-k-json-api) к [JSON API 1.2](https://dev.moysklad.ru/doc/api/remap/1.2).

4. Если пользователь должен будет настраивать решение при его установке на аккаунт, то в ответе на [запрос установки решения](#/vendor-api/vendor-endpoints#4-aktivaciya-resheniya-na-akkaunte) верните **SettingsRequired** и реализуйте [главное окно решения](#/developer-guide/iframes#4-glavnyj-iframe).

5. Если в решении нужны дополнительные поля для сущностей и/или документов, создайте их через JSON API 1.2 в рамках [активации решения](#/vendor-api/activation#2-process-aktivacii-resheniya-na-akkaunte). Если при этом процесс создания занимает более одной минуты, используйте асинхронную активацию с возвратом статуса **Activating**.

6. Если решение нужно встроить в интерфейс МоегоСклада, то можно:
  * добавить [виджет](#/developer-guide/widgets#2-vidzhety) решения. Для этого нужно реализовать страницу виджета и обновить [дескриптор](#/developer-guide/solution-descriptor#2-deskriptor-resheniya), добавив тег `widgets`. 
  * добавить [кастомную кнопку](#/developer-guide/custom-buttons#2-kastomnye-knopki). Для этого нужно реализовать [эндпоинт обработчика нажатия на кнопку в vendorApi](#/vendor-api/vendor-endpoints#4-obrabotka-nazhatiya-na-kastomnuyu-knopku) и обновить [дескриптор](#/developer-guide/solution-descriptor#2-deskriptor-resheniya), добавив тег `buttons`.
  * добавить [окно чатов](#/developer-guide/iframes#4-okno-chatov). Для этого нужно реализовать страницу чата и обновить [дескриптор](#/developer-guide/solution-descriptor#2-deskriptor-resheniya), добавив тег `iframes`.

7. Решение может быть встроено в интерфейс мобильного приложения МоегоСклада. Для этого нужно реализовать страницу [мобильного окна](#/developer-guide/iframes#4-mobilnye-prilozheniya) и обновить тег `iframes` в [дескрипторе](#/developer-guide/solution-descriptor#2-deskriptor-resheniya).

8. Если решение поддерживает работу с системой лояльности, реализуйте на своей стороне поддержку Loyalty API и после установки решения сохраните настройки программы лояльности через [запрос изменения настроек лояльности на аккаунте](#/vendor-api/moysklad-endpoints#4-izmenenie-nastroek-loyalnosti-na-akkaunte). Подробнее про процесс взаимодействия с системами лояльности см. [Сценарии работы с LoyaltyAPI](https://dev.moysklad.ru/doc/api/loyalty/1.0/#scenarij-raboty).

9. Если решение поддерживает работу с операциями фискализации, реализуйте на своей стороне поддержку [Fiscal API](https://dev.moysklad.ru/doc/api/fiscal/1.0).

10. Если решение поддерживает работу с оплатой по QR-коду, реализуйте на своей стороне поддержку [QrPay API](https://dev.moysklad.ru/doc/api/qr-pay/1.0).

11. [Разместите](#/placement/placement-requirements#1-usloviya-razmesheniya-reshenij) решение в каталоге решений или как приватное с возможностью установки только по прямой ссылке. Режим распространения (публичное/приватное) выбирается при отправке на модерацию. После прохождения модерации изменить режим будет невозможно.
