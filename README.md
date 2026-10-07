# Документация Vendor API

Публичная версия: https://dev.moysklad.ru/doc/api/vendor/1.0/

## Структура

- `md/` — тексты разделов. Файл раздела называется `_имя.md` и лежит в каталоге раздела.
- `config.json` — оглавление. Поле `folderPath` указывает на файл в `md/`.
- `site.json` — название документации и путь к логотипу.
- `hash-redirect-map.json` — соответствие старых адресов Middleman новым адресам React-документации.
- `images/` — изображения, на которые ссылаются файлы в `md/`.

## Новый раздел

1. Создайте файл, например `md/new_section/_new_section.md`.
2. Добавьте пункт в `config.json`:

```json
{
  "title": "Название раздела",
  "level": 1,
  "folderPath": "./new_section/_new_section.md",
  "children": []
}
```

3. Положите картинки в `images/` и вставляйте их так: `![описание](./images/file.png)`.

Вложенный пункт задаётся в `children` с `level` больше 1. `folderPath` может указывать на тот же файл, если несколько пунктов открывают разные заголовки одного раздела.

## Локальный запуск

Нужны Docker и доступ к `docker.infra.lognex`. Образ `AS-4800-482141` — тот же, которым собирается Vendor API.

```bash
docker compose up
```

Документация откроется по адресу http://localhost:4567. Изменения в `md/` подхватываются без перезапуска. После правки `config.json` или заголовков, которые должны появиться в поиске, перезапустите контейнер.

## Проверки

В GitHub Actions на pull request и после merge в `master` запускаются две проверки:

```bash
npm install --no-save --package-lock=false slugify@1.6.6
python3 scripts/build_hash_redirect_map.py --check
python3 scripts/check-doc-links.py --markdown-dir md
```

Первая сверяет внутренние ссылки и старые адреса. Вторая проверяет внешние ссылки `http` и `https` в Markdown. Для локального прогона без сети добавьте `--skip-external`.

Адреса API `https://api.moysklad.ru/api/remap/1.2` и `https://apps-api.moysklad.ru/api/vendor/1.0` не проверяются по HTTP. Внешний адрес, который недоступен из CI, но проверен вручную, можно добавить в `scripts/check-doc-links-allowlist.txt`: он будет отмечен как `INFO`.

Правила оформления Markdown (`test:md`) выполняются при сборке в [remap-deployer](https://git.company.lognex/moysklad/remap-deployer), а не в GitHub Actions.

## Публикация

Preview ветки собирается вручную в remap-deployer. Параметры: `api=vendor_10` и `branch` — имя ветки этого репозитория.

[Запустить preview](https://git.company.lognex/moysklad/remap-deployer/-/pipelines/new?ref=master&var%5Bapi%5D=vendor_10&var%5Bbranch%5D=)

Адрес результата: `https://moysklad.pages.lognex/remap-deployer/vendor_10/<ветка>/`.

Production-выкладка тоже запускается вручную. Параметр `deploy_target=vendor-api`. `source_sha` можно не указывать: тогда берётся текущий `master`. Если к моменту выкладки `master` уже другой, запуск пропускается.

[Запустить production](https://git.company.lognex/moysklad/remap-deployer/-/pipelines/new?ref=master&var%5Bdeploy_target%5D=vendor-api)

Подробности обеих схем — в [README remap-deployer](https://git.company.lognex/moysklad/remap-deployer/-/blob/master/README.md).
