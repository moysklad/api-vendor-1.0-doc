# Руководство разработчика


## Доступ по токену к JSON API

Токен для доступа к JSON API 1.2 передается разработчику при активации решения через Vendor API в момент установки или 
возобновления решения. Время жизни токена не ограничено. 

Токен аннулируется при удалении и приостановке решения. На момент деактивации решения через Vendor API токен уже аннулирован.

Токен при доступе к JSON API 1.2 следует передавать как [Bearer-токен](https://dev.moysklad.ru/doc/api/remap/1.2/#mojsklad-json-api-obschie-swedeniq-autentifikaciq),
 а именно в виде заголовка HTTP-запроса:
 
 ```text
Authorization: Bearer <access_token>
 ```

Пример:

```text
Authorization: Bearer 6ab89be1ae6ff147755625ee8da948e42612233b
```

#### Диаграмма последовательности предоставления доступа при подключении решения

![useful image](images/diag_install.png)

#### Диаграмма последовательности отзыва доступа при отключении решения

![useful image](images/diag_uninstall.png)
