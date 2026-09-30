## Кастомные модальные окна

Дескриптор с виджетом и главным iframe, использующие кастомные модальные окна

```xml
<ServerApplication  xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2      
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
        <expand>true</expand>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://api.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
    <widgets>        
        <entity.counterparty.edit>            
            <sourceUrl>https://example.com/widget.php</sourceUrl>            
            <height>                
                <fixed>150px</fixed>            
            </height>
            <uses>
                <good-folder-selector/>
            </uses>                  
        </entity.counterparty.edit>    
    </widgets>
    <popups>
        <popup>
            <name>somePopup</name>
            <sourceUrl>https://example.com/popup.php</sourceUrl>
        </popup>
        <popup>
            <name>somePopup2</name>
            <sourceUrl>https://example.com/popup-2.php</sourceUrl>
        </popup>
    </popups>
</ServerApplication>
```
> Сообщение ShowPopupRequest

```json 
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup",
  "popupParameters": "hello"
}
```

> Сообщение OpenPopup

```json 
{
  "name": "OpenPopup",
  "messageId": 36,
  "popupName": "somePopup",
  "popupParameters": "hello"
}
```

> Сообщение ClosePopup

```json 
{
  "name": "ClosePopup",
  "messageId": 17,
  "popupResponse": "world"
}
```

> Сообщение ShowPopupResponse

```json 
{
  "name": "ShowPopupResponse",
  "correlationId": 12,
  "popupName": "somePopup",
  "popupResolution": "normal",
  "popupResponse": "world"
}
```

Модальные окна позволяют расширить функциональность главного окна решения, виджетов или кастомных кнопок. 

Характеристики кастомного модального окна:

