## Виджеты

Виджет - это плагин с визуальной частью, представляющей собой прямоугольный блок в конкретном месте в UI МоегоСклада. 
Содержимое блока определяется приложением.

### FAQ по виджетам

#### Куда сейчас можно встраивать виджеты?

Список страниц для встраивания виджетов можно увидеть [тут](#blok-widgets).

#### В чем отличия у точек встраивания edit и create?

Виджеты на страницах создания (например в точке встраивания `document.customerorder.create`) имеют ограниченную функциональность 
по сравнению с виджетами на страницах редактирования (`document.customerorder.edit`). 
Это выражается как в меньшем количестве поддерживаемых протоколов, так и в реализации самих протоколов.
Например, в сообщении Change часть полей, которые заполняются после первого сохранения документа (`id`, `created`, `meta` и т.д.) 
будет заполнено значением `null`. 

Поддержка [сервисных протоколов](#blok-serwisnyh-protokolow-uses) виджетами на страницах создания пока не реализована.
Список поддерживаемых дополнительных протоколов в зависимости от точки встраивания можно увидеть [тут](#dostupnost-dopolnitel-nyh-protokolow-w-zawisimosti-ot-tochek-wstraiwaniq).

#### В каком порядке отображаются виджеты?

Если у пользователя установлены сразу несколько приложений с виджетами, встроенными на одну
 страницу МС, то отобразятся все виджеты в порядке, соответствующем расположению родительских
 приложений на витрине. В редакторах, где поддерживается drag-and-drop, пользователь может сам поменять порядок
отображения виджетов.

#### Хочу встроить виджет в точку МоегоСклада, которой нет в списке - что делать?

Если вы хотите встроить виджет в какую-то точку МоегоСклада, но её пока нет в списке доступных точек расширения -
 обращайтесь с предложением 
в Telegram или по электронной почте, мы всегда открыты для таких запросов.


#### Какими могут быть виджеты

Сейчас можно создать только виджеты с  

- фиксированной шириной: 416px - для всего виджета (с рамкой), 384px - для рабочей области (iframe, определяемый
приложением).
- фиксированной высотой: задается в дескрипторе.

Поддерживается два режима отображения виджетов:

- развернутая форма (полная) - виджет отображается с рабочей iframe-областью.
- свернутая форма - рабочая область скрыта.

### Жизненный цикл виджета

Виджет начинает отображаться на странице только после перехода приложения в статус **Activated**.
Если приложение предполагает настройку и статус **SettingsRequired** - виджет отобразится 
после настройки приложения.

При первом открытии страницы с виджетом (в рамках одной вкладки браузера) cистема МоегоСклада 
загружает виджет по HTTP GET-запросом по URL'у, указанному в теге sourceUrl. При этом система 
генерирует (и передает GET-параметром `contextKey`) ключ, по которому виджет получает текущий 
контекст пользователя через [Vendor API](#poluchenie-kontexta-pol-zowatelq-dlq-prilozhenij-s-iframe-chast-u-i-widzhetami).

Прочие данные передаются при помощи [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) в первом и последующих открытиях виджета.

В частности, при каждом открытии виджета система МоегоСклада отображает ранее загруженный iframe 
виджета (без повторной загрузки с сервера вендора) и через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage) передает 
в iframe этого виджета сообщение `Open`.

Без дополнительных настроек виджет отображает содержимое сразу, как только получает 
сообщение `Open`, даже если еще не успел обновить отображаемую информацию. 

В случае, если виджет поддерживает протокол **open-feedback**, система не отображает 
содержимое виджета сразу, а ждет ответного сообщения от виджета о готовности. 
До этого момента внутри виджета отображается заглушка. Когда виджет готов, он 
отправляет сообщение  `OpenFeedback`, после чего система полностью открывает 
виджет пользователю.
 
Если виджет поддерживает протокол **change-handler**, то при редактировании документа пользователем на странице с виджетом 
он оповещается об изменениях, получая сообщение `Change`,
содержащее несохраненное состояние документа. 
 
Если виджет поддерживает протокол **update-provider**, то при редактировании документа пользователем на странице с виджетом 
он может изменять несохраненное состояние документа, отправляя сообщение `UpdateRequest` со списком полей, которые необходимо изменить. 
 
При сохранении страницы с виджетом, если виджет, который находится на экране редактирования сущности, 
поддерживает протокол **save-handler**, то он оповещается о факте сохранения объекта пользователем, 
получая сообщение `Save`.

Если виджет поддерживает протокол **dirty-state**, он (виджет) может сообщить хост-окну, 
что в виджете есть несохраненные изменения. Для этого виджет отправляет хост-окну 
сообщение `SetDirty`. Виджет может отправить хост-окну сообщение `ClearDirty`,
после чего диалог подтвержения закрытия окна не будет появляться (если, конечно, 
отсутствуют несохраненные изменения в самом UI МоегоСклада или в других виджетах).

Внутренний dirty-флаг для виджета в хост-окне сбрасывается при открытии
(при отправке сообщения `Open`) - т.е. хост-окно считает, что в виджете нет несохраненных изменений.
 
Поддержку виджетом протоколов **open-feedback**, **save-handler**, **dirty-state**, **change-handler** необходимо указать в [дескрипторе](#deskriptor-prilozheniq) 
приложения.

### Как работают виджеты

#### Описание конфигурации виджетов приложения в дескрипторе

Виджеты доступны для серверных приложений с дескриптором версии v2. 

Пример дескриптора приложения с виджетом в карточке контрагента расположен в правой части экрана.

> Дескриптор приложения с виджетом в карточке контрагента


```xml
   <ServerApplication xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2
         https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
       <iframe>...</iframe>
       <vendorApi>...</vendorApi>
       <access>...</access>
       <widgets>
           <entity.counterparty.edit>
               <sourceUrl>https://b2b.moysklad.ru/widget/counter-party</sourceUrl>
               <height>
                   <fixed>28px</fixed>
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

Подробнее со структурой дескриптора для приложения с виджетом можно ознакомиться в
разделе [Дескриптор приложений](#deskriptor-prilozheniq).

В результате после установки и настройки пользователем приложения с дескриптором из примера виджет отображается 
на карточке контрагента:

![useful image](widget-counterparty-page.png)

#### Загрузка виджета на странице

Виджет на странице загружается в iframe по URL, указанному в теге 
`<sourceUrl>...</sourceUrl>` виджета в [дескрипторе приложения](#deskriptor-prilozheniq).

Ширина содержимого виджета одинакова для виджетов всех приложений и равна 400px, 
а высота содержимого виджета статически указывается разработчиком в дескрипторе 
приложения (в данном примере 61px).

![useful image](widget-size.png)

Так же, как и для основной iframe-части приложения, виджету GET-параметром передается 
`contextKey`, по которому через [Vendor API](#blok-vendorapi) можно получить информацию о текущем 
пользователе.

Пока происходит загрузка виджета - отображается ненавязчивый лоадер.
#### Кэширование виджетов

Система виджетов в МоемСкладе реализована таким образом, чтобы, по-возможности, 
загрузить виджет только один раз при первом открытии страницы с виджетом 
(в рамках одной вкладки браузера) и далее кэшировать iframe c загруженном в него
виджетом, переиспользуя его во всех последующих (в рамках одной вкладки
браузера) открытиях страницы с виджетом.

Несмотря на стремление к идеальному кэшированию - оно не гарантировано. 
То есть хост-окно может:

- физически создать несколько экземпляров iframe’ов для одной и той же 
точки расширения в рамках одной вкладки браузера (по тем или иным техническим 
причинам), причем эти экземпляры могут существовать одновременно
- не кэшировать iframe виджета после загрузки

#### Открытие виджета

При открытии пользователем страницы с виджетом хост-окно отображает iframe
виджета (только что загруженный или ранее закэшированный) и передает в
этот iframe виджета сообщение `Open` через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage).

Пример сообщения `Open` cм. в правой части экрана.

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

- `extensionPoint` - текущая точка расширения;
- `objectId` - идентификатор текущего документа или сущности. Для виджета отображаемого на экране создания значение будет `null`;
- `displayMode` - режим отображения виджета. В настоящее время может принимать только одно значение `expanded`.

Виджет при получении сообщения `Open` может, например, обратиться на сервер 
за данными для указанного объекта `objectId` и отобразить их пользователю.

**Примечание**: в сообщении Open передается идентификатор текущей открытой сущности в карточке (который отображается в URL браузера в параметре `id`). 
Несмотря на то, что для сущностей Товар, Услуга, Комплект и Модификация этот идентификатор отличается от используемого в remap API, 
запрос по нему по-прежнему будет работать (при этом сервер будет использовать [редирект](https://developer.mozilla.org/ru/docs/Web/HTTP/Status/308)). 
Пример запроса для Товара `https://online.moysklad.ru/app/#good/edit?id=9e73d736-a0de-11e9-9109-f8fc00095c7f` приведен в правой части (часть вывода для упрощения опущена).

> Ответ на запрос получения Товара  

```shell
curl -X GET --location "https://online.moysklad.ru/api/remap/1.2/entity/product/9e73d736-a0de-11e9-9109-f8fc00095c7f"     -H "Content-Type: application/json"     -H "Authorization: Bearer ..." -v 

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
< Location: https://online.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81
< X-Lognex-Retry-TimeInterval: 3000
< X-RateLimit-Remaining: 44
< X-RateLimit-Limit: 45
< Strict-Transport-Security: max-age=15552000
< 
* Connection #1 to host online.moysklad.ru left intact
* Issue another request to this URL: 'https://online.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81'
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
    "href" : "https://online.moysklad.ru/api/remap/1.2/entity/product/9e73e41d-a0de-11e9-9109-f8fc00095c81",
    "metadataHref" : "https://online.moysklad.ru/api/remap/1.2/entity/product/metadata",
    "type" : "product",
    "mediaType" : "application/json",
    "uuidHref" : "https://online.moysklad.ru/app/#good/edit?id=9e73d736-a0de-11e9-9109-f8fc00095c7f"
  },
  "id" : "9e73e41d-a0de-11e9-9109-f8fc00095c81",
  ...
}
```


#### Протокол обратной связи при открытии виджета

По умолчанию при открытии закэшированного виджета его содержимое отображается сразу.

Если виджет при открытии делает обращение к серверу, то может быть видна 
небольшая задержка и в это время будет отображается прежнее состояние/содержание 
виджета (например, данные для прошлого контрагента).

Протокол обратной связи позволяет виджету явно сообщить хост-окну в какой именно 
момент отобразить содержимое виджета. До этого содержимое виджета будет закрыто 
ненавязчивым лоадером:

![useful image](loader-in-widget.png)

> Тег дополнительных протоколов supports с протоколом open-feedback


```xml
    <supports>
        <open-feedback/>
    </supports>
```

Для переключения хост-окна на использование протокола обратной связи при открытии виджета 
в дескрипторе для виджета надо явно указать поддержку дополнительного протокола **open-feedback**. Пример
тега дополнительных протоколов supports с указанным в нем протоколом **open-feedback** см. в правой части экрана.



Виджет передает сообщение `OpenFeedback` хост-окну в качестве сигнала готовности содержимого 
виджета для отображения пользователю. Пример сообщения  `OpenFeedback` - в правой части экрана.

> Cообщение OpenFeedback

```json 
{
  "name": "OpenFeedback",
  "correlationId": 12345
}
```

Здесь `correlationId` содержит значение `messageId` ранее полученного сообщения `Open`.

Хост-окно, получив сообщение `OpenFeedback`, отображает содержимое виджета пользователю 
(убирает ненавязчивый лоадер).

#### Сохранение пользователем редактируемого объекта

Хост-окно может оповещать виджет о факте сохранения редактируемого объекта. 
Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **save-handler**.

  > Тег дополнительных протоколов supports с протоколом save-handler
  
  ```xml
      <supports>
          <save-handler/>
      </supports>
  ```
 
 Хост-окно отправляет виджету сообщение `Save` (через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)) 
 при сохранении редактируемого объекта после сохранения объекта в БД (то есть на момент получения 
 виджетом сообщения Save сохраненное состояние объекта уже доступно через JSON API).
 
 Сохранение редактируемого объекта инициируется пользователем:
 
 - при явном нажатии на кнопку “Сохранить”, в том числе при сохранении объекта без фактического внесения изменений
 
 - при покидании объекта и его явном сохранении через диалог подтверждения сохранения 
 изменений, в том числе при листании кнопками-стрелочками на соседние объекты
 
 - при автоматическом сохранении изменений закрываемого объекта (например, при создании связанного 
 документа Отгрузки из Заказа покупателя)
 
 Пример сообщения `Save` cм. в правой части экрана.
 
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

- `extensionPoint` - текущая точка расширения;
- `objectId` - идентификатор текущего документа или сущности (аналогичен идентификатору в сообщении Open).


#### Признак несохраненного состояния виджета

> Тег дополнительных протоколов supports с протоколом dirty-state
  
```xml
  <supports>
      <dirty-state/>
  </supports>
```
Хост-окно поддерживает подтверждение закрытия окна пользователем, если он изменил данные 
в форме виджета, но не сохранил их. Для этого в дескрипторе для виджета 
нужно объявить поддержку опционального протокола **dirty-state**.

 
> Сообщение SetDirty

```json
    {
      "name": "SetDirty",
      "messageId": 12,
      "openMessageId": 7
    }
```
После внесения пользователем изменений в виджете, он отправляет хост-окну сообщение `SetDirty`. 
Пример сообщения SetDirty - в правой части экрана.
Здесь openMessageId содержит значение messageId ранее полученного сообщения Open.

Система учитывает, что в виджете есть несохраненные изменения. Далее, если пользователь нажимает кнопку “Закрыть“ (или другим способом пытается уйти с формы редактирования), 
система отображает диалог подтверждения сохранения изменений:

<img src=images/confirm-save-popup.png height="70%" width="70%">

> Сообщение ClearDirty

```json
    {
      "name": "ClearDirty",
      "messageId": 13
    }
```
Если виджет после отправки `SetDirty` отправляет хост-окну сообщение `ClearDirty`, 
то Система не учитывает данный виджет при отображении диалога подтверждения сохранения
 изменений (т.е., если отсутствуют прочие несохраненные изменения самого объекта 
 или в других виджетах - Система не запрашивает диалог подтверждения сохранения изменений 
при закрытии редактируемого объекта).

#### Получение состояния редактируемого объекта

Хост-окно может оповещать виджет об изменениях несохраненного состояния редактируемого объекта. 
Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **change-handler**.

  > Тег дополнительных протоколов supports с протоколом change-handler
  
  ```xml
      <supports>
          <change-handler/>
      </supports>
  ```
 
 Хост-окно отправляет виджету сообщение `Change` (через [postMessage](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)), 
 содержащее несохраненное состояние документа, при редактировании документа пользователем.
 
 Отправка сообщения `Change` инициируется при следующих действиях пользователя:
 
 - при изменении полей документа (в т.ч. дополнительных полей) путём редактирования/выбора значения в селекторе
 - при добавлении/удалении/редактировании позиций документа
 
 Отправка сообщения `Change` **не происходит** в следующих случаях:
 
 - при открытии экрана редактирования документа
 - при изменении состояния документа в результате сохранения пользователем
 - при изменении полей, которые не поддерживаются
 - если при редактировании значение редактируемого поля не изменилось (т. е. при отсутствии реальных изменений)
 
 
 Узнать, для каких точек поддерживается протокол **change-handler**, можно [тут](#dostupnost-dopolnitel-nyh-protokolow-w-zawisimosti-ot-tochek-wstraiwaniq).

 Пример сообщения `Change` cм. в правой части экрана. 
 Здесь `changeHints` представляет собой массив с подсказками о том, что именно было изменено в редактируемом объекте:
                                        
- `_fields` - стандартные простые и ссылочные поля объекта (название, даты, контрагент и т. п.)  
- `positions` - позиции документа
- `attributes` - значения доп. полей объекта 
 
 Поле `objectState` - изменённое состояние объекта, которое представляет собой JavaScript-объект, соответствующий по структуре ответу JSON API 1.2 на получение того же объекта (документа) с позициями.
 
 Несмотря на то, что структура `objectState` в целом соответствует JSON API 1.2, имеются расхождения:
 
- Поля, обязательные в JSON API 1.2, могут быть не заданы в несохраненном состоянии документа. В качестве значение таких полей в `objectState` передаётся `null`.
- Числовые поля, которые могут иметь разные типы (целочисленные и с плавающей точкой) в JSON API 1.2, в `objectState` имеют один и тот же тип  [Number](https://developer.mozilla.org/ru/docs/Glossary/Number). 
 Это связано с тем, что `objectState` передаётся не как JSON, а как JavaScript Object.
- В `objectState` передаётся документ со всеми позициями, что в целом соответствует  запросу в JSON API c `expand=positions`. При этом в метаданных позиций документа всегда `offset=0`,
  а `limit` зависит от  `size`: `limit=1000`, если `size <= 1000` и `limit=size` если `size > 1000`.
- В objectState учитывается url сервиса – [МойСклад](https://online.moysklad.ru) или [Моя Торговля](https://online.sb-mt.ru)
- В доп. полях типа Файл в `value` содержится имя файла с расширением, в отличие от JSON API 1.2
- На страницах создания (точка расширения `*.create`) часть полей, которые заполняются после первого сохранения документа, могут быть не заполнены (иметь значение `null`):
  - `id`, `accountId`, `created`, `meta`, `href`, `uuidHref` для документа;
  - `externalCode` для документа (кроме Заказа покупателя, где внешний код может быть заполнен пользователем);
  - `id`, `accountId`, `meta`, `href`, `uuidHref` для позиций документа.
- На страницах создания некоторые поля могут иметь другое значение:
  - `updated` - заполняется временем открытия страницы документа.

  
 Актуальные сведения о поддержке конкретных полей документов в протоколе **change-handler** - см. в документации JSON API 1.2.

- [Заказ покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-zakaz-pokupatelq)
- [Оприходование](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-oprihodowanie)
- [Отгрузка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-otgruzka)
- [Приемка](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-priemka)
- [Перемещение](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-peremeschenie)
- [Списание](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-spisanie)
- [Счет покупателю](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-schet-pokupatelu)
- [Счет поставщика](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-schet-postawschika).

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
      "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/c4c6e6ea-b3f5-11eb-0a80-35ed000000b8",
      "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
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
        "href": "https://online.moysklad.ru/api/remap/1.2/entity/store/605491e4-b3f2-11eb-0a80-35ed00000074",
        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/store/metadata",
        "type": "store",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#warehouse/edit?id=605491e4-b3f2-11eb-0a80-35ed00000074"
      }
    },
    "rate": {
      "currency": {
        "meta": {
          "href": "https://online.moysklad.ru/api/remap/1.2/entity/currency/6055a619-b3f2-11eb-0a80-35ed00000079",
          "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/currency/metadata",
          "type": "currency",
          "mediaType": "application/json",
          "uuidHref": "https://online.moysklad.ru/app/#currency/edit?id=6055a619-b3f2-11eb-0a80-35ed00000079"
        }
      }
    },
    "organization": {
      "meta": {
        "href": "https://online.moysklad.ru/api/remap/1.2/entity/organization/6051401c-b3f2-11eb-0a80-35ed00000072",
        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/organization/metadata",
        "type": "organization",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#mycompany/edit?id=6051401c-b3f2-11eb-0a80-35ed00000072"
      }
    },
    "agent": {
      "meta": {
        "href": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/60550738-b3f2-11eb-0a80-35ed00000077",
        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
        "type": "counterparty",
        "mediaType": "application/json",
        "uuidHref": "https://online.moysklad.ru/app/#company/edit?id=60550738-b3f2-11eb-0a80-35ed00000077"
      }
    },
    "state": {
      "meta": {
        "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/states/60850d6a-b3f2-11eb-0a80-35ed00000097",
        "type": "state",
        "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata",
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
          "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fb3ad9-b3f6-11eb-0a80-35ed000000cb",
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
          "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fbcb79-b3f6-11eb-0a80-35ed000000cc",
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
          "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/14fbd363-b3f6-11eb-0a80-35ed000000cd",
          "type": "attributemetadata",
          "mediaType": "application/json"
        },
        "id": "14fbd363-b3f6-11eb-0a80-35ed000000cd",
        "name": "Компания",
        "type": "counterparty",
        "value": {
          "meta": {
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/6054e7f9-b3f2-11eb-0a80-35ed00000075",
            "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
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
        "href": "https://online.moysklad.ru/api/remap/1.2/entity/customerorder/c4c6e6ea-b3f5-11eb-0a80-35ed000000b8/positions",
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
              "href": "https://online.moysklad.ru/api/remap/1.2/entity/product/788a1cc7-b3f6-11eb-0a80-35ed000000e2",
              "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/product/metadata",
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
              "href": "https://online.moysklad.ru/api/remap/1.2/entity/service/9d0c9a63-b3f6-11eb-0a80-35ed000000eb",
              "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/service/metadata",
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

#### Валидация состояния редактируемого объекта

Виджет может проверять (валидировать) состояние редактируемого объекта и запрещать хост-окну сохранять объект, если он невалиден.
Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **validation-feedback**, который является параметром тега `change-handler`.

> Тег дополнительных протоколов supports с протоколом change-handler

  ```xml
      <supports>
        <change-handler>
          <validation-feedback/>
        </change-handler>
      </supports>
  ```
Протокол работает в паре с `change-handler`, т.е. виджет поддерживающий протокол `validation-feedback` 
должен отправить сообщение `ValidationFeedback` о валидности документа в ответ на сообщение `Change`.

Если виджет в сообщении `ValidationFeedback` укажет, что документ невалиден, 
то при попытке сохранить документ пользователь увидит сообщение об ошибке, которое включает в себя наименование виджета:

![useful image](validation-feedback.png)

Если виджет по какой-то причине не отправит `ValidationFeedback` (или отправит некорректное сообщение), то **пользователь не сможет сохранить документ**. 

Узнать, для каких точек поддерживается протокол **validation-feedback**, можно [тут](#dostupnost-dopolnitel-nyh-protokolow-w-zawisimosti-ot-tochek-wstraiwaniq).

Пример сообщений `ValidationFeedback` cм. в правой части экрана.
Здесь:

- `messageId` - целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет - хост-окно. Назначается виджетом;
- `correlationId` - идентификатор соответствующего сообщения `Change`;
- `valid` - признак валидности документа;
- `message` - сообщение об ошибке. Требуется для случая когда `valid=false`. Максимум 100 символов.

> Сообщение ValidationFeedback - документ валиден (может быть сохранен)

 ```json
{
  "name": "ValidationFeedback",
  "messageId": 11,
  "correlationId": 10,
  "valid": true
}
```

> Сообщение ValidationFeedback - документ невалиден (не должен быть сохранен)

 ```json
{
  "name": "ValidationFeedback",
  "messageId": 12,
  "correlationId": 11,
  "valid": false,
  "message": "Пример ошибки от вендора"
}
```


#### Изменение состояния редактируемого объекта

> Тег дополнительных протоколов supports с протоколом update-provider

  ```xml
      <supports>
          <update-provider/>
      </supports>
  ```

Виджет может изменять поля текущего редактируемого объекта посредством передачи сообщения `UpdateRequest` хост-окну.
Для этого в дескрипторе для виджета нужно объявить поддержку опционального протокола **update-provider**.

Изменения в данном протоколе, в отличие от JSON API, происходят без сохранения состояния объекта в БД МоегоСклада,
аналогично тому, как если бы они были сделаны самим пользователем.
Предполагается, что сообщения `UpdateRequest` будут отправляться виджетом преимущественно как реакция на действия пользователя
(чтобы для пользователя не были сюрпризом неожиданные изменения редактируемого им документа).

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

Сценарий работы:

1. Виджет отправляет хост-окну сообщение `UpdateRequest`, содержащее набор полей документа и/или позиции документа, которые нужно изменить.
2. Хост-окно валидирует содержимое сообщения и отправляет обратно ответ `UpdateRequest`.
3. Если сообщение `UpdateRequest` невалидно, хост-окно отправит в ответ сообщение `InvalidMessageError`, содержащее описание ошибочных полей.


Примеры сообщений `UpdateRequest` cм. в правой части экрана.

Здесь

- `messageId` - целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет - хост-окно. Назначается виджетом;
- `updateState` - список полей, которые необходимо изменить. Соответствует телу запроса для обновления соответствующего документа в JSON API (см. например [Заказ покупателя](https://dev.moysklad.ru/doc/api/remap/1.2/documents/#dokumenty-zakaz-pokupatelq-izmenit-zakaz-pokupatelq))  


Пример сообщения `UpdateResponse` cм. в правой части экрана.

> Сообщение UpdateResponse

```json
{
  "name": "UpdateResponse",
  "correlationId": 10
}
```
Здесь

- `correlationId` - идентификатор соответствующего сообщения `UpdateRequest`.

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
          "href":"https://online.moysklad.ru/api/remap/1.2/entity/customerorder/metadata/attributes/f6d39a2b-146f-11ec-0a80-072a002cf678",
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
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/product/8b382799-f7d2-11e5-8a84-bae5000003a5",
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
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/service/be903062-f504-11e5-8a84-bae50000019a",
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
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/bundle/c02e3a5c-007e-11e6-9464-e4de00000006",
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
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/bundle/c02e3a5c-007e-11e6-9464-e4de00000006",
            "type": "bundle"
          }
        },
        "reserve": 30
      }
    ]
  }
}
```

> Сообщение UpdateRequest для добавления одной новой и сохранения 3-х существующих позиций

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
            "href": "https://online.moysklad.ru/api/remap/1.2/entity/service/c02e3a5c-007e-11e6-9464-e4de00000006",
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
* При изменении значения поля на то же самое, поле на UI не обновляется и документ не считается измененным - 
т.е. пользователь может закрыть экран редактирования документа без диалога с вопросом “Данные были изменены. Сохранить изменения?”. 
К позициям это не относится: если позиции в запросе есть - список всегда обновляется и документ считается измененным.
* Содержимое поля можно сбросить указав в качестве его значения `null`. 
* Если пришло несколько сообщений подряд, все они обрабатываются последовательно.
* Поля типа _Дата-время_ необходимо передавать с включением информации о часовом поясе, чтобы избежать неопределенности в интерпретации.
* Значения полей типа _Дата-время_ всегда округляются до минут (секунды отбрасываются), по аналогии с UI.
* Для значений ссылочных полей обязательными являются `meta.href` и `meta.type`, остальные поля внутри `meta` игнорируются.
* Для одновременного изменения согласованных полей, таких как Организация (Контрагент), Счет и Договор необходимо чтобы их значения были совместимы: 
счет должен принадлежать указанной организации, договор должен относиться к этой организации и контрагенту. 
В противном случае - возникнет ошибка валидации и значения полей на UI не изменятся.

**Работа с дополнительными полями (attributes)**:

* Для идентификации дополнительного поля необходимо указать `meta.href` либо `id` (если указаны оба поля, значение берется из `meta.href`).
* Для передачи значения поля служит поле `value`.
* Остальные поля не являются обязательными.
* Пока не поддерживаются доп. поля типа Файл.

**Работа с позициями (positions)**:

* При указании позиций в сообщении `UpdateRequest` существующие позиции в документе полностью заменяются позициями из сообщения.
* Для редактирования позиции необходимо использовать `id` существующей позиции (например, получив их в сообщении `Change` или через JSON API).
* При необходимости добавить новые позиции с сохранением существующих можно указать `id` существующих позиций и новые позиции - в результате останутся существующие позиции и добавятся новые.
* До сохранения документа в БД у новых позиций отсутствует `id`.
* Позиции добавляются в порядке, который указан в сообщении.

Узнать, для каких точек поддерживается протокол **update-provider**, можно [тут](#dostupnost-dopolnitel-nyh-protokolow-w-zawisimosti-ot-tochek-wstraiwaniq).

### Сервисы хост-окна

В настоящий момент сервисы хост-окна представлены следующими:

* [Селектор группы товаров](#selektor-gruppy-towarow)
* [Стандартные диалоги](#standartnye-dialogi)
* [Протокол навигации](#protokol-nawigacii)

#### Селектор группы товаров

> Дескриптор приложения с виджетом, использующим селектор группы товаров

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
        <expand>true</expand>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
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
</ServerApplication>
```

> Дескриптор приложения, у которого iframe-часть и popup используют селектор группы товаров

```xml
<ServerApplication xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/iframe.html</sourceUrl>
    <expand>true</expand>
    <uses>
      <good-folder-selector/>
    </uses>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://online.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <popups>
    <popup>
      <name>coolPopup</name>
      <sourceUrl>https://vendorurl.coolpopup.ru</sourceUrl>
      <uses>
        <good-folder-selector/>
      </uses>
    </popup>
  </popups>
</ServerApplication>
```

Позволяет виджетам, основной iframe-части и попап-окнам приложений переиспользовать существующий в МоемСкладе селектор группы 
товаров с получением ими результата выбора пользователя.
Чтобы виджет, iframe-часть или попап-окно начали поддерживать селектор в дескрипторе, необходимо добавить блок: 

```
<uses>
    <good-folder-selector/>
</uses>
```

соответственно в блоки `widgets`, `iframe` или `popup`. Примеры справа.

В частности далее рассмотрим кейс с виджетом.
Когда виджет отправляет хост-окну сообщение `SelectGoodFolderRequest`(через Window.postMessage), 
хост-окно запрашивает у пользователя выбор группы товаров, используя встроенный в МойСклад попап-селектор:

![useful image](good-folder-selector.png)

> Cообщение SelectGoodFolderRequest

```json 
{
  "name": "SelectGoodFolderRequest",
  "messageId": 12345
}
```

Здесь `messageId` - целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет - 
хост-окно. Назначается виджетом.

После совершения пользователем выбора группы товаров или отказа от него хост-окно передает виджету результат 
действий пользователя в сообщении `SelectGoodFolderResponse`. 

> Cообщение SelectGoodFolderResponse(Пользователь выбрал группу товаров, имеющую идентификатор 8e9512f3-111b-11ea-0a80-02a2000a3c9c)

```json 
{
  "name": "SelectGoodFolderResponse",
  "correlationId": 12345,
  "selected": true,
  "goodFolderId": "8e9512f3-111b-11ea-0a80-02a2000a3c9c"
}
```

Здесь:

+ `correlationId` - идентификатор соответствующего сообщения `SelectGoodFolderRequest`;
+ `selected` - признак наличия выбора;
+ `goodFolderId` - идентификатор выбранной группы товаров.

> Cообщение SelectGoodFolderResponse(Пользователь отменил выбор)

```json 
{
  "name": "SelectGoodFolderResponse",
  "correlationId": 12345,
  "selected": false
}
```

#### Стандартные диалоги

> Дескриптор с виджетом, использующим стандартные диалоги

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
        <expand>true</expand>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
    <widgets>        
        <entity.counterparty.edit>            
            <sourceUrl>https://example.com/widget.php</sourceUrl>            
            <height>                
                <fixed>150px</fixed>            
            </height>
            <uses>
                <standard-dialogs/>
            </uses>                  
        </entity.counterparty.edit>    
    </widgets>
</ServerApplication>
```

Позволяет виджетам приложений использовать существующие в МоемСкладе стандартные диалоги.
Чтобы виджет начал поддерживать протокол в дескрипторе необходимо добавить блок:
```
<uses>
    <standard-dialogs/>
</uses>
```

Когда виджет хочет показать пользователю стандартный диалог, он отправляет хост-окну сообщение `ShowDialogRequest`, 
указывая в нем текст сообщения и кнопки, которые необходимо отобразить пользователю. Пример:

![useful image](standard-dialog-with-two-buttons.png)


> Cообщение ShowDialogRequest

```json 
{
  "name": "ShowDialogRequest",
  "messageId": 12345,
  "dialogText": "Учетная запись будет удалена. Вы хотите продолжить?",
  "buttons": [
    {"name": "Yes", "caption": "Да, удалить"},
    {"name": "No", "caption": "Нет"}
  ]
}
```

Параметры сообщения `ShowDialogRequest`:

* `messageId` - целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет - 
хост-окно. Назначается виджетом;
* `dialogText` - текст сообщения, который нужно отобразить пользователю МС. 
Максимальный размер ограничен 4096 символами. HTML-теги не допускаются (будут экранированы);
* `buttons` - список кнопок в диалоге, элементами которого являются объекты с двумя обязательными полями: 
`name` - имя кнопки (будет возвращено в сообщении `ShowDialogResponse`), 
`caption` - текст, отображаемый на кнопке. Максимальный размер поля `caption` ограничен 100 символами. 
HTML-теги в нем не допускаются (будут экранированы).

После нажатия пользователем кнопки в диалоге или принудительном закрытии (через "крестик") хост-окно передает виджету результат 
действий пользователя в сообщении `ShowDialogResponse`.

> Cообщение ShowDialogResponse (Пользователь нажимает кнопку "Нет")

```json 
{
  "name": "ShowDialogResponse",
  "correlationId": 12345,
  "buttonName": "No",
  "dialogResolution": "normal"
}
```

Параметры ответа `ShowDialogResponse`:

+ `correlationId` - идентификатор соответствующего сообщения `ShowDialogResponse`;
+ `dialogResolution` - признак выбора: `normal` - означает, что была нажата одна из кнопок, 
`closedByUser` - означает, что диалог был завершен принудительно;
+ `buttonName` - имя выбранной кнопки.

> Cообщение ShowDialogResponse (Пользователь закрыл диалог через "крестик")

```json 
{
  "name": "ShowDialogResponse",
  "correlationId": 12345,
  "dialogResolution": "closedByUser"
}
```
**Примечание**: 
В последних версиях Google Chrome (92.0 и выше) использование браузерных диалоговых окон 
через вызовы Window.alert(), Window.confirm() из iframe [запрещено](https://www.chromestatus.com/feature/5148698084376576). 
В связи с этим, крайне желательно использовать сервис стандартных диалогов МС.

#### Протокол навигации

> Дескриптор с виджетом, использующим протокол навигации

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
        <expand>true</expand>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
    <widgets>        
        <entity.counterparty.edit>            
            <sourceUrl>https://example.com/widget.php</sourceUrl>            
            <height>                
                <fixed>150px</fixed>            
            </height>
            <uses>
                <navigation-service/>
            </uses>                  
        </entity.counterparty.edit>    
    </widgets>
</ServerApplication>
```
> Дескриптор приложения, у которого iframe-часть и popup используют протокол навигации

```xml
<ServerApplication xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/iframe.html</sourceUrl>
    <expand>true</expand>
    <uses>
      <navigation-service/>
    </uses>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://online.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <popups>
    <popup>
      <name>coolPopup</name>
      <sourceUrl>https://vendorurl.coolpopup.ru</sourceUrl>
      <uses>
        <navigation-service/>
      </uses>
    </popup>
  </popups>
</ServerApplication>
```
Позволяет виджетам, iframe-части и попап-окнам приложений осуществлять переход на другую страницу МоегоСклада и открывать МойСклад в новой вкладке.
Чтобы виджет, iframe или попап начали поддерживать протокол навигации в дескрипторе необходимо добавить блок:
```
<uses>
    <navigation-service/>
</uses>
```
соответственно в блоки `widgets`, `iframe` или `popup`. Примеры справа.

В частности далее рассмотрим кейс с виджетом. Когда виджет отправляет хост-окну сообщение `NavigateRequest`(через Window.postMessage),
хост-окно переходит на другую страницу МоегоСклада или открывает в новой вкладке браузера нужную страницу МоегоСклада.

> Cообщение NavigateRequest

```json 
{
  "name": "NavigateRequest",
  "messageId": 12345,
  "path": "#good/edit?id=e8a46787-0ff4-11ec-0a80-1eb200000740",
  "target": "blank"
}
```

Параметры сообщения `NavigateRequest`:

* `messageId` - целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет -
хост-окно. Назначается виджетом.
* `path` - путь до страницы, на которую виджет хочет осуществить переход. Например, чтобы осуществить переход пользователя на страницу реестра заказов 
покупателя https://online.moysklad.ru/app/#customerorder, нужно передать `#customerorder`.
* `target` - вид навигации. Может принимать одно из двух значений: `self` - переход в текущей вкладке, `blank` - открытие в новой вкладке. 

Если валидация сообщения пройдет успешно, то перед переходом пользователя будет отправлен `NavigateResponse` обратно в виджет. 

> Cообщение NavigateResponse

```json 
{
  "name": "NavigateResponse",
  "correlationId": 12345 
}
```

Параметры ответа `NavigateResponse`:

+ `correlationId` - идентификатор соответствующего сообщения `NavigateRequest`.

При навигации из попапа в текущей вкладке (`target` имеет значение `self`) произойдет переход, но попап будет поверх страницы. Если необходимо, чтобы после перехода попап закрывался можно использовать сообщение `ClosePopup`. Подробнее в разделе [Кастомные попапы](#kastomnye-popapy-modal-nye-okna).

### Кастомные попапы (модальные окна)

> Дескриптор с виджетом и iframe-частью, использующие кастомные попапы

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
        <expand>true</expand>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
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

Использование модальных окон позволяет виджетам (которые имеют фиксированную высоту и ширину) и iframe-части
расширить свою функциональность путем отображения всплывающего (попап) окна, аналогичного существующим в МоемСкладе, 
с возможностью передачи данных как от виджета и iframe в попап-окно, так и в обратном направлении.

Попап-окна отображаются развернутыми на весь экран, что позволяет показать в них больший или дополнительный объем информации. 
При этом МС отрисовывает только заголовок окна с кнопкой закрытия в верхнем правом углу (в качестве заголовка используется название приложения).
Все остальное должно быть отображено страницей вендора (страница отображаемая внутри iframe попапа).

Далее рассмотрим модальные окна на примере виджетов, для iframe-части аналогично. Для использования виджетом 
попап-окон необходимо добавить блок 
```
<popups>
    ...
</popups>
```
в [дескрипторе приложения](#blok-popups). Пример дескриптора с блоком `popups` можно увидеть справа.

Виджет может отобразить одно из попап-окон, отправив сообщение `ShowPopupRequest` с именем выбранного попапа хост-окну.
Пример такого сообщения можно увидеть справа. 
Здесь:

* `messageId` - идентификатор сообщения;
* `popupName` - имя открываемого попапа;
* `popupParameters` - опциональные параметры, передаваемые попапу виджетом (может иметь любой тип, в том числе `null`).

МойСклад проверяет сообщение `ShowPopupRequest` и, если сообщение валидно, то отображает попап-окно, 
загружая страницу попапа по адресу `sourceUrl` в iframe с передачей `contextKey` в GET-параметре (аналогично загрузке виджета).
Значение `sourceUrl` загружается из соответствующего элемента списка попап-окон `<popups>` в дескрипторе. 
При этом поиск производится по переданному в сообщении `popupName`.

После загрузки попапа хост-окно отправляет попап-окну сообщение `OpenPopup` (набор полей тот же что и в `ShowPopupRequest`).
При этом `messageId` в данном сообщении свой, а не тот, что был передан в сообщении `ShowPopupRequest`.
  
Когда необходимо закрыть модальное окно, попап отправляет сообщение `ClosePopup` хост-окну.
Пример такого сообщения можно увидеть справа. Здесь:

* `messageId` - идентификатор сообщения;
* `popupResponse` - опциональный ответ, возвращаемый виджету (может иметь любой тип, в том числе `null`).

МойСклад в свою очередь отправляет сообщение `ShowPopupResponse` виджету, открывшему попап-окно.
Пример такого сообщения можно увидеть справа. Здесь:

* `correlationId` - идентификатор соответствующего сообщения ShowPopupRequest;
* `popupName` - имя открывавшегося попапа;
* `popupResolution` - вариант, по которому произошло закрытие попапа:
                      `normal` - нормальное закрытие попапа по `ClosePopup`,
                      `closedByUser` - закрытие попапа пользователем путем нажатия на крестик;
* `popupResponse` - опциональный ответ, возвращаемый виджету.

Страницы попап-окон кэшируются аналогично кэшированию виджетов: при повторном открытии попапа (по сообщению `ShowPopupRequest`)
будет переиспользован ранее загруженный iframe.

Рассмотрим работу с попап-окнами на примерах ниже.

#### Пример работы без возврата параметров из попап-окна 

> Пример взаимодействия без передачи дополнительных параметров

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 12,
  "popupName": "somePopup"
}

// хост-окно -> попап
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

// хост-окно -> попап
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

1. Виджет отправляет хост-окну сообщение `ShowPopupRequest`, указывая в нем имя попапа и опциональные параметры
1. Хост-окно отображает попап-окно, загружая страницу попапа по адресу `sourceUrl` в iframe с передачей `contextKey` в GET-параметре
1. Хост-окно отправляет в iframe попап-окна сообщение `OpenPopup`, передавая в нем опциональные параметры от виджета
1. Пользователь взаимодействует с веб-содержимым попапа, после чего закрывает его через системную кнопку (крестик), находящуюся в верхнем правом углу модального окна
1. Система скрывает попап-окно и отправляет виджету сообщение `ShowPopupResponse` с указанием того, что попап был закрыт пользователем через системную кнопку (```"popupResolution": "closedByUser"```)

Пример попап-окна с наличием только системной кнопки закрытия:

![useful image](popup-view.png)

> Закрытие попап-окна с использованием сообщения ClosePopup

```json 
...
// попап -> хост-окно
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

Вендор может отобразить на странице и собственную кнопку закрытия окна, при нажатии на которую будет отправляться сообщение `ClosePopup`,
а виджет получит сообщение `ShowPopupResponse` с  ```"popupResolution": "normal"```.

![useful image](popup-view-button.png)


#### Пример работы с возвратом параметров из попап-окна 

> Пример ответа с передачей данных о нажатой кнопке

```json 
// виджет -> хост-окно
{
  "name": "ShowPopupRequest",
  "messageId": 29,
  "popupName": "somePopup"
}

// хост-окно -> попап
{
  "name": "OpenPopup",
  "messageId": 36,
  "popupName": "somePopup"
}

// пользователь нажимает кнопку Сохранить

// попап -> хост-окно
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
Если попап-окну требуется вернуть информацию обратно в виджет, он должен передать ее в поле `popupResponse` сообщения `ClosePopup`.

1. Виджет отправляет хост-окну сообщение `ShowPopupRequest`, указывая в нем имя попапа и опциональные параметры
1. Хост-окно отображает попап-окно, загружая страницу попапа по адресу `sourceUrl` в iframe с передачей `contextKey` в GET-параметре
1. Хост-окно отправляет в iframe попап-окна сообщение `OpenPopup` с опциональными параметрами
1. Пользователь взаимодействует с веб-содержимым попапа, после чего нажимает кнопку закрытия или сохранения, находящуюся внутри страницы попапа
1. Попап отправляет хост-окну сообщение `ClosePopup`, передавая в нем параметры в зависимости от действий пользователя, например тип нажатой кнопки
1. Система скрывает попап-окно и отправляет виджету сообщение `ShowPopupResponse` с указанием параметров, переданных попапом

Пользователь может закрыть попап принудительно, при этом параметры переданы в виджет не будут.

Пример попап-окна с кнопками "Сохранить" и "Отмена":

![useful image](popup-edit.png)

#### Отображение содержимого, которое не вмещается в окно целиком

> Пример "плавающей" верстки содержимого

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
    </style>
    <link rel="stylesheet" href="css/uikit.css">
</head>

<body>
<div class="main-container">
    <div class="content-container">
        <!--Разместите здесь содержимое -->
    </div>
    <div class="buttons-container">
        <button class="button button--success">Сохранить</button>
        <button class="button">Отмена</button>
    </div>
</div>
</body>
</html>
```

Если в попап-окне требуется отобразить содержимое, которое потенциально может не вместиться на экране пользователя, 
то желательно использовать "плавающую" верстку: чтобы появлялись полосы прокрутки для содержимого, 
и кнопки закрытия окна всегда отображались в нижней части окна. 

Пример попап-окна с полосами прокрутки:

![useful image](popup-scroll.png)

Пример такой верстки с использованием [UI Kit](https://github.com/moysklad/html-marketplace-1.0-uikit) представлен справа.


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

// хост-окно -> попап
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

// хост-окно -> попап
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

// хост-окно -> попап
{
  "name": "OpenPopup",
  "messageId": 35,
  "popupName": "somePopup",
  "popupParameters": [123, "foobar"]
}
```

Существует несколько способов передачи параметров между виджетами и попапами:

* передача в виде примитивного значения
* передача в виде объекта
* передача в виде массива (в т.ч. массива объектов) 
* передача в виде значения `null`

Справа приведены примеры передачи параметров из виджета в попап-окно через сообщение `ShowPopupRequest`.
Аналогичные способы передачи можно использовать и для возврата ответа обратно в сообщении `ClosePopup`.

 
#### Подытожим сведения о попап-окнах 

* Попап-окно открывается на весь экран аналогично прочим модальным окнам в UI МоегоСклада (например, вызываемые “через карандаш” окна редактирования сущностей в полях).
* Попап-окно является модальным, т.е. открывается поверх текущей страницы МС и требует действия от пользователя внутри этого окна (взаимодействие с веб-страницей и/или закрытие попапа).
* Содержимое попапа определяется вендором (веб-содержимое загружается в iframe окна аналогично загрузке iframe виджета или основной iframe-части приложения).
* Попап, так же как и виджеты и основной iframe приложения, может получать текущий контекст пользователя.
* В качестве заголовка попап-окна используется название приложения.
* У попапов всегда есть кнопка для принудительного закрытия попапа пользователем (крестик справа вверху).
* Попап изменяет свои размеры при изменении размеров окна браузера.

### Ошибки

При получении сообщения от виджета хост-окно производит валидацию сообщения и, в случае если проверка не пройдена, 
возвращает в ответ сообщение `InvalidMessageError` со списком ошибок.

> Пример сообщения InvalidMessageError

```json 
{
  "name": "InvalidMessageError",
  "correlationId": null,
  "invalidMessage": {
    "name": "SelectGoodFolderRequest"
  },
  "errors": [
    {
      "code": 1001,
      "error": "Отсутствует обязательный параметр messageId"
    }
  ]
}
```

Пример такого сообщения можно увидеть справа. Здесь:

+ `correlationId` - идентификатор сообщения, которое вызвало ошибку;
+ `invalidMessage` - исходное сообщение, которое вызвало ошибку;
+ `errors` - список ошибок, каждое из которых содержит поля: `code` - код ошибки и `error` - описание ошибки.

Перечень возможных ошибок представлен в таблице:

| Код ошибки | Сообщение                                                                                                           | Описание                                                                                                                                                                                                    | Пример                                                                                            |
|------------|---------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| 1000       | Недопустимое состояние виджета %state% для сообщения %message.name%, допустимые состояния: %message.expectedStates% | Не допускается отправка данного сообщения из текущего состояния виджета                                                                                                                                     | `Недопустимое состояние виджета Opened для сообщения OpenFeedback, допустимые состояния: Opening` |
| 1001       | Отсутствует обязательный параметр %parameter.name%                                                                  | В сообщении отсутствует обязательный параметр                                                                                                                                                               | `Отсутствует обязательный параметр messageId`                                                     | 
| 1002       | Некорректное значение параметра %parameter.name%: %пояснение%                                                       | Параметр сообщения имеет некорректное значение                                                                                                                                                              | `Некорректное значение параметра popupName: popup with name = 'somePopup1' not found`             |
| 1003       | Параллельный запрос %message.name%                                                                                  | Не допускается отправка виджетом повторного запроса до момента получения ответа на предыдущий такой же запрос. Например: виджет уже отправил `SelectGoodFolderRequest` и пользователь еще не завершил выбор | `Параллельный запрос SelectGoodFolderRequest`                                                     |
| 1004       | Виджет не поддерживает протокол для обработки сообщения %message.name%                                              | Не допускается обработка сообщения в виджете, который не поддерживает протокол данного сообщения                                                                                                            | `Виджет не поддерживает протокол для обработки сообщения ShowDialogRequest`                       |


