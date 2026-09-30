## Сервисы хост-окна

В виджетах, iframe и модальных окнах доступны следующие сервисные возможности МоегоСклада (хост-окна):

* [Селектор группы товаров](#/developer-guide/host-window-services#4-selektor-gruppy-tovarov),
* [Стандартные диалоги](#/developer-guide/host-window-services#4-standartnye-dialogi),
* [Протокол навигации](#/developer-guide/host-window-services#4-protokol-navigacii),
* [Протокол контекста пользователя](#/developer-guide/host-window-services#4-protokol-konteksta-polzovatelya).

#### Селектор группы товаров

Дескриптор решения с виджетом, использующим селектор группы товаров

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
</ServerApplication>
```

Дескриптор решения, главный iframe и модальное окно которого используют селектор группы товаров

```xml
<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2      
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
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
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
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
Позволяет виджетам, главному и модальным окнам решений переиспользовать существующий в МоемСкладе селектор группы
товаров с получением ими результата выбора пользователя.

Чтобы виджет, главное или модальное окно начали поддерживать селектор в дескрипторе, необходимо добавить в блок `uses` для `widgets`, `iframe` или `popup` тег:
`<good-folder-selector/>`.

Рассмотрим пример с виджетом. Когда виджет отправляет хост-окну сообщение `SelectGoodFolderRequest` через Window.postMessage,
хост-окно запрашивает у пользователя выбор группы товаров, используя встроенный в МойСклад селектор:

![useful image](./images/good-folder-selector.png)

> Cообщение SelectGoodFolderRequest

```json 
{
  "name": "SelectGoodFolderRequest",
  "messageId": 12345
}
```

Здесь:
- `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом.

После совершения пользователем выбора группы товаров или отказа от него хост-окно передает виджету результат действий пользователя в сообщении `SelectGoodFolderResponse`.

> Cообщение SelectGoodFolderResponse (Пользователь выбрал группу товаров, имеющую идентификатор 8e9512f3-111b-11ea-0a80-02a2000a3c9c)

```json 
{
  "name": "SelectGoodFolderResponse",
  "correlationId": 12345,
  "selected": true,
  "goodFolderId": "8e9512f3-111b-11ea-0a80-02a2000a3c9c"
}
```

Здесь:

- `correlationId` — идентификатор соответствующего сообщения `SelectGoodFolderRequest`;
- `selected` — признак наличия выбора;
- `goodFolderId` — идентификатор выбранной группы товаров.

> Cообщение SelectGoodFolderResponse (Пользователь отменил выбор)

```json 
{
  "name": "SelectGoodFolderResponse",
  "correlationId": 12345,
  "selected": false
}
```

#### Стандартные диалоги

Дескриптор с виджетом, использующим стандартные диалоги

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
                <standard-dialogs/>
            </uses>                  
        </entity.counterparty.edit>    
    </widgets>
</ServerApplication>
```

Дескриптор решения, главное и модальное окно которого используют стандартные диалоги

```xml
<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2      
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/iframe.html</sourceUrl>
    <expand>true</expand>
    <uses>
        <standard-dialogs/>
    </uses>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <popups>
    <popup>
      <name>coolPopup</name>
      <sourceUrl>https://vendorurl.coolpopup.ru</sourceUrl>
      <uses>
          <standard-dialogs/>
      </uses>
    </popup>
  </popups>
</ServerApplication>
```


Позволяет виджетам, главному и кастомным модальным окнам использовать существующие в МоемСкладе стандартные диалоги.

Чтобы виджет, iframe или модальное окно начали поддерживать протокол, необходимо добавить в блок `uses` для `widgets`, `iframe` или `popup` тег:
`<standard-dialogs/>`.

Рассмотрим пример с виджетом. Когда виджет хочет показать пользователю стандартный диалог, он отправляет хост-окну сообщение `ShowDialogRequest`. В сообщении указывается текст сообщения и кнопки, которые необходимо отобразить пользователю. Наример:

![useful image](./images/standard-dialog-with-two-buttons.png)


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

* `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом;
* `dialogText` — текст сообщения, который нужно отобразить пользователю МоегоСклада. Максимальный размер — 4096 символов. HTML-теги не допускаются (будут экранированы);
* `buttons` — список кнопок в диалоге, элементами которого являются объекты с двумя обязательными полями: `name` — имя кнопки, будет возвращено в сообщении `ShowDialogResponse`, `caption` — текст, отображаемый на кнопке. Максимальный размер поля `caption` — 100 символов. HTML-теги в нем не допускаются (будут экранированы).

После того, как пользователь нажимает кнопку в диалоге или принудительно закрывает хост-окно (нажимает на «крестик»), результат действий пользователя возвращается в сообщении `ShowDialogResponse`.

> Сообщение ShowDialogResponse (Пользователь нажимает кнопку **Нет**)

```json 
{
  "name": "ShowDialogResponse",
  "correlationId": 12345,
  "buttonName": "No",
  "dialogResolution": "normal"
}
```

Параметры ответа `ShowDialogResponse`:

+ `correlationId` — идентификатор соответствующего сообщения `ShowDialogResponse`;
+ `dialogResolution` — признак выбора: `normal` — была нажата одна из кнопок, `closedByUser` — диалог был завершен принудительно;
+ `buttonName` — имя выбранной кнопки.

> Сообщение ShowDialogResponse (Пользователь закрыл диалог, нажав на «крестик»)

```json 
{
  "name": "ShowDialogResponse",
  "correlationId": 12345,
  "dialogResolution": "closedByUser"
}
```
**Примечание**:
В версии Google Chrome 92.0 и выше использование браузерных диалоговых окон через вызовы Window.alert(), Window.confirm() из iframe [запрещено](https://www.chromestatus.com/feature/5148698084376576).
Поэтому рекомендуется использовать сервис стандартных диалогов МоегоСклада.

#### Протокол навигации

Дескриптор с виджетом, использующим протокол навигации

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
                <navigation-service/>
            </uses>                  
        </entity.counterparty.edit>    
    </widgets>
</ServerApplication>
```
Дескриптор решения, у которого главное и модальное окно используют протокол навигации

```xml
<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2      
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
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
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
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
Позволяет виджетам, главному и модальным окнам решений осуществлять переход на другую страницу МоегоСклада и открывать МойСклад в новой вкладке.

Чтобы виджет, iframe или модальное окно начали поддерживать протокол навигации в дескрипторе необходимо добавить в блок `uses` для `widgets`, `iframe` или `popup` тег:
`<navigation-service/>`.
Примеры смотрите в правой части экрана.

Рассмотрим пример с виджетом. Когда виджет отправляет хост-окну сообщение `NavigateRequest` (через Window.postMessage), хост-окно переходит на другую страницу МоегоСклада или открывает в новой вкладке браузера нужную страницу МоегоСклада.

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

* `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом.
* `path` — путь до страницы, на которую виджет хочет осуществить переход. Например, чтобы осуществить переход пользователя на страницу реестра заказов покупателя https://online.moysklad.ru/app/#customerorder, нужно передать `#customerorder`.
* `target` — вид навигации. Может принимать одно из двух значений: `self` — переход в текущей вкладке, `blank` — открытие в новой вкладке.

Если валидация сообщения пройдет успешно, перед переходом пользователя будет отправлен `NavigateResponse` обратно в виджет.

> Cообщение NavigateResponse

```json 
{
  "name": "NavigateResponse",
  "correlationId": 12345 
}
```
Параметры ответа `NavigateResponse`:

+ `correlationId` — идентификатор соответствующего сообщения `NavigateRequest`.

При навигации из модального окна в текущей вкладке (`target` имеет значение `self`) произойдет переход, и модальное окно будет отображаться поверх страницы. Если необходимо, чтобы после перехода окно закрывалось, используйте сообщение `ClosePopup`. Подробнее смотрите в разделе [Кастомные модальные окна](#/developer-guide/custom-popups#2-kastomnye-modalnye-okna).

#### Протокол контекста пользователя

Дескриптор решения, у которого главное окно и виджет используют протокол контекста пользователя

```xml
<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframes>
    <iframe type="main" sourceUrl="https://example.com/iframe.html" useContextKey="false">
      <uses>
        <user-context/>
      </uses>
    </iframe>
  </iframes>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <widgets>
    <entity.counterparty.edit useContextKey="false">
      <sourceUrl>https://example.com/widget.php</sourceUrl>
      <height>
        <fixed>150px</fixed>
      </height>
      <uses>
        <user-context/>
      </uses>
    </entity.counterparty.edit>
  </widgets>
</ServerApplication>
```

Позволяет виджетам, главному окну и модальным окнам решений получить у хост-окна одноразовый токен и обменять его на
сервере разработчика на контекст текущего пользователя МоегоСклада.

Чтобы виджет, главное окно или модальное окно начали поддерживать протокол контекста пользователя, в дескрипторе
необходимо добавить в блок `uses` для `widgets`, `iframe` или `popup` тег: `<user-context/>`.
Примеры смотрите в правой части экрана.

В [окне чатов](#/developer-guide/iframes#4-okno-chatov) и [мобильном окне](#/developer-guide/iframes#4-mobilnye-prilozheniya) протокол пока не поддерживается: тег
`<user-context/>` для окон типа `chat` и `mobile` указать нельзя.

Атрибут `useContextKey="false"` отключает передачу параметра `contextKey` в URL загрузки. Подробнее
смотрите в разделе [Блок iframes](#/developer-guide/solution-descriptor#4-blok-iframes).

Рассмотрим пример с виджетом. Когда виджет отправляет хост-окну сообщение `UserContextRequest` (через
Window.postMessage), хост-окно выдает одноразовый токен и возвращает его в сообщении `UserContextResponse`.
Полученный токен виджет передает на сервер разработчика, а сервер обменивает его на контекст пользователя запросом
[POST /context/user](#/vendor-api/moysklad-endpoints#4-poluchenie-konteksta-polzovatelya-po-odnorazovomu-tokenu).

> Сообщение UserContextRequest

```json
{
  "name": "UserContextRequest",
  "messageId": 12345
}
```

Параметры сообщения `UserContextRequest`:

* `messageId` — целочисленный идентификатор сообщения, уникальный в рамках текущего взаимодействия виджет — хост-окно. Назначается виджетом.

> Сообщение UserContextResponse

```json
{
  "name": "UserContextResponse",
  "correlationId": 12345,
  "token": "a1b2c3d4e5f6478901234567890abcdef1234567"
}
```

Параметры ответа `UserContextResponse`:

+ `correlationId` — идентификатор соответствующего сообщения `UserContextRequest`;
+ `token` — одноразовый токен контекста пользователя. Токен действует 60 секунд с момента выдачи и перестает
  действовать после первого успешного обмена.

Для работы с протоколом рекомендуется использовать [JS Widget SDK](#/developer-guide/widget-sdk#2-sdk-dlya-vidzhetov) версии 1.2.0 и выше. Метод
`requestUserContextToken()` отправляет сообщение `UserContextRequest`, ожидает ответ хост-окна (по умолчанию не
более 10 секунд) и возвращает полученный токен. Библиотека не сохраняет токен в браузере и не выводит его значение
в отладочные логи.

При работе с токеном следует учитывать следующее:

1. Не передавайте токен в URL и не сохраняйте его в `localStorage`, `sessionStorage` и cookie.
1. Не отображайте токен пользователю и не записывайте его в логи.
1. Передавайте токен на сервер разработчика сразу после получения, в теле POST-запроса.
1. Запрашивайте новый токен на каждый обмен: повторно обменять уже использованный токен нельзя.