* Открывается на весь экран аналогично прочим модальным окнам в интерфейсе МоегоСклада. Например, вызываемое через иконку «карандаш» окно редактирования сущностей в полях.
* Является модальным, то есть открывается поверх текущей страницы МоегоСклада, и требует действия от пользователя внутри этого окна — взаимодействия с веб-страницей и/или закрытие окна.
* Содержимое окна определяет разработчик. Передавать данные можно от виджета (главного iframe) в модальное окно и в обратном направлении. 
* Может получать текущий [контекст пользователя](#/developer-guide/user-context#2-kontekst-polzovatelya), так же как виджеты и главное окно решения.
* В качестве заголовка окна всегда используется название решения.
* Имеет кнопку принудительного закрытия для пользователя — «крестик» справа вверху.
* Изменяет свои размеры при изменении размеров окна браузера.

Рассмотрим работу кастомных модальных окон на примере виджетов. В случае главного iframe все работает аналогично. 
Отличия при вызове окна из кастомных кнопок будут описаны ниже. 

Чтобы решение могло использовать кастомные модальные окна, добавьте в [дескриптор решения](#/developer-guide/solution-descriptor#4-blok-popups) блок `<popups>...</popups>`.
Пример дескриптора смотрите в правой части экрана.

Виджет может отобразить одно из кастомных модальных окон, отправив сообщение `ShowPopupRequest` с именем выбранного окна хост-окну. Пример такого сообщения смотрите в правой части экрана. 

Здесь:

* `messageId` — идентификатор сообщения;
* `popupName` — имя открываемого окна;
* `popupParameters` — опциональные параметры, передаваемые окну виджетом. Может иметь любой тип, в том числе `null`.

МойСклад проверяет сообщение `ShowPopupRequest`. Если сообщение валидно, отображается модальное окно: загружается страница окна по адресу `sourceUrl` в iframe, в GET-параметре передается `contextKey`. Процесс аналогичен загрузке виджета. Значение `sourceUrl` загружается из соответствующего элемента списка модальных окон `<popups>` в дескрипторе. Поиск производится по `popupName`, переданному в сообщении.

После загрузки модального окна хост-окно отправляет ему сообщение `OpenPopup`. Набор полей тот же, что и в `ShowPopupRequest`.
При этом `messageId` в данном сообщении свой, а не тот, что был передан в сообщении `ShowPopupRequest`.
  
Для закрытия модального окна, оно отправляет сообщение `ClosePopup` хост-окну. Пример такого сообщения смотрите в правой части экрана. 

Здесь:

* `messageId` — идентификатор сообщения;
* `popupResponse` — опциональный ответ, возвращаемый виджету. Может иметь любой тип, в том числе `null`.

МойСклад, в свою очередь, отправляет сообщение `ShowPopupResponse` виджету, открывшему окно. Пример такого сообщения смотрите в правой части экрана. 

Здесь:

* `correlationId` — идентификатор соответствующего сообщения ShowPopupRequest;
* `popupName` — имя открывавшегося модального окна;
* `popupResolution` — вариант, по которому произошло закрытие модального окна:
                      `normal` — нормальное закрытие окна по `ClosePopup`,
                      `closedByUser` — закрытие окна пользователем путем нажатия на «крестик»;
* `popupResponse` — опциональный ответ, возвращаемый виджету.

Страницы кастомных модальных окон кэшируются аналогично кэшированию виджетов. При повторном открытии окна по сообщению `ShowPopupRequest` переиспользуется ранее загруженный iframe. 

Ниже приводятся примеры работы с кастомными модальными окнами.

#### Пример работы без возврата параметров из модального окна

> Пример взаимодействия без передачи дополнительных параметров

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup"
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 35,
  "popupName": "somePopup"
}

// хост-окно -> виджет
{
  "name": "ShowPopupResponse",
  "correlationId": 12,
  "popupName": "somePopup",
  "popupResolution": "closedByUser"
}
```

> Пример взаимодействия с передачей параметров в виде строки

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 17,
  "popupName": "somePopup",
  "popupParameters": "hello"
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 36,
  "popupName": "somePopup",
  "popupParameters": "hello"
}

// хост-окно -> виджет
{
  "name": "ShowPopupResponse",
  "correlationId": 17,
  "popupName": "somePopup",
  "popupResolution": "closedByUser"
}
```

1. Виджет отправляет хост-окну сообщение `ShowPopupRequest`. В сообщении указывается имя модального окна и опциональные параметры.
2. Хост-окно отображает модальное окно, загружая страницу окна по адресу `sourceUrl` в iframe с передачей `contextKey` в GET-параметре.
3. Хост-окно отправляет в iframe модального окна сообщение `OpenPopup`, передавая в нем опциональные параметры от виджета.
4. Пользователь взаимодействует с веб-содержимым модального окна, после чего закрывает его через системную кнопку («крестик»), находящуюся в верхнем правом углу окна.
5. Система скрывает модальное окно и отправляет виджету сообщение `ShowPopupResponse` с указанием того, что окно было закрыто пользователем через системную кнопку (```"popupResolution": "closedByUser"```).

Пример модального окна с наличием только системной кнопки закрытия:

![useful image](./images/popup-view.png)

> Закрытие модального окна с использованием сообщения ClosePopup

```json 
...
// модальное окно -> хост-окно
{
  "name": "ClosePopup",
  "messageId": 37,
}

// хост-окно -> виджет
{
  "name": "ShowPopupResponse",
  "correlationId": 14,
  "popupName": "somePopup",
  "popupResolution": "normal"
}
```

Разработчик может отобразить на странице и собственную кнопку закрытия окна. При нажатии на нее будет отправляться сообщение `ClosePopup`, а виджет получит сообщение `ShowPopupResponse` с  ```"popupResolution": "normal"```.

![useful image](./images/popup-view-button.png)


#### Пример работы с возвратом параметров из модального окна

> Пример ответа с передачей данных о нажатой кнопке

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 29,
  "popupName": "somePopup"
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 36,
  "popupName": "somePopup"
}

// пользователь нажимает на кнопку «Сохранить»

// модальное окно -> хост-окно
{
  "name": "ClosePopup",
  "messageId": 44,
  "popupResponse": "save"
}

