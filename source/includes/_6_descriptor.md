## Дескриптор приложения

Дескриптор приложения представляет собой XML-структуру, которая описывает технические параметры встраивания/интеграции 
приложения вендора в МойСклад.

Содержимое дескриптора должно соответствовать версии XSD-схемы.
Актуальной версией считается [v2](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd).

### История версий XSD-схемы дескриптора

| Версия | Описание  | Разрешенное содержимое дескриптора  |  Поддерживаемые типы приложений  |  
|----|----|----|----|
|[1.0.0](https://online.moysklad.ru/xml/ns/appstore/app/v1/application-1.0.0.xsd)|Серверные и простые iFrame-приложения | vendorApi, access, iframe | iFrame, Серверные
|[1.1.0](https://online.moysklad.ru/xml/ns/appstore/app/v1/application-1.1.0.xsd)|Расширение iFrame (тег expand) |  vendorApi, access, iframe(c expand) | iFrame, Серверные
|[2.0.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.0.0.xsd)|Виджеты в старой карточке контрагента. Прекращена поддержка приложений с типом iFrame  |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.1.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.1.0.xsd)|Виджеты в Заказе покупателя и Отгрузке |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.2.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.2.0.xsd)|Виджеты с поддержкой селектора групп товаров |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.3.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.3.0.xsd)|Виджеты в Счете покупателю |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.4.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.4.0.xsd)|Виджеты в новой карточке Контрагента |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.5.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.5.0.xsd)|Виджеты с поддержкой протокола save-handler |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.6.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.6.0.xsd)|Виджеты с поддержкой протокола dirty-state |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.7.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.7.0.xsd)|Виджеты в Счете поставщика, Заказе поставщику, Заказе на производство, Приемке |vendorApi, access, iframe(c expand), widgets | Серверные
|[2.8.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.8.0.xsd)|Кастомные попапы |vendorApi, access, iframe(c expand), widgets, popups | Серверные
|[2.9.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.9.0.xsd)|Виджеты в Розничной продаже, Входящем и Исходящем платеже, Приходном и Расходном ордере |vendorApi, access, iframe(c expand), widgets, popups | Серверные
|[2.10.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.10.0.xsd)|Протокол change-handler для виджетов в Заказе покупателя |vendorApi, access, iframe(c expand), widgets, popups | Серверные
|[2.12.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.12.0.xsd)|Стандартные диалоги |vendorApi, access, iframe(c expand), widgets, popups | Серверные
|[2.13.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.13.0.xsd)|Гибкие права приложений |vendorApi, access(с permissions), iframe(c expand), widgets, popups | Серверные
|[2.14.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.14.0.xsd)|Виджеты в Перемещении, Списании, Оприходовании, Внутреннем заказе, Инвентаризации |vendorApi, access(с permissions), iframe(c expand), widgets, popups | Серверные
|[2.16.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.16.0.xsd)|Виджеты в Возвратах покупателя и в Возвратах поставщику |vendorApi, access(с permissions), iframe(c expand), widgets, popups | Серверные
|[2.17.0](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-2.17.0.xsd)|Протокол навигации |vendorApi, access(с permissions), iframe(c expand), widgets, popups | Серверные

Основные отличия дескриптора v2 от дескрипторов версий 1.x.x:

- Изменение корневого тега - теперь каждый тип приложений представлен своим корневым тегом. 
  В версии v2 есть только один тип приложений - ServerApplication (iframe-приложения 
  объявлены deprecated и с отменой поддержки дескрипторов версий 1.x.x станут недоступны).
  
- Добавлен блок widgets (необязательный) для указания конфигурации виджетов приложения.

- Добавлен блок popups (необязательный) для указания конфигурации попап-окон приложения.

Дескрипторы версий 1.x.x некоторое время будут продолжать поддерживаться.


