## Примеры дескрипторов

#### Для серверных решений (актуальная версия схемы дескриптора v2)

Дескриптор для серверных решений

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
</ServerApplication>
```

Дескриптор для серверных решений с главным окном, окном чата и мобильным окном

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframes>
    <iframe type="main" sourceUrl="https://example.com/dummy-app/main.html">
      <uses>
        <standard-dialogs/>
      </uses>
    </iframe>
    <iframe type="chat" sourceUrl="https://example.com/dummy-app/chat.html"/>
    <iframe type="mobile" sourceUrl="https://example.com/dummy-app/mobile.html"/>
  </iframes>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
</ServerApplication>
```

Дескриптор для серверных решений с виджетом в карточке Контрагента

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
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
      <sourceUrl>https://example.com/dummy-app/widget.php</sourceUrl>
      <height>
        <fixed>150px</fixed>
      </height>
    </entity.counterparty.edit>
  </widgets>
</ServerApplication>
```

Дескриптор для серверных решений с виджетом и протоколами open-feedback, save-handler, change-handler в Карточке контрагента, Заказе покупателя и Отгрузке 

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
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
      <sourceUrl>https://example.com/dummy-app/widget.php</sourceUrl>
      <height>
        <fixed>150px</fixed>
      </height>
      <supports>
        <open-feedback/>
      </supports>
    </entity.counterparty.edit>

    <document.customerorder.edit>
      <sourceUrl>https://example.com/dummy-app/widget-customerorder.php</sourceUrl>
      <height>
        <fixed>50px</fixed>
      </height>
      <supports>
        <open-feedback/>
        <save-handler/>
        <change-handler/>
      </supports>
    </document.customerorder.edit>

    <document.demand.edit>
      <sourceUrl>https://example.com/dummy-app/widget-demand.php</sourceUrl>
      <height>
        <fixed>50px</fixed>
      </height>
      <supports>
        <open-feedback/>
        <change-handler/>
      </supports>
    </document.demand.edit>
  </widgets>
</ServerApplication>
```

Дескриптор для серверных решений с виджетом и протоколом change-handler c validation-feedback в Заказе покупателя

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <widgets>
    <document.customerorder.edit>
      <sourceUrl>https://example.com/dummy-app/widget-customerorder.php</sourceUrl>
      <height>
        <fixed>50px</fixed>
      </height>
      <supports>
        <change-handler>
          <validation-feedback/>
        </change-handler>
      </supports>
    </document.customerorder.edit>
  </widgets>
</ServerApplication>
```

Дескриптор для серверных решений с виджетом и протоколами good-folder-selector и dirty-state в карточке Контрагента, Заказе покупателя и Отгрузке 

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
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
      <sourceUrl>https://example.com/dummy-app/widget.php</sourceUrl>
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
      <sourceUrl>https://example.com/dummy-app/widget-customerorder.php</sourceUrl>
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
      <sourceUrl>https://example.com/dummy-app/widget-demand.php</sourceUrl>
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

Дескриптор для серверных решений с виджетом в Заказе покупателя и Счете покупателю

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <widgets>
    <document.customerorder.edit>
      <sourceUrl>https://example.com/dummy-app/widget-customerorder.php</sourceUrl>
      <height>
        <fixed>150px</fixed>
      </height>
    </document.customerorder.edit>
    <document.invoiceout.edit>
      <sourceUrl>https://example.com/dummy-app/widget-invoiceout.php</sourceUrl>
      <height>
        <fixed>110px</fixed>
      </height>
    </document.invoiceout.edit>
  </widgets>
</ServerApplication>
```

Дескриптор для серверных решений с виджетом в Заказе покупателя и двумя кастомными модальными окнами, одно из
которых поддерживает протокол good-folder-selector

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <widgets>
    <document.customerorder.edit>
      <sourceUrl>https://example.com/dummy-app/widget-customerorder.php</sourceUrl>
      <height>
        <fixed>150px</fixed>
      </height>
    </document.customerorder.edit>
  </widgets>
  <popups>
    <popup>
      <name>viewPopup</name>
      <sourceUrl>https://example.com/dummy-app/view-popup.php</sourceUrl>
    </popup>
    <popup>
      <name>editPopup</name>
      <sourceUrl>https://example.com/dummy-app/edit-popup.php</sourceUrl>
      <uses>
        <good-folder-selector/>
      </uses>
    </popup>
  </popups>
</ServerApplication>
```

Дескриптор для серверных решений с кнопками в Заказе покупателя, Заказе поставщику, карточке Контрагента и Товара

```xml

   <ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2
         https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>admin</scope>
  </access>
  <buttons>
    <button name="button1" title="Отправить контрагенту">
      <locations>
        <document.customerorder.edit/>
      </locations>
    </button>
    <button name="button2" title="Сформировать цифровую подпись">
      <locations>
        <entity.counterparty.edit/>
        <entity.product.edit/>
        <document.customerorder.edit/>
        <document.purchaseorder.edit/>
      </locations>
    </button>
  </buttons>
</ServerApplication>
```

Дескриптор для серверных решений с явным указанием прав доступа

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
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

Дескриптор для решений, работающих с webhooks

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>custom</scope>
    <permissions>
      <useOwnWebhooks/>
      <!-- Используйте <useAllWebhooks/> если решение должно управлять вебхуками всех решений -->
    </permissions>
  </access>
</ServerApplication>
```

Дескриптор для решений, работающих с дополнительными полями

```xml

<ServerApplication xmlns="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="https://apps-api.moysklad.ru/xml/ns/appstore/app/v2    
                    https://apps-api.moysklad.ru/xml/ns/appstore/app/v2/application-v2.xsd">
  <iframe>
    <sourceUrl>https://example.com/dummy-app/iframe.html</sourceUrl>
  </iframe>
  <vendorApi>
    <endpointBase>https://example.com/dummy-app</endpointBase>
  </vendorApi>
  <access>
    <resource>https://api.moysklad.ru/api/remap/1.2</resource>
    <scope>custom</scope>
    <permissions>
      <useOwnAttributeMetadata/>
      <!-- Используйте <useAllAttributeMetadata/> если решение должно управлять доп.полями всех решений -->
    </permissions>
  </access>
</ServerApplication>
```

#### Для телефонии

Для решений телефонии дескриптор на текущий момент не требуется (не поддерживается).