// хост-окно -> виджет
{
  "name": "ShowPopupResponse",
  "correlationId": 29,
  "popupName": "somePopup",
  "popupResolution": "normal",
  "popupResponse": "save"
}
```
Если модальному окну требуется вернуть информацию обратно в виджет, окно должно передать ее в поле `popupResponse` сообщения `ClosePopup`.

1. Виджет отправляет хост-окну сообщение `ShowPopupRequest`, указывая в нем имя модального окна и опциональные параметры.
1. Хост-окно отображает модальное окно, загружая его страницу по адресу `sourceUrl` в iframe с передачей `contextKey` в GET-параметре.
1. Хост-окно отправляет в iframe модального окна сообщение `OpenPopup` с опциональными параметрами.
1. Пользователь взаимодействует с веб-содержимым модального окна, после чего нажимает кнопку закрытия или сохранения, находящуюся внутри страницы модального окна.
1. Модальное окно отправляет хост-окну сообщение `ClosePopup`. В нем передаются параметры, которые зависят от действий пользователя, например тип нажатой кнопки. 
1. Система скрывает модальное окно и отправляет виджету сообщение `ShowPopupResponse` с указанием параметров, переданных модальным окном.

Пользователь может закрыть модальное окно принудительно. При этом параметры в виджет не будут переданы.

Пример модального окна с кнопками «Сохранить» и «Отмена»:

![useful image](./images/popup-edit.png)

#### Отображение содержимого, которое не вмещается в окно целиком

Пример плавающей верстки содержимого

```html
<!doctype html>
<html lang="ru">
<head>
    <meta charset="utf-8">

    <title>Popup example</title>
    <style>
        body {
            overflow: hidden;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        .content-container {
            overflow: auto;
            flex-grow: 1;
        }
        .buttons-container {
            padding-top: 15px;
            min-height: 55px;
        }
        .button {
          font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
          font-size: 12px;
          cursor: pointer;
          color: #222222;
          padding: 7px 11px;
          border-radius: 3px;
          border: 1px solid #cccccc;
          background-image: linear-gradient(to bottom, #ffffff, #e6e6e6);
          line-height: 1;
        }

        .button:hover {
          opacity: .8;
        }

        .button:focus {
          outline: 0;
          background-image: linear-gradient(to bottom, #e6e6e6, #ffffff);
        }

        .button--success {
          color: #ffffff;
          border: 1px solid #a1b900;
          background-image: linear-gradient(to bottom, #cee356, #a1b900);
        }

        .button--success:focus {
          background-image: linear-gradient(to bottom, #a1b900, #cee356);
        }
    </style>
</head>

<body>
<div class="main-container">
    <div class="content-container">
        <!--Разместите содержимое здесь -->
    </div>
    <div class="buttons-container">
        <button class="button button--success">Сохранить</button>
        <button class="button">Отмена</button>
    </div>
</div>
</body>
</html>
```

Если во модальном окне нужно отобразить содержимое, которое может не поместиться на экране пользователя, используйте плавающую верстку. Так вы можете создать полосы прокрутки для содержимого, и кнопки закрытия окна всегда будут отображаться в нижней части окна. 

Пример модального окна с полосами прокрутки:

![useful image](./images/popup-scroll.png)

Пример такой верстки представлен справа.


#### Способы передачи параметров

> Пример взаимодействия с передачей параметров в виде строки

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup",
  "popupParameters": "hello"
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 35,
  "popupName": "somePopup",
  "popupParameters": "hello"
}
```

> Пример взаимодействия с передачей параметров в виде объекта

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup",
  "popupParameters": {
    "aaa": 1,
    "bbb": "qwerty"
  }
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 35,
  "popupName": "somePopup",
  "popupParameters": {
    "aaa": 1,
    "bbb": "qwerty"
  }
}
```     

> Пример взаимодействия с передачей параметров в виде массива

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup",
  "popupParameters": [123, "foobar"]
}

// хост-окно -> модальное окно
{
  "name": "OpenPopup",
  "messageId": 35,
  "popupName": "somePopup",
  "popupParameters": [123, "foobar"]
}
```

Существует несколько способов передачи параметров между виджетами и модальными окнами:

* передача в виде примитивного значения;
* передача в виде объекта;
* передача в виде массива, в том числе массива объектов;
* передача в виде значения `null`.

Справа приведены примеры передачи параметров из виджета в модальное окно через сообщение `ShowPopupRequest`.

Аналогичные способы передачи можно использовать для возврата ответа в сообщении `ClosePopup`.

#### Вызов модального окна из кастомной кнопки

Кнопка может отобразить одно из модальных окон решения, отправив в ответе на [запрос обработки нажатия на кнопку](#/vendor-api/vendor-endpoints#4-obrabotka-nazhatiya-na-kastomnuyu-knopku) значение `action=ShowPopup` с именем выбранного окна и опциональными параметрами. 

Если такое окно описано в дескрипторе решения, то, как и для вызова через сообщение, оно загружается (с передачей `contextKey`) или берется из кэша.
После загрузки модального окна хост-окно отправляет ему сообщение `OpenPopup` и передает опциональные параметры, полученные в запросе.

По окончании работы с модальным окном пользователь может закрыть его через системную кнопку либо само окно может отправить сообщение `ClosePopup`.  

Отличия при работе с модальными окнами, вызванными по нажатию кастомной кнопки:

* нет взаимодействия с хост-окном (не используются сообщения `ShowPopupRequest` и `ShowPopupResponse`)