### Содержимое дескриптора приложения


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
        <scope>custom</scope>
        <permissions>
          <viewDashboard/>
          <customerOrder>
            <view/>
            <create/>
            <update/>
          </customerOrder>
        </permissions>
    </access>
    <widgets>        
        <entity.counterparty.edit>            
            <sourceUrl>https://example.com/widget.php</sourceUrl>            
            <height>                
                <fixed>150px</fixed>            
            </height>
            <uses>
                <good-folder-selector/>
                <standard-dialogs/>
                <navigation-service/>
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


На текущий момент в [актуальной](https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd) версии дескриптора 
приложения есть четыре блока: **iframe**, **vendorApi**, **access**, **widgets**, **popups**. 
Порядок расположения этих блоков относительно друг друга в дескрипторе может быть произвольным.

|Блок|Назначение|Доступно для типов приложений|Требует наличия других блоков|
|----|----------|-----------------------------|-----------------------------|
|iframe|Описывает iframe-часть приложения|iframe-приложения, серверные приложения|Не требует|
|vendorApi|Описывает взаимодействие по Vendor API|серверные приложения|Не требует|
|access|Описывает требуемый доступ приложения к ресурсам пользовательского аккаунта|серверные приложения|vendorApi|
|widgets|Описывает виджеты|серверные приложения|Не требует|
|popups|Описывает кастомные попапы|серверные приложения|Не требует|

### Блок iframe

В теге **iframe/sourceUrl** указывается URL, по которому будет загружаться содержимое iframe внутри UI МоегоСклада. 
В URL допускается использование только протокола HTTPS.

В случае отсутствия блока **iframe** в дескрипторе считается, что у приложения отсутствует iframe-часть.

В теге **iframe/expand** указывается `boolean` значение, которое отвечает, будет ли iframe расширяться в основном приложении 
МоегоСклада. Под расширением подразумевается автоматическое масштабирование iframe элемента в зависимости от контента.
Данный элемент является опциональным со значением `false` по умолчанию, 
но требуется его установка для случаев, когда содержимое не умещается в окне браузера по высоте.

Чтобы расширение iframe работало верно, на странице, которая указана в **sourceUrl**, должен работать скрипт, 
оповещающий страницу МоегоСклада об изменении высоты его контента, то есть:

* Реализовать посылку сообщения “EventMessage” при любом изменении высоты контента, причем
    * сообщение послать parent окну
    * данные сообщения должны содержать свойство “height” - высоту содержимого, страницы, которая сейчас отображается (в px)

