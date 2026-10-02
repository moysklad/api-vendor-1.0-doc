## Виджеты

Виджет — это плагин, имеющий визуальную часть. Визуальная часть виджета — прямоугольный блок, который встраивается в интерфейс МоегоСклада в определенном месте. Содержимое блока определяется решением.

Виджеты можно добавить на страницы МоегоСклада, которые есть в [списке](#/developer-guide/app-descriptor#3-blok-widgets). Чтобы встроить виджет на страницу, которая пока не поддерживается, свяжитесь с нами в Telegram или по электронной почте.

Виджеты доступны для серверных решений с дескриптором версии v2.

Подробнее структура дескриптора для решения с виджетом описана в разделе [Дескриптор решений](#/developer-guide/app-descriptor#2-deskriptor-resheniya).

> Дескриптор решения с виджетом в карточке контрагента

```xml
   <ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2
         https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
       <iframe>...</iframe>
       <vendorApi>...</vendorApi>
       <access>...</access>
       <widgets>
           <entity.counterparty.edit>
               <sourceUrl>https://b2b.moysklad.ru/widget/counter-party</sourceUrl>
               <height>
                   <fixed>61px</fixed>
               </height>
               <supports>
                   <open-feedback/>
                   <save-handler/>
               </supports>
                <uses>
                    <good-folder-selector/>
                </uses>
           </entity.counterparty.edit>
       </widgets>
   </ServerApplication>
```

### Загрузка и отображение виджета на странице

Виджет на странице загружается в iframe по URL, указанному в теге `<sourceUrl>...</sourceUrl>` виджета в дескрипторе, 
с передачей текущего [контекста пользователя](#/developer-guide/user-context#2-kontekst-polzovatelya).

Виджет начинает отображаться на странице только после перехода решения в статус **Activated**.
Если решение предполагает настройку и статус **SettingsRequired**, виджет отображается после настройки решения.

После того как пользователь установил и настроил решение с дескриптором из примера выше, виджет будет показан в карточке контрагента.

![useful image](./images/widget-counterparty-page.png)

Виджеты могут отображаться в нескольких режимах:

- развернутый вид — виджет отображается с рабочей iframe-областью;
- свернутый вид — рабочая область виджета скрыта;
- скрыт — элемент управления виджетом не отображается (пользователь не может взаимодействовать с виджетом).

Если у пользователя установлены несколько решений с виджетами, встроенными на одну страницу МоегоСклада, отображаются все виджеты.
Порядок отображения соответствует расположению родительских решений в каталоге. В редакторах, поддерживающих функцию Drag-and-drop, пользователь может сам поменять порядок отображения виджетов.

Параметры содержимого виджетов:

- ширина `400px` — для виджетов всех решений,
- высота — статически указывается разработчиком в дескрипторе решения. В примере высота — `61px`.

Виджет можно скрыть, указав высоту `0px`. Скрытые виджеты не отображаются на страницах, но могут использовать все возможные протоколы, например [протокол **validation-feedback**](#/developer-guide/widgets#3-validaciya-sostoyaniya-redaktiruemogo-obuekta). 

![useful image](./images/widget-size.png)

### Кэширование виджетов

Система виджетов в МоемСкладе реализована так, чтобы, по-возможности, загружать виджет один раз. При первом открытии страницы с виджетом в рамках одной вкладки браузера происходит загрузка. Далее iframe c загруженным в него виджетом кэшируется и переиспользуется во всех последующих открытиях страницы с виджетом в рамках одной вкладки браузера.

Если по техническим причинам кэширование не произошло, хост-окно может:

- создать несколько iframe-экземпляров для одной точки расширения в рамках одной вкладки браузера (эти экземпляры могут существовать одновременно);
- не кэшировать iframe виджета после загрузки.

### Протоколы виджетов

Для передачи данных между МоимСкладом и виджетами может использоваться один из перечисленных ниже протоколов обмена сообщениями через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage).

Если виджет поддерживает [протокол **open-feedback**](#/developer-guide/widgets#3-protokol-obratnoj-svyazi-pri-otkrytii-vidzheta), система не отображает содержимое виджета сразу, а ждет ответного сообщения от виджета о готовности. До этого момента внутри виджета отображается заглушка. Когда виджет готов, он отправляет сообщение `OpenFeedback`. После этого система полностью открывает виджет пользователю.
Виджеты без поддержки этого протокола отображаются сразу как только получают сообщение `Open`, даже если они к этому моменту еще не успели обновить отображаемую информацию.
 
Если виджет поддерживает [протокол **change-handler**](#/developer-guide/widgets#3-poluchenie-sostoyaniya-redaktiruemogo-obuekta), при редактировании документа пользователем на странице с виджетом он оповещается об изменениях, получая сообщение `Change`, содержащее несохраненное состояние документа. 

Если виджет поддерживает [протокол **validation-feedback**](#/developer-guide/widgets#3-validaciya-sostoyaniya-redaktiruemogo-obuekta), то в ответ на сообщение `Change` он может запрещать хост-окну сохранять документ, если тот невалиден.

Если виджет поддерживает [протокол **update-provider**](#/developer-guide/widgets#3-izmenenie-sostoyaniya-redaktiruemogo-obuekta), при редактировании документа пользователем на странице с виджетом 
он может изменять несохраненное состояние документа, отправляя сообщение `UpdateRequest` со списком полей, которые необходимо изменить. 
 
При сохранении страницы с виджетом, если виджет, который находится на экране редактирования сущности, поддерживает [протокол **save-handler**](#/developer-guide/widgets#3-sohranenie-polzovatelem-redaktiruemogo-obuekta), он оповещается о факте сохранения объекта пользователем, получая сообщение `Save`.

Виджет, поддерживающий [протокол **dirty-state**](#/developer-guide/widgets#3-priznak-nesohranennogo-sostoyaniya-vidzheta), может сообщить хост-окну, что в виджете есть несохраненные изменения. Для этого виджет отправляет хост-окну сообщение `SetDirty`. Виджет может отправить хост-окну сообщение `ClearDirty`, после чего диалог подтвержения закрытия окна не будет появляться, при условии, что отсутствуют несохраненные изменения в самом UI МоегоСклада или в других виджетах. Внутренний dirty-флаг для виджета в хост-окне сбрасывается при открытии. То есть при отправке сообщения `Open` хост-окно считает, что в виджете нет несохраненных изменений.
 
Поддержку виджетом протоколов **open-feedback**, **save-handler**, **dirty-state**, **change-handler** необходимо указать в [дескрипторе](#/developer-guide/app-descriptor#2-deskriptor-resheniya)   решения.
Каждая точка встраивания имеет свой [список поддерживаемых протоколов](#/developer-guide/app-descriptor#3-dostupnost-dopolnitelnyh-protokolov-v-zavisimosti-ot-tochek-vstraivaniya).

Виджеты на страницах создания, например в точке встраивания `document.customerorder.create`, имеют ограниченную функциональность
по сравнению с виджетами на страницах редактирования, например `document.customerorder.edit`. Это выражается в меньшем количестве поддерживаемых протоколов и в реализации самих протоколов. Например, в сообщении **Change** часть полей, которые заполняются после первого сохранения документа (`id`, `created`, `meta` и другие) будет заполнено значением `null`.

После первого сохранения виджет точки `*.create` закрывается, а хост-окно открывает виджет точки `*.edit` — отдельный экземпляр iframe со своим сообщением `Open`, в котором уже заполнен `objectId`. Отдельное уведомление о первом сохранении в точку `*.create` не отправляется; признаком сохранения служит `Open` в точке `*.edit` с новым `objectId`.

Особенность работы документа Заказ кодов маркировки после его отправки в Честный Знак (через кнопку Заказ кодов):

- Документ доступен для редактирования, но сохранение изменений заблокировано. 
Т.е. на любые изменения в документе (статусы, поля) в виджет будут приходить сообщения **Change** без последующего **Save**.

Поддержка [сервисных протоколов](#/developer-guide/app-descriptor#3-blok-servisnyh-protokolov-uses) виджетами на страницах создания пока не реализована,
за исключением [протокола контекста пользователя](#/developer-guide/host-window-services#3-protokol-konteksta-polzovatelya).

### Открытие виджета

Когда пользователь открывает страницу с виджетом, хост-окно отображает iframe виджета, только что загруженный или ранее закэшированный, и передает в этот iframe сообщение `Open` через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage).

> Сообщение Open для виджета на экране создания в Заказе покупателя

```json
    {
      "name": "Open",
      "messageId": 12345,
      "extensionPoint": "document.customerorder.create",
      "objectId": null,
      "displayMode": "expanded"
    }
```

> Сообщение Open для виджета на экране редактирования в Заказе покупателя

```json
    {
      "name": "Open",
      "messageId": 12345,
      "extensionPoint": "document.customerorder.edit",
      "objectId": "8e9512f3-111b-11ea-0a80-02a2000a3c9c",
      "displayMode": "expanded"
    }
```

Здесь: 

- `extensionPoint` — текущая точка расширения;
- `objectId` — идентификатор текущего документа или сущности. Для виджета, отображаемого на экране создания, значение — `null`;
- `displayMode` — режим отображения виджета. Сейчас может принимать только одно значение `expanded`.

Виджет при получении сообщения `Open` может, например, обратиться на сервер за данными для указанного объекта `objectId` и отобразить их пользователю.

**Примечание**: в сообщении Open передается идентификатор текущей открытой сущности в карточке, который отображается в URL браузера в параметре `id`. Несмотря на то, что для сущностей Товар, Услуга, Комплект и Модификация этот идентификатор отличается от используемого в remap API, запрос по нему по-прежнему будет работать. При этом сервер будет использовать [редирект](https://developer.mozilla.org/ru/docs/Web/HTTP/Status/308) . 
Пример запроса для Товара `https://online.moysklad.ru/app/#good/edit?id=9e73d736-a0de-11e9-9109-f8fc00095c7f`. Для упрощения часть вывода пропущена.

> Ответ на запрос получения Товара  

```shell
curl -X GET --location "https://api.moysklad.ru/api/remap/1.2/entity/product/9e73d736-a0de-11e9-9109-f8fc00095c7f"     -H "Content-Type: application/json"     -H "Authorization: Bearer ..." -v 

> GET /api/remap/1.2/entity/product/9e73d736-a0de-11e9-9109-f8fc00095c7f HTTP/1.1
> Host: online.moysklad.ru
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Type: application/json
> Authorization: Bearer ...
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 308 Permanent Redirect
< Server: nginx/1.18.0
< Date: Fri, 28 Jan 2022 11:13:00 GMT
< Content-Length: 0
< Connection: keep-alive
< Cache-Control: max-age=0, no-cache
< X-Lognex-Reset: 0
< X-Lognex-Retry-After: 0
< Location: https://api.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81
< X-Lognex-Retry-TimeInterval: 3000
< X-RateLimit-Remaining: 44
< X-RateLimit-Limit: 45
< Strict-Transport-Security: max-age=15552000
< 
* Connection #1 to host online.moysklad.ru left intact
* Issue another request to this URL: 'https://api.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81'
* Found bundle for host online.moysklad.ru: 0x55cb04fa3970 [serially]
* Can not multiplex, even if we wanted to!
* Re-using existing connection! (#1) with host online.moysklad.ru
* Connected to online.moysklad.ru (88.212.252.4) port 443 (#1)
> GET /api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81 HTTP/1.1
> Host: online.moysklad.ru
> User-Agent: curl/7.68.0
> Accept: */*
> Content-Type: application/json
> Authorization: Bearer ...
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Server: nginx/1.18.0
< Date: Fri, 28 Jan 2022 11:13:00 GMT
< Content-Type: application/json;charset=utf-8
< Content-Length: 6535
< Connection: keep-alive
< Vary: Accept-Encoding
< Cache-Control: no-cache
< X-Lognex-Reset: 0
< X-Lognex-Retry-After: 0
< X-Lognex-Retry-TimeInterval: 3000
< X-RateLimit-Remaining: 43
< X-RateLimit-Limit: 45
< Strict-Transport-Security: max-age=15552000
< 
{
  "meta" : {
    "href" : "https://api.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81",
    "metadataHref" : "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
    "type" : "product",
    "mediaType" : "application/json",
    "uuidHref" : "https://online.moysklad.ru/app/#good/edit?id=9e73d736-a0de-11e9-9109-f8fc00095c7f"
  },
  "id" : "9e73e41d-a0de-11e9-9109-f8fc00095c81",
  ...
}
```

### Протокол обратной связи при открытии виджета

По умолчанию при открытии закэшированного виджета его содержимое отображается сразу.

Если виджет при открытии делает обращение к серверу, может быть видна небольшая задержка. В это время будет отображается прежнее состояние и содержание виджета, например, данные для прошлого контрагента.

Протокол обратной связи позволяет виджету явно сообщить хост-окну в какой именно момент отобразить содержимое виджета. До этого содержимое виджета будет закрыто ненавязчивым лоадером:

![useful image](./images/loader-in-widget.png)

Для переключения хост-окна на использование протокола обратной связи при открытии виджета в дескрипторе для виджета надо явно указать поддержку дополнительного протокола **open-feedback**.

> Тег дополнительных протоколов supports с протоколом open-feedback

```xml
    <supports>
        <open-feedback/>
    </supports>
```

Виджет передает сообщение `OpenFeedback` хост-окну в качестве сигнала готовности содержимого виджета для отображения пользователю.

> Cообщение OpenFeedback

```json 
{
  "name": "OpenFeedback",
  "correlationId": 12345
}
```

Здесь `correlationId` содержит значение `messageId` ранее полученного сообщения `Open`.

Хост-окно, получив сообщение `OpenFeedback`, отображает содержимое виджета пользователю и убирает лоадер.

### Сохранение пользователем редактируемого объекта

Хост-окно может оповещать виджет о факте сохранения редактируемого объекта. Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **save-handler**.

> Тег дополнительных протоколов supports с протоколом save-handler

```xml
    <supports>
        <save-handler/>
    </supports>
```

Хост-окно отправляет виджету сообщение `Save` через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) при сохранении редактируемого объекта после сохранения объекта в базе данных. То есть на момент получения виджетом сообщения Save сохраненное состояние объекта уже доступно через JSON API.

Сохранение редактируемого объекта инициируется пользователем:

- при явном нажатии на кнопку **Сохранить**, в том числе при сохранении объекта без фактического внесения изменений;

- при покидании объекта и его явном сохранении через диалог подтверждения сохранения изменений, в том числе при листании кнопками-стрелочками на соседние объекты;

- при автоматическом сохранении изменений закрываемого объекта, например, при создании связанного документа Отгрузки из Заказа покупателя.

> Сообщение Save

```json
    {
      "name": "Save",
      "messageId": 32109,
      "extensionPoint": "entity.counterparty.edit",
      "objectId": "8e9512f3-111b-11ea-0a80-02a2000a3c9c"
    }
```

Здесь:

- `extensionPoint` — текущая точка расширения;
- `objectId` — идентификатор текущего документа или сущности, аналогичен идентификатору в сообщении `Open`.

### Признак несохраненного состояния виджета

Хост-окно поддерживает подтверждение закрытия окна пользователем, если он изменил данные в форме виджета, но не сохранил их. Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **dirty-state**.

> Тег дополнительных протоколов supports с протоколом dirty-state

```xml
  <supports>
      <dirty-state/>
  </supports>
```

После того, как пользователь внес изменения в виджет, он отправляет хост-окну сообщение `SetDirty`.

> Сообщение SetDirty

```json
    {
      "name": "SetDirty",
      "messageId": 12,
      "openMessageId": 7
    }
```

Здесь openMessageId содержит значение messageId ранее полученного сообщения `Open`.

Система учитывает, что в виджете есть несохраненные изменения. Далее, если пользователь нажимает кнопку **Закрыть** или другим способом пытается уйти с формы редактирования, система отображает диалог подтверждения сохранения изменений:

 ![useful image](./images/confirm-save-popup.png)

Если виджет после отправки `SetDirty` отправляет хост-окну сообщение `ClearDirty`, система не учитывает данный виджет при отображении диалога подтверждения сохранения изменений. То есть, если отсутствуют прочие несохраненные изменения самого объекта или в других виджетах, система не запрашивает диалог подтверждения сохранения изменений при закрытии редактируемого объекта.

> Сообщение ClearDirty

```json
    {
      "name": "ClearDirty",
      "messageId": 13
    }
```

### Получение состояния редактируемого объекта

Хост-окно может оповещать виджет об изменениях несохраненного состояния редактируемого объекта. Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **change-handler**.

> Тег дополнительных протоколов supports с протоколом change-handler

```xml
    <supports>
        <change-handler/>
    </supports>
```

Хост-окно отправляет виджету сообщение `Change` через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage), содержащее несохраненное состояние документа при редактировании документа пользователем.
 
 Отправка сообщения `Change` инициируется при следующих действиях пользователя:
 
 - при изменении полей документа, в том числе дополнительных полей, путем редактирования/выбора значения в селекторе;
 - при добавлении/удалении/редактировании позиций документа.
 
 Отправка сообщения `Change` **не происходит** в следующих случаях:
 
 - при открытии экрана редактирования документа;
 - при изменении состояния документа в результате сохранения пользователем;
 - при изменении полей, которые не поддерживаются;
 - если при редактировании значение редактируемого поля не изменилось, то есть при отсутствии реальных изменений. 

При сохранении без изменений валидация виджета не запрашивается и сохранение проходит. Чтобы проверить уже сохраненный документ при открытии, получите его по JSON API, используя `objectId` из сообщения `Open`, и покажите результат в виджете.
 
 
 Узнать, для каких точек поддерживается протокол **change-handler**, можно [тут](#/developer-guide/app-descriptor#3-dostupnost-dopolnitelnyh-protokolov-v-zavisimosti-ot-tochek-vstraivaniya).

> Сообщение Change

```json
{
  "name": "Change",
  "extensionPoint": "document.customerorder.edit",
  "messageId": 7,
  "changeHints": [
    "positions",
    "_fields"
  ],
  "objectState": {
    "meta": {
      "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/c4c6e6ea-b3f5-11eb-0a80-35ed000000b8",
      "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
      "type": "customerorder",
      "mediaType": "application/json",
      "uuidHref": "https://online.moysklad.ru/app/#customerorder/edit?id=c4c6e6ea-b3f5-11eb-0a80-35ed000000b8"
    },
    "id": "c4c6e6ea-b3f5-11eb-0a80-35ed000000b8",
    "accountId": "5fc956ad-b3f2-11eb-0a80-1b8a00000000",
    "created": "2021-05-13 17:16:11.465",
    "payedSum": 0,
    "shippedSum": 0,
    "invoicedSum": 0,
    "name": "00001",
    "applicable": true,
    "moment": "2021-05-13 17:15:00.000",
    "store": {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/store/605491e4-b3f2-11eb-0a80-35ed00000074",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/store/metadata",
        "type": "store",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#warehouse/edit?id=605491e4-b3f2-11eb-0a80-35ed00000074"
      }
    },
    "rate": {
      "currency": {
        "meta": {
          "href": "https://api.moysklad.ru/api/remap/1.2/entity/currency/6055a619-b3f2-11eb-0a80-35ed00000079",
          "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/currency/metadata",
          "type": "currency",
          "mediaType": "application/json",
          "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=6055a619-b3f2-11eb-0a80-35ed00000079"
        }
      }
    },
    "organization": {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/organization/6051401c-b3f2-11eb-0a80-35ed00000072",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/organization/metadata",
        "type": "organization",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#mycompany/edit?id=6051401c-b3f2-11eb-0a80-35ed00000072"
      }
    },
    "agent": {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/60550738-b3f2-11eb-0a80-35ed00000077",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
        "type": "counterparty",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#company/edit?id=60550738-b3f2-11eb-0a80-35ed00000077"
      }
    },
    "state": {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/60850d6a-b3f2-11eb-0a80-35ed00000097",
        "type": "state",
        "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
        "mediaType": "application/json"
      }
    },
    "externalCode": "JAGi0Yg0i0OYvylp7SzDi3",
    "vatEnabled": true,
    "vatIncluded": true,
    "vatSum": 0,
    "sum": 21000,
    "updated": "2021-05-13 17:16:11.434",
    "reservedSum": 20000,
    "attributes": [
      {
        "meta": {
          "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fb3ad9-b3f6-11eb-0a80-35ed000000cb",
          "type": "attributemetadata",
          "mediaType": "application/json"
        },
        "id": "14fb3ad9-b3f6-11eb-0a80-35ed000000cb",
        "name": "Строка",
        "type": "string",
        "value": "123АААББвQ"
      },
      {
        "meta": {
          "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fbcb79-b3f6-11eb-0a80-35ed000000cc",
          "type": "attributemetadata",
          "mediaType": "application/json"
        },
        "id": "14fbcb79-b3f6-11eb-0a80-35ed000000cc",
        "name": "Ссылка",
        "type": "link",
        "value": null
      },
      {
        "meta": {
          "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fbd363-b3f6-11eb-0a80-35ed000000cd",
          "type": "attributemetadata",
          "mediaType": "application/json"
        },
        "id": "14fbd363-b3f6-11eb-0a80-35ed000000cd",
        "name": "Компания",
        "type": "counterparty",
        "value": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/6054e7f9-b3f2-11eb-0a80-35ed00000075",
            "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
            "type": "counterparty",
            "mediaType": "application/json",
            "uuidHref": "https://online.moysklad.ru/app/#company/edit?id=6054e7f9-b3f2-11eb-0a80-35ed00000075"
          },
          "name": "ООО \"Поставщик\""
        }
      }
    ],
    "positions": {
      "meta": {
        "href": "https://api.moysklad.ru/api/remap/1.2/entity/customerorder/c4c6e6ea-b3f5-11eb-0a80-35ed000000b8/positions",
        "type": "customerorderposition",
        "mediaType": "application/json",
        "size": 2,
        "limit": 1000,
        "offset": 0
      },
      "rows": [
        {
          "meta": {
            "href": null,
            "type": "customerorderposition",
            "mediaType": "application/json"
          },
          "id": null,
          "accountId": "5fc956ad-b3f2-11eb-0a80-1b8a00000000",
          "price": 10000,
          "quantity": 2,
          "reserve": 2,
          "shipped": 0,
          "assortment": {
            "meta": {
              "href": "https://api.moysklad.ru/api/remap/1.2/entity/product/788a1cc7-b3f6-11eb-0a80-35ed000000e2",
              "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/product/metadata",
              "type": "product",
              "mediaType": "application/json",
              "uuidHref": "https://online.moysklad.ru/app/#good/edit?id=78896bd4-b3f6-11eb-0a80-35ed000000e0"
            }
          },
          "vat": 0,
          "discount": 0
        },
        {
          "meta": {
            "href": null,
            "type": "customerorderposition",
            "mediaType": "application/json"
          },
          "id": null,
          "accountId": "5fc956ad-b3f2-11eb-0a80-1b8a00000000",
          "price": 1000,
          "quantity": 1,
          "shipped": 0,
          "assortment": {
            "meta": {
              "href": "https://api.moysklad.ru/api/remap/1.2/entity/service/9d0c9a63-b3f6-11eb-0a80-35ed000000eb",
              "metadataHref": "https://api.moysklad.ru/api/remap/1.2/entity/service/metadata",
              "type": "service",
              "mediaType": "application/json",
              "uuidHref": "https://online.moysklad.ru/app/#good/edit?id=9d0c74c3-b3f6-11eb-0a80-35ed000000e9"
            }
          },
          "vat": 0,
          "discount": 0
        }
      ]
    }
  }
}

```

 Здесь `changeHints` представляет собой массив с подсказками о том, что именно было изменено в редактируемом объекте:
                                        
- `_fields` — стандартные простые и ссылочные поля объекта (название, даты, контрагент и т. п.);  
- `positions` — позиции документа;
- `attributes` — значения дополнительных полей объекта. 
 
 Поле `objectState` — измененное состояние объекта, которое представляет собой JavaScript-объект, соответствующий по структуре ответу JSON API 1.2 на получение того же объекта (документа) с позициями.
 
 Несмотря на то, что структура `objectState` в целом соответствует JSON API 1.2, имеются расхождения:
 
- Поля, обязательные в JSON API 1.2, могут быть не заданы в несохраненном состоянии документа. В качестве значение таких полей в `objectState` передается `null`.
- Числовые поля, которые могут иметь разные типы (целочисленные и с плавающей точкой) в JSON API 1.2, в `objectState` имеют один и тот же тип  [Number](https://developer.mozilla.org/ru/docs/Glossary/Number). Это связано с тем, что `objectState` передается не как JSON, а как JavaScript Object.
- В `objectState` передаются позиции (по аналогии с запросом в JSON API c `expand=positions`): 
  - для документов с листанием списка позиций (на данный момент это **Инвентаризация**) отправляются позиции с текущей страницы. В метаданных позиций `size` содержит общее количество позиций, `offset` — смещение текущей страницы, `limit` — размер страницы (сейчас `100`).
  - для остальных документов передаются все позиции. В метаданных позиций `offset` всегда равен `0`, а `limit` зависит от `size`: `limit = max(size, 1000)`.
- В objectState учитывается URL сервиса — [МойСклад](https://online.moysklad.ru).
- В дополнительных полях типа Файл в `value` содержится имя файла с расширением, в отличие от JSON API 1.2.
- В `attributes` передаются дополнительные поля с заполненным значением, обязательные поля (`required`) и все поля типа Boolean. Необязательные поля без значения не передаются. Флаг `show` на состав `attributes` не влияет.
- На страницах создания (точка расширения `*.create`) часть полей, которые заполняются после первого сохранения документа, могут быть не заполнены — иметь значение `null`:
  - `id`, `accountId`, `created`, `meta`, `href`, `uuidHref` для документа; 
  - `externalCode` для документа, кроме Заказа покупателя, где внешний код может быть заполнен пользователем;
  - `id`, `accountId`, `meta`, `href`, `uuidHref` для позиций документа.
- на страницах создания некоторые поля могут иметь другое значение:
  - `updated` — заполняется временем открытия страницы документа.

  
 Актуальные сведения о поддержке конкретных полей документов в протоколе **change-handler** смотрите в документации JSON API 1.2:

- [Внутренний заказ](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/internalOrder#2-vnutrennij-zakaz)
- [Возврат покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-vozwrat-pokupatelq)
- [Заказ кодов маркировки](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/emissionorder#2-zakaz-kodov-markirovki)
- [Заказ покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-zakaz-pokupatelq)
- [Заказ поставщику](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/purchaseOrder#2-zakaz-postavshiku)
- [Инвентаризация](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/inventory#2-inventarizaciya)
- [Оприходование](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-oprihodowanie)
- [Отгрузка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-otgruzka)
- [Приемка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka)
- [Перемещение](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-peremeschenie)
- [Розничная продажа](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-roznichnaq-prodazha)
- [Списание](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-spisanie)
- [Счет покупателю](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-schet-pokupatelu)
- [Счет поставщика](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-schet-postawschika)

### Валидация состояния редактируемого объекта

Виджет может проверять состояние редактируемого объекта и запрещать хост-окну сохранять объект, если он невалиден. Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **validation-feedback**, который является параметром тега `change-handler`.

> Тег дополнительных протоколов supports с протоколом change-handler

```xml
      <supports>
        <change-handler>
          <validation-feedback/>
        </change-handler>
      </supports>
```

Протокол работает в паре с `change-handler`, то есть виджет, поддерживающий протокол `validation-feedback`, должен отправить сообщение `ValidationFeedback` о валидности документа в ответ на сообщение `Change`.

Если виджет в сообщении `ValidationFeedback` укажет, что документ невалиден, то при попытке сохранить документ пользователь увидит сообщение об ошибке, которое включает в себя наименование виджета.

![useful image](./images/validation-feedback.png)

Валидация запрашивается только у виджета, который загрузился и получил сообщения `Open` и `Change`. Если iframe не загрузился из-за недоступности сервера решения, сетевого таймаута или ошибки HTTP, виджет не участвует в валидации и сохранение проходит без него.

После нажатия кнопки «Сохранить» хост-окно не более 3 секунд ожидает `ValidationFeedback` на последнее сообщение `Change`. Полученный ответ применяется, а при его отсутствии сохранение блокируется и пользователь видит сообщение с названием виджета и адресом электронной почты поддержки вендора. 
В случае тяжелых проверок рекомендуется отвечать на `Change` сначала синхронно (`"valid": false`), а проверки выполнять асинхронно и затем уточнять вердикт.

`ValidationFeedback` применяется, только если его `correlationId` равен `messageId` последнего отправленного сообщения `Change`. Ответы на более ранние сообщения игнорируются без `InvalidMessageError`. Повторный ответ с актуальным `correlationId` перезаписывает предыдущий вердикт, что позволяет уточнить результат после асинхронной проверки.

Вердикт сбрасывается при закрытии виджета, например при уходе со страницы или смене точки встраивания. Откат пользователем изменений документа до исходного состояния вердикт не сбрасывает.

Подробнее о том, для каких точек поддерживается протокол **validation-feedback**, смотрите [здесь](#/developer-guide/app-descriptor#3-dostupnost-dopolnitelnyh-protokolov-v-zavisimosti-ot-tochek-vstraivaniya).

> Сообщение ValidationFeedback — документ валиден (может быть сохранен)

```json
{
  "name": "ValidationFeedback",
  "messageId": 11,
  "correlationId": 10,
  "valid": true
}
```

> Сообщение ValidationFeedback — документ невалиден (не должен быть сохранен)

```json
{
  "name": "ValidationFeedback",
  "messageId": 12,
  "correlationId": 11,
  "valid": false,
  "message": "Пример ошибки от разработчика"
}
```

> Отложенная валидация при длительной проверке (сначала синхронный ответ, потом асинхронный)

```json
{
  "name": "ValidationFeedback",
  "messageId": 13,
  "correlationId": 12,
  "valid": false,
  "message": "Происходит проверка..."
}
```

> Асинхронный ответ после завершения проверки

```json
{
  "name": "ValidationFeedback",
  "messageId": 14,
  "correlationId": 12,
  "valid": true
}
```

Здесь:

- `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом;
- `correlationId` — идентификатор соответствующего сообщения `Change`;
- `valid` — признак валидности документа;
- `message` — сообщение об ошибке. Требуется для случая когда `valid=false`. Максимум 100 символов.

### Изменение состояния редактируемого объекта

Виджет может изменять поля текущего редактируемого объекта посредством передачи сообщения `UpdateRequest` хост-окну.
Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **update-provider**.

> Тег дополнительных протоколов supports с протоколом update-provider

```xml
      <supports>
          <update-provider/>
      </supports>
```

Изменения в этом протоколе, в отличие от JSON API, происходят без сохранения состояния объекта в базе данных МоегоСклада, так же, как если бы они были сделаны самим пользователем. Виджет должен отправлять сообщения `UpdateRequest` преимущественно в качестве реакции на действия пользователя, чтобы предупредить его об изменениях в редактируемом документе.

Сценарий работы:

1. Виджет отправляет хост-окну сообщение `UpdateRequest`, содержащее набор полей документа и/или позиции документа, которые нужно изменить.
2. Хост-окно валидирует содержимое сообщения и отправляет обратно ответ `UpdateResponse`.
3. Если сообщение `UpdateRequest` невалидно, хост-окно отправляет в ответ сообщение `InvalidMessageError`, содержащее описание ошибочных полей.

На каждое сообщение `UpdateRequest` хост-окно всегда отвечает либо `UpdateResponse`, либо `InvalidMessageError` — в том числе если обработка не завершилась по вине хост-окна. Следующие сообщения `UpdateRequest` при этом обрабатываются как обычно.

Ошибки, характерные для протокола **update-provider** (полный перечень см. в разделе [Ошибки при работе с виджетами](#/developer-guide/widget-errors#2-oshibki-pri-rabote-s-vidzhetami)):

- `1002` — ошибка в данных `updateState`: неподдерживаемое поле, неверный тип значения, несуществующий или невалидный идентификатор, несогласованные контрагент, организация, договор и счета. Поля документа не изменены;
- `1005` — документ доступен пользователю только для чтения;
- `1006` — ошибка на стороне МоегоСклада, с данными запроса всё в порядке: обработка не завершилась за отведённое время или произошла внутренняя ошибка. Поля документа не изменены, запрос можно повторить.

> Сообщение UpdateRequest

```json
{
  "name": "UpdateRequest",
  "messageId": 10,
  "updateState": {
    "name": "1",
    "deliveryPlannedMoment": "2021-08-21T12:15:50.333Z",
    "applicable": true,
    "description": null
  }
}
```

Здесь:

- `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом;
- `updateState` — список полей, которые необходимо изменить. Соответствует телу запроса для обновления соответствующего документа в JSON API, смотрите, например, [Заказ покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-zakaz-pokupatelq-izmenit-zakaz-pokupatelq).

> Сообщение UpdateResponse

```json
{
  "name": "UpdateResponse",
  "correlationId": 10
}
```

Здесь:

- `correlationId` — идентификатор соответствующего сообщения `UpdateRequest`.

> Сообщение UpdateRequest для изменения дополнительных полей

```json
{
  "name":"UpdateRequest",
  "messageId":10,
  "updateState":{
    "description": "красивое",
    "attributes":[
      {
        "meta":{
          "href":"https://api.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/f6d39a2b-146f-11ec-0a80-072a002cf678",
          "type":"attributemetadata"
        },
        "name":"Доставлено в срок",
        "type":"boolean",
        "value":true
      },
      {
        "id":"f6d39d12-146f-11ec-0a80-072a002cf679",
        "name":"Срок доставки, дней",
        "type":"long",
        "value":10
      },
      {
        "id":"f6d39d12-146f-11ec-0a80-072a002cf678",
        "value":45.78
      }
    ]
  }
}
```

> Сообщение UpdateRequest для добавления позиций

```json
{
  "name":"UpdateRequest",
  "messageId":10,
  "updateState":{
    "vatIncluded": true,
    "positions": [
      {
        "quantity": 10,
        "price": 100,
        "discount": 0,
        "vat": 0,
        "assortment": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/product/8b382799-f7d2-11e5-8a84-bae5000003a5",
            "type": "product"
          }
        },
        "reserve": 10
      },
      {
        "quantity": 1,
        "price": 200,
        "assortment": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/service/be903062-f504-11e5-8a84-bae50000019a",
            "type": "service"
          }
        },
        "pack": null
      },
      {
        "quantity": 30,
        "price": 300,
        "discount": 0,
        "vat": 18,
        "assortment": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/bundle/c02e3a5c-007e-11e6-9464-e4de00000006",
            "type": "bundle"
          }
        },
        "pack": {
          "id": "1bf22e62-8b47-11e8-56c0-000800000006"
        },
        "reserve": 30
      }
    ]
  }
}
```

> Сообщение UpdateRequest для изменения существующих позиций

```json
{
  "name":"UpdateRequest",
  "messageId":10,
  "updateState":{
    "vatIncluded": true,
    "positions": [
      {
        "id": "be903062-f504-11e5-8a84-bae50000019a",
        "price": 100,
        "discount": -10
      },
      {
        "id": "be903062-f504-11e5-8a84-bae500000123",
        "quantity": 30,
        "price": 300,
        "discount": 0,
        "vat": 18,
        "assortment": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/bundle/c02e3a5c-007e-11e6-9464-e4de00000006",
            "type": "bundle"
          }
        },
        "reserve": 30
      }
    ]
  }
}
```

> Сообщение UpdateRequest для добавления одной новой и сохранения трех  существующих позиций

```json
{
  "name":"UpdateRequest",
  "messageId":10,
  "updateState":{
    "vatIncluded": true,
    "positions": [
      {
        "id": "be903062-f504-11e5-8a84-bae50000019a"
      },
      {
        "id": "0fb51a51-e01d-48da-9035-4b21f5e69055"
      },
      {
        "id": "ef34072d-5fd3-4ac4-b4b9-87458ca61da2"
      },
      {
        "quantity": 1,
        "price": 300,
        "assortment": {
          "meta": {
            "href": "https://api.moysklad.ru/api/remap/1.2/entity/service/c02e3a5c-007e-11e6-9464-e4de00000006",
            "type": "service"
          }
        }
      }
    ]
  }
}
```

**Работа с полями из `updateState`**:

* Список может содержать одно или несколько полей для изменения.
* При изменении значения поля на то же самое, поле в интерфейсе не обновляется и документ не считается измененным. То есть пользователь может закрыть экран редактирования документа без диалога с вопросом «Данные были изменены. Сохранить изменения?». К позициям это не относится: если позиции в запросе есть, список всегда обновляется и документ считается измененным.
* Содержимое поля можно сбросить, указав в качестве его значения `null`. 
* Если пришло несколько сообщений подряд, все они обрабатываются последовательно.
* Поля типа **Дата-время** необходимо передавать с включением информации о часовом поясе, чтобы избежать неопределенности в интерпретации.
* Значения полей типа **Дата-время** всегда округляются до минут, секунды отбрасываются.
* Для значений ссылочных полей обязательными являются `meta.href` и `meta.type`, остальные поля внутри `meta` игнорируются.
* Для одновременного изменения согласованных полей, таких как Организация (Контрагент), Счет, Договор, необходимо, чтобы их значения были совместимы. Счет должен принадлежать указанной организации, договор должен относиться к этой организации и контрагенту. Иначе возникнет ошибка валидации и значения полей в интерфейсе не изменятся.

**Работа с дополнительными полями (attributes)**:

* Для идентификации дополнительного поля необходимо указать `meta.href` либо `id`. Если указаны оба поля, значение берется из `meta.href`.
* Для передачи значения поля служит поле `value`.
* Остальные поля не являются обязательными.
* Пока не поддерживаются дополнительные поля типа Файл.

**Работа с позициями (positions)**:

* При указании позиций в сообщении `UpdateRequest` существующие позиции в документе полностью заменяются позициями из сообщения.
* Для редактирования позиции необходимо использовать `id` существующей позиции, например, получив их в сообщении `Change` или через JSON API.
* При необходимости добавить новые позиции с сохранением существующих можно указать `id` существующих позиций и новые позиции. В результате останутся существующие позиции и добавятся новые.
* До сохранения документа в базе данных у новых позиций отсутствует `id`.
* Позиции добавляются в порядке, который указан в сообщении.

Актуальные сведения о поддержке конкретных полей документов в протоколе **update-provider** смотрите в документации JSON API 1.2:

- [Внутренний заказ](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/internalOrder#2-vnutrennij-zakaz)
- [Заказ кодов маркировки](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/emissionorder#2-zakaz-kodov-markirovki)
- [Заказ покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-zakaz-pokupatelq)
- [Заказ поставщику](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/purchaseOrder#2-zakaz-postavshiku)
- [Инвентаризация](https://dev.moysklad.ru/doc/api/remap/1.2/#/documents/inventory#2-inventarizaciya)
- [Оприходование](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-oprihodowanie)
- [Отгрузка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-otgruzka)
- [Приемка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka)
- [Перемещение](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-peremeschenie)
- [Списание](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-spisanie)
- [Счет покупателю](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-schet-pokupatelu)

Подробнее о том, для каких точек поддерживается протокол **update-provider**, смотрите в [статье](#/developer-guide/app-descriptor#3-dostupnost-dopolnitelnyh-protokolov-v-zavisimosti-ot-tochek-vstraivaniya).
