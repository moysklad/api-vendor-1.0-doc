## Типы решений для каталога решений

Тип решения определяет, в первую очередь, технический способ интеграции решения с МоимСкладом.

В каталог решений МоегоСклада можно добавить:

+ Серверные решения,
+ Телефония (Phone API)

Поддержка функций в зависимости от типа решения:

| Функциональность                         | Серверные решения | Телефония |
|------------------------------------------|-------------------|-----------|
| Iframe и доступ к контексту пользователя | +                 | -         |
| Активация и деактивация по Vendor API    | +                 | -         |
| Доступ по токену к JSON API 1.2          | +                 | -         |
| Отладка на аккаунтах разработчика        | +                 | +         |
| Phone API                                | -                 | +         |
| Loyalty API                              | +                 | -         |
| Fiscal API                               | +                 | -         |
| Виджеты                                  | +                 | -         |
| Кастомные кнопки                         | +                 | -         |
| Количество решений на аккаунте           | Не ограничено     | 1         |

### Серверные решения

Серверные решения — это решения, основная функциональность которых основана на обмене данными с МоимСкладом по
JSON API.
Для этого при активации решения по Vendor API на сервер разработчика
передается [токен доступа к JSON API 1.2](#dostup-po-tokenu-k-json-api). Доступ по токену поддерживается только в JSON
API 1.2.

Для серверных решений поддерживается активация и деактивация по Vendor API.

Для серверных решений доступно
получение [контекста текущего пользователя](#poluchenie-kontexta-pol-zowatelq-dlq-reshenij-s-iframe-chast-u-kastomnymi-modal-nymi-oknami-i-widzhetami)
МоегоСклада (через Vendor API) —
то есть можно узнать, какой именно пользователь какого аккаунта открывает решение в UI МоегоСклада.

Также серверное решение может иметь iframe-часть — страницу, которую можно использовать как пользовательский
интерфейс,
в том числе для настроек решения со стороны пользователя МоегоСклада или администратора аккаунта.
Iframe-часть решения загружается по указанному разработчиком URL на отдельной вкладке внутри раздела Решения
МоегоСклада. Поддерживается возможность расширенного iframe. Подробнее смотрите [Дескриптор](#blok-iframe).

Только для серверных решений доступны [виджеты](#vidzhety) и [кастомные кнопки](#kastomnye-knopki).

Только серверные решения могут быть [платными](#stoimost-resheniq).

В общем случае жесткие требования к внешнему виду и визуальному дизайну iframe-части решений отсутствуют.
Приветствуется визуальное соответствие дизайну МоегоСклада. Для этого разработан UI Kit:

![useful image](ui-kit.png)

UI Kit доступен по [ссылке](https://github.com/moysklad/html-marketplace-1.0-uikit).

Одновременно на аккаунте может быть подключено несколько серверных решений.

Доступна отладка на аккаунтах разработчика.

Серверные решения могут поддерживать [Loyalty API](https://dev.moysklad.ru/doc/api/loyalty/1.0).
Для отладки используйте собственный черновик решения совместно с решением Касса МоегоСклада.

Примечание: при наличии у пользователя нескольких установленных решений, использующих Loyalty API, отправка запросов из Кассы будет происходить только для одного решения, выбранного пользователем в настройках Скидок.

### Телефония

Эти решения представляют собой интеграцию с внешними сервисами телефонии по Phone API:
[https://online.moysklad.ru/api/phone/1.0/doc/index.html](https://online.moysklad.ru/api/phone/1.0/doc/index.html)

Решения телефонии не могут получать доступ по токену к JSON API, не имеют возможности активации и деактивации по
Vendor API. В перспективе эти возможности могут появиться.

Одновременно на аккаунте может быть подключено только одно решение телефонии.

Доступна отладка на аккаунтах разработчика.