Для удобства можно добавить следующий [js скрипт](https://online.moysklad.ru/js/ns/appstore/app/v1/moysklad-iframe-expand-2.js) 
на свою страницу. Пример:


```html
<!doctype html>
<html>

<head>
...
</head>

<body>
...
<script type="text/javascript" src="https://online.moysklad.ru/js/ns/appstore/app/v1/moysklad-iframe-expand-2.js"></script>
</body>

</html>
```



### Блок vendorApi

В теге **vendorApi/endpointBase**  указывается базовый URL эндпоинта на стороне вендора, к которому будет обращаться 
МойСклад. В URL допускается использование только протокола HTTPS.

Для получения полного адреса конкретного эндпоинта Vendor API на стороне вендора к базовому URL’у добавляется суффикс 
`/api/moysklad/vendor/1.0` и путь эндпоинта. То есть шаблон формирования полного URL ресурса в общем случае такой:

`{endpointBase}/api/moysklad/vendor/1.0/{endpointPath}/…`

Для эндпоинта активации/деактивации приложений на аккаунте шаблон следующий (endpointPath = apps):

`{endpointBase}/api/moysklad/vendor/1.0/apps/{appId}/{accountId}`

Например, если:

+ <endpointBase>https://example.com/dummy-app</endpointBase>
+ appId = 5f3c5489-6a17-48b7-9fe5-b2000eb807fe
+ accountId = f088b0a7-9490-4a57-b804-393163e7680f
+ endpointPath = apps

то полный URL ресурса на стороне вендора, к которому будет выполнять запросы МойСклад при активации (и деактивации) 
приложения на аккаунте, будет следующим: 

`https://example.com/dummy-app/api/moysklad/vendor/1.0/apps/5f3c5489-6a17-48b7-9fe5-b2000eb807fe/f088b0a7-9490-4a57-b804-393163e7680f`
 
В случае отсутствия блока vendorApi в дескрипторе не выполняется активация и деактивация приложения на серверах вендора.

### Блок access

Требуется для серверных приложений, которые хотят получить доступ по JSON API к ресурсам аккаунта.
В случае отсутствия этого блока в дескрипторе приложения при установке на аккаунт приложению не выдаются никакие доступы 
к ресурсам.
Наличие блока **access** требует наличия блока **vendorApi** для передачи токена к ресурсам аккаунта при активации 
приложения по Vendor API.

В теге **access/resource** указывается ресурс, к которому приложению нужен доступ.
На текущий момент для ресурса возможно только одно значение: `https://online.moysklad.ru/api/remap/1.2`

В теге **access/scope** указывается требуемый уровень доступа.
Для него на текущий момент доступно два значения: `admin` и `custom`. 
Если указан уровень `admin`, то приложение будет работать с правами администратора аккаунта.
Если указан уровень `custom`, то приложение получит доступ только к отчетам, документам и сущностям, 
перечисленным в теге **permissions**.
 
В теге **access/permissions** указываются требуемые пермиссии. 
Данный тег обязателен для уровня доступа со значением `custom`.
 

> Пример заполнения блока **access** с указанием прав Администратора:

```xml
<access>
    <resource>https://online.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
</access>
```

> Пример заполнения блока **access** с явным перечислением пермиссий:

```xml
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>custom</scope>
        <permissions>
          <viewDashboard/>
          <viewAudit/>
          <customerOrder>
            <view/>
            <create/>
            <update/>
            <delete/>
            <approve/>
            <print/>
          </customerOrder>
          <company>
            <view/>
            <create/>
          </company>
        </permissions>
    </access>
```

Перечисленные в теге **permissions** права доступа могут включать в себя:

* **Пользовательские** — права доступа, в которых достаточно указать только название. Позволяют получить доступ к отчетам в МоемСкладе.
  Могут принимать следующие значения: viewDashboard, viewAudit, viewSaleProfit, viewTurnover, viewCompanyCRM, viewProfitAndLoss,
  viewMoneyDashboard
* **Сущностей** — права доступа, в которых помимо названия необходимо указывать так же и уровни доступа к соответствующим сущностям и документам: view, create, update и т.д. 

Есть три типа значений для пермиссий сущностей, далее будут указаны тип (уровни доступа) и названия:

**1. OPERATION (view, create, update, delete, print, approve)** — purchaseOrder, invoiceIn, supply, purchaseReturn, factureIn, customerOrder,
invoiceOut, demand, commissionReportIn, commissionReportOut, salesReturn, factureOut, enter, loss, internalOrder, move, priceList, paymentIn,
paymentOut, cashIn, cashOut, retailDemand, retailSalesReturn, retailDrawerCashIn, retailDrawerCashOut, bonusTransaction, prepayment, prepaymentReturn,
processing, processingOrder

**2. DICTIONARY (view, create, update, delete, print)** — good, inventory, company, contract, retailShift

**3. BASE (view, create, update, delete, print)** — retailStore, processingPlan, myCompany, employee, warehouse, currency, project, country, uom,
customEntity

Подробнее о пермиссиях в МоемСкладе см. в [документации JSON API](https://dev.moysklad.ru/doc/api/remap/1.2/dictionaries/#sushhnosti-sotrudnik-rabota-s-pravami-sotrudnika).

Примечания: 

* Имеются два ограничения на сочетания пермиссий сущностей: 
  * уровень доступа `<view/>` необходим, если есть другие уровни;
  * уровень доступа `<update/>` необходим, если требуется уровень `<delete/>`.
* При установке приложения ему будет автоматически предоставлено право на просмотр справочника Валют (`<currency><view/></currency>`).
* В настоящий момент нет отдельной пермиссии для работы с web-хуками. 
  Приложение, которое хочет получить доступ к ним, должно работать с правами администратора.
* В настоящий момент не поддерживается пермиссия для работы с Задачами (`script`). 
  Приложение, которое хочет получить доступ к ним, должно работать с правами администратора.
* В настоящий момент не поддерживаются пермиссии для работы с сущностями Маркировки: 
  `crptCancellation`, `crptPackageCreation`, `crptPackageItemRemoval`, `crptPackageDisaggregation`, `GTINList`, `trackingCodeList`. 


### Блок widgets

Сначала необходимо определить в блоке **widgets** точку расширения - указать страницу, где будет 
расположен виджет. 

Сейчас доступны следующие точки расширения:
 
- **entity.counterparty.edit** - карточка Контрагента
- **document.customerorder.edit** - документ "Заказ покупателя"
- **document.demand.edit** - документ "Отгрузка"
- **document.invoiceout.edit** - документ "Счет покупателю"
- **document.processingorder.edit** - документ "Заказ на производство"
- **document.purchaseorder.edit** - документ "Заказ поставщику"
- **document.invoicein.edit** - документ "Счет поcтавщика"
- **document.supply.edit** - документ "Приемка"
- **document.retaildemand.edit** - документ "Розничная продажа"
- **document.paymentin.edit** - документ "Входящий платеж"
- **document.paymentout.edit** - документ "Исходящий платеж"
- **document.cashin.edit** - документ "Приходный ордер"
- **document.cashout.edit** - документ "Расходный ордер" 
- **document.move.edit** - документ "Перемещение"
- **document.loss.edit** - документ "Списание"
- **document.enter.edit** - документ "Оприходование"
- **document.internalorder.edit** - документ "Внутренний заказ"
- **document.inventory.edit** - документ "Инвентаризация"
- **document.purchasereturn.edit** - документ "Возврат поставщику"
- **document.salesreturn.edit** - документ "Возврат покупателя"

В одном дескрипторе может быть указано несколько точек расширения, то есть одно приложение сможет создать
 сразу несколько виджетов - на разных страницах. В то же время для приложения действует правило:
 одна страница - один виджет. То есть, в дескрипторе может быть указано только по 
  одной точке расширения каждого типа.
 
Тем не менее, в итоге на одной странице может оказаться несколько виджетов (от разных приложений).

Только виджет документа Заказ покупателя на данный момент поддерживает протокол `change-handler`. В остальном виджеты во всех точках расширения обладают одинаковой функциональностью, поэтому ниже приведен универсальный список 
тегов для любой из точек расширения:

Тег **sourceUrl** - обязательный. Содержит URL, по которому загружается код виджета в iframe.
В URL допускается использование только протокола HTTPS.

Тег **height** - обязательный.  В теге **height/fixed** задается фиксированная высота виджета
в пикселях, в формате **150px**.

Тег **supports** - опциональный. Предназначен для  дополнительных протоколов, поддерживаемых 
виджетом. На данный момент в нем можно указать протоколы:
 
 - **open-feedback** - при открытии экрана обеспечивает 
скрытие содержимого виджета до явного уведомления от виджета о готовности. Параметры у протокола отсутствуют.
 
 - **save-handler** - при сохранении сущности или объекта позволяет уведомить об этом виджет. Параметры у протокола отсутствуют.
 
 - **dirty-state** - при наличии несохраненных изменений в виджете позволяет отобразить 
   диалог подтверждения сохранения изменений. Параметры у протокола отсутствуют.
   
 - **change-handler** - при изменении несохраненного состояния объекта позволяет уведомить об этом виджет, отправляя текущее состояние объекта. Пока доступен только в Заказе покупателя. Параметры у протокола отсутствуют.
 
 Подробнее про дополнительные протоколы **open-feedback**, **save-handler**, **dirty-state**, **change-handler** можно прочитать в разделе
  [Жизненный цикл виджета](#zhiznennyj-cikl-widzheta).
 
Тег **uses** - опциональный. Предназначен для сервисных протоколов, используемых виджетом. 
На данный момент в нем можно указать следующие протоколы: 

* **uses/good-folder-selector** позволяет виджетам приложений переиспользовать существующий в МоемСкладе селектор группы товаров с получением 
виджетом результата выбора пользователя. 
Подробнее про протокол можно прочитать в разделе [Селектор группы товаров](#serwisy-host-okna). 
Параметры у протокола отсутствуют.

* **uses/standard-dialogs** позволяет виджетам приложений использовать существующие в МоемСкладе стандартные диалоги с получением 
виджетом результата выбора пользователя (кнопки, нажатой пользователем). 
Подробнее про протокол можно прочитать в разделе [Стандартные диалоги](#serwisy-host-okna). 
Параметры у протокола отсутствуют.

* **uses/navigation-service** позволяет виджетам приложений осуществлять переход на другую страницу МоегоСклада и открывать МойСклад в новой вкладке. 
Подробнее про протокол можно прочитать в разделе [Протокол навигации](#protokol-nawigacii). 
Параметры у протокола отсутствуют.

Пример заполненного блока **widgets**:

> Блок widgets с точками расширения в контрагенте и заказе покупателя

```xml
    <widgets>
        <entity.counterparty.edit>
            <sourceUrl>https://example.com/widget-counterparty.php</sourceUrl>
            <height>
                <fixed>200px</fixed>
            </height>
            <supports><open-feedback/></supports>
        </entity.counterparty.edit>

        <document.customerorder.edit>
            <sourceUrl>https://example.com/widget-customerorder.php</sourceUrl>
            <height>
                <fixed>50px</fixed>
            </height>
            <uses>
                <good-folder-selector/>
                <standard-dialogs/>
                <navigation-service/>
            </uses>
        </document.customerorder.edit>
    </widgets>
```
### Блок popups

> Блок popups с двумя попапами

```xml
    <popups>
        <popup>
            <name>somePopup1</name>
            <sourceUrl>https://example.com/popup-1.php</sourceUrl>
        </popup>
        <popup>
            <name>somePopup2</name>
            <sourceUrl>https://example.com/popup-2.php</sourceUrl>
        </popup>
    </popups>
```

Служит для задания списка кастомных попап-окон, которые могут использоваться приложением (виджетами).

Для задания имени попап-окна используется тег `name` (обязательный).
Для задания адреса страницы используется тег `sourceUrl` (обязательный).

Подробнее про работу с кастомными попап-окнами можно прочитать в разделе [Кастомные попапы](#kastomnye-popapy-dialogowye-okna). 


### Примеры дескрипторов


#### Для серверных приложений (актуальная версия схемы дескриптора v2)

> Дескриптор для серверных приложений с iframe-частью и расширением окна (expand)

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
</ServerApplication>
```



> Дескриптор для серверных приложений с виджетом в карточке контрагента

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
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
        </entity.counterparty.edit>    
    </widgets>
</ServerApplication>
```
> Дескриптор для серверных приложений с виджетом в карточке контрагента, заказе покупателя и отгрузке и протоколами openfeedback и save-handler

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
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
            <supports><open-feedback/></supports>        
        </entity.counterparty.edit>    

        <document.customerorder.edit>
            <sourceUrl>https://example.com/widget-customerorder.php</sourceUrl>
            <height>
                <fixed>50px</fixed>
            </height>
            <supports>
                <open-feedback/>
                <save-handler/>
            </supports>  
        </document.customerorder.edit>

        <document.demand.edit>
            <sourceUrl>https://example.com/widget-demand.php</sourceUrl>
            <height>
                <fixed>50px</fixed>
            </height>
            <supports><open-feedback/></supports>  
        </document.demand.edit>
    </widgets>
</ServerApplication>
```

> Дескриптор для серверных приложений с виджетом в карточке контрагента, заказе покупателя и отгрузке и протоколами good-folder-selector и dirty-state

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
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
            <supports>
                <dirty-state/>  
            </supports>
            <uses>
                <good-folder-selector/>
            </uses>      
        </entity.counterparty.edit>    

        <document.customerorder.edit>
            <sourceUrl>https://example.com/widget-customerorder.php</sourceUrl>
            <height>
                <fixed>50px</fixed>
            </height>
            <supports>
                <dirty-state/>  
            </supports>
            <uses>
                <good-folder-selector/>
            </uses>
        </document.customerorder.edit>

        <document.demand.edit>
            <sourceUrl>https://example.com/widget-demand.php</sourceUrl>
            <height>
                <fixed>50px</fixed>
            </height>
            <supports>
                <dirty-state/>
            </supports>
            <uses>
                <good-folder-selector/>
            </uses>
        </document.demand.edit>
    </widgets>
</ServerApplication>
```
> Дескриптор для серверных приложений с виджетом в заказе покупателя и счете покупателю

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
    <widgets>        
        <document.customerorder.edit>
            <sourceUrl>https://example.com/widget-customerorder.php</sourceUrl>
            <height>
                <fixed>150px</fixed>
            </height>
        </document.customerorder.edit>
        <document.invoiceout.edit>
            <sourceUrl>https://example.com/widget-invoiceout.php</sourceUrl>
            <height>
                <fixed>110px</fixed>
            </height>
        </document.invoiceout.edit>
    </widgets>
</ServerApplication>
```

> Дескриптор для серверных приложений с виджетом в заказе покупателя и двумя кастомными попапами

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"             
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"             
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
    <widgets>        
        <document.customerorder.edit>
            <sourceUrl>https://example.com/widget-customerorder.php</sourceUrl>
            <height>
                <fixed>150px</fixed>
            </height>
        </document.customerorder.edit>
    </widgets>
    <popups>
        <popup>
            <name>viewPopup</name>
            <sourceUrl>https://example.com/view-popup.php</sourceUrl>
        </popup>
        <popup>
            <name>editPopup</name>
            <sourceUrl>https://example.com/edit-popup.php</sourceUrl>
        </popup>
    </popups>
</ServerApplication>
```

> Дескриптор для серверных приложений с явным указанием прав доступа

```xml
<ServerApplication  xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v2"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v2      
                    https://online.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://online.moysklad.ru/api/remap/1.2</resource>
    <scope>custom</scope>
    <permissions>
      <viewDashboard/>
      <viewAudit/>
      <purchaseOrder>
        <view/>
        <create/>
        <update/>
        <delete/>
        <print/>
        <approve/>
      </purchaseOrder>
      <good>
        <view/>
        <create/>
        <print/>
      </good>
    </permissions>
  </access>
</ServerApplication>
```

#### Для серверных приложений (устаревшие версии схемы дескриптора 1.x.x)

> Минимальный дескриптор для серверных приложений (без возможности настройки параметров приложения пользователем 
МоегоСклада, так как у приложения отсутствует iframe-часть)

```xml
<application xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"                                  
      xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v1 
      https://online.moysklad.ru/xml/ns/appstore/app/v1/application-1.1.0.xsd">
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
</application>
```

> Дескриптор для серверных приложений с iframe-частью

```xml
<application xmlns="https://online.moysklad.ru/xml/ns/appstore/app/v1"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"                                  
      xsi:schemaLocation="https://online.moysklad.ru/xml/ns/appstore/app/v1 
      https://online.moysklad.ru/xml/ns/appstore/app/v1/application-1.1.0.xsd">
    <iframe>
        <sourceUrl>https://example.com/iframe.html</sourceUrl>
    </iframe>
    <vendorApi>
        <endpointBase>https://example.com/dummy-app</endpointBase>
    </vendorApi>
    <access>
        <resource>https://online.moysklad.ru/api/remap/1.2</resource>
        <scope>admin</scope>
    </access>
</application>
```



#### Для телефонии

Для приложений телефонии дескриптор на текущий момент не требуется (не поддерживается).



#### Для систем лояльности

Для интеграций с системами лояльности дескриптор на текущий момент не требуется (не поддерживается).
