## Демо-решения


Для демонстрации способов взаимодействия решений разработчиков с МоимСкладом были созданы проекты на нескольких языках программирования:

* Node.js  - [репозиторий проекта на GitHub](https://github.com/moysklad/node-js-demo-app)
* PHP - [репозиторий проекта на GitHub](https://github.com/moysklad/php-demo-app)
* Python  - [репозиторий проекта на GitHub](https://github.com/moysklad/python-demo-app)

В этих проектах реализован следующий набор функций:

* Активация с получением токена доступа к JSON API 1.2 и деактивация по Vendor API
* Хранение состояния установок решений в БД (SQLite)
* [Сохранение пользовательских настроек](#/vendor-api/suspend-and-resume#4-sohranenie-nastroek-pri-priostanovke-resheniya) при приостановке и удалении решения с восстановлением при возобновлении и повторной установке
* Использование [основного окна](#/developer-guide/iframes#2-okna-iframes) для настройки решения администратором аккаунта с обновлением статуса в каталоге решений
* Получение [контекста пользователя](#/developer-guide/user-context#2-kontekst-polzovatelya): отображение информации о пользователе, проверка прав администратора
* Получение данных из JSON API 1.2
* Встраивание [виджетов](#/developer-guide/widgets#2-vidzhety) в Заказ покупателя и Счет покупателю. Работа с виджетами через [JS Widget SDK](#/developer-guide/widget-sdk#2-sdk-dlya-vidzhetov)
* Обработка [кастомных кнопок](#/developer-guide/custom-buttons#2-kastomnye-knopki) в документе и списке Заказов покупателя
* Открытие [кастомного модального окна](#/developer-guide/custom-popups#2-kastomnye-modalnye-okna) из виджета и по нажатию кастомной кнопки
* Генерация дескриптора для создания черновика решения в [личном кабинете разработчика](#/cabinet/developer-cabinet#1-lichnyj-kabinet-razrabotchika)
