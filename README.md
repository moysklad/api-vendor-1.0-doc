[![Build Status](https://travis-ci.org/moysklad/api-vendor-1.0-doc.svg?branch=master)](https://travis-ci.org/moysklad/api-vendor-1.0-doc)

Запуск локальной версии документации
------------

_Чтобы локально развернуть копию документации:_

1. Установить docker CE и docker-compose, следуя инструкциям на https://docs.docker.com/ для своей ОС
2. Склонировать репозиторий `https://github.com/moysklad/api-vendor-1.0-doc.git`
3. В командной строке, перейдите в папку репозитория.
4. Выполните команды `docker-compose build` `docker-compose up`

Локальная версия документации будет доступна по адресу `http://localhost:4567`

Основная версия документации доступна по адресу https://dev.moysklad.ru/doc/api/vendor/1.0/

## Описание репозитория и структуры документации

В ветке `master` находится версия документации, развернутая на продуктовом сервере. После мерджа измений в мастер необходимо запустить скрипт `deploy.sh`, чтобы сделанные изменения стали доступны пользователям.

Для деплоя, возможно потребуется установить зависимости:
```bash
sudo apt install ruby
sudo apt install ruby-dev
sudo apt install zlib1g-dev
sudo gem install bundler -v '1.16.6'
bundle install
```

В папке `source/includes` находятся .md-файлы документации.

## Оформление нового раздела

Для добавления нового раздела необходимо создать .md-файл в папке `source/includes`. Имя файла должно начинаться с `_`. Для отображения нового раздела в боковом меню в `source/index.html.md` в раздел `includes` нужно прописать название нового раздела (должно совпадать с названием .md-файла).

Пример разметки страницы:
```
## Заголовок раздела

### Название сущности
Описание сущности

#### Атрибуты сущности
Описание аттрибутов сущности
+ **attribute** - описание аттрибута

#### Атрибуты доступные для фильтрации
При необходимости

#### Атрибуты доступные для сортировки
При необходимости

### Получить Сущности

**Параметры**

| Параметр | Описание  |
| --- |:---|
|parameter |  Описание параметра |

> Получить Сущности

> **`GET`**
> http://example.com/baseurl/api/moysklad/vendor/1.0/retaildemand/recalc

> **Request**

> Headers

> Body

> **Response**
> 200 (application/json)

Успешный запрос. Результат - JSON представление списка Сущностей

JSON ответа от сервера

```
