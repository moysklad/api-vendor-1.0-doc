## Обработка ошибок на стороне МоегоСклада
Обработка ошибок на стороне МоегоСклада (при взаимодействии Вендор → МойСклад) выполняется аналогично тому, 
как это сделано в JSON API 1.2 
[https://moysklad.github.io/api-remap-1.2-doc/api/remap/1.2/ru/#obrabotka-oshibok](https://moysklad.github.io/api-remap-1.2-doc/api/remap/1.2/ru/#obrabotka-oshibok) - 
в тело ответа включается JSON объект с описанием ошибки и также проставляются (если нужно) соответствующие 
HTTP-заголовки в ответе.
