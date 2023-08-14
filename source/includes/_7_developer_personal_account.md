## Личный кабинет разработчика
### Личный кабинет разработчика

Личный кабинет разработчика — это сервис, который упрощает работу над приложениями для магазина приложений. Личный кабинет позволяет разработчику:
- Самостоятельно создавать приложения в статусе **Draft (Черновик)**; 
- Отлаживать и тестировать приложения на витрине приложений, вносить необходимые изменения, в том числе самостоятельно, получать и изменять SecretKey; 
- Отправлять приложение на модерацию в МойСклад по окончании разработки. 

В личном кабинете можно:
 
- Создавать Черновики приложений; 
- Редактировать Черновики приложений и просматривать информацию о приложениях в прочих статусах;
- Редактировать информацию о разработчике; 
- Отправлять Черновики приложений на модерацию;
- Следить за статусом публикации своих приложений;
- Предоставлять и продлевать пробный период для платных приложений; 
- Привязывать аккаунты в МоемСкладе к аккаунту в личном кабинете для отладки неопубликованных приложений;
- Просматривать отчеты по установкам и выручке;
- Просматривать, скачивать и согласовывать отчет об использовании приложений;
- Просматривать отчет по причинам удаления приложений. 

### Получение доступа к личному кабинету разработчика

Для получения доступа в личный кабинет разработчика заполните [анкету](https://partners.moysklad.ru/developers/#register). Доступ и дальнейшие инструкции будут высланы на почту, указанную в анкете, в течение нескольких дней.

### Жизненный цикл приложения 

Статусы жизненного цикла приложения для магазина приложений:

- **Черновик (Draft)** — статус черновика, предназначен для разработки и тестирования. Приложение не отображается на витрине у пользователей МоегоСклада.
- **Готово, отправлено на модерацию (Ready)** — статус готовности. Приложение готово к публикации со стороны разработчика. Сотрудники МоегоСклада проверят приложение перед публикацией. Приложение не отображается на витрине у пользователей МоегоСклада.
- **Опубликовано (Published)** — приложение опубликовано на витрине приложений и доступно к установке пользователями МоегоСклада.
- **Снято с публикации (Hidden)** — публикация приложения приостановлена. Приложение исчезает с витрины, но у текущих пользователей приложения сохраняется возможность работать с ним. 

Жизненный цикл приложения :

1. Приложение создается в [личном кабинете разработчика](#lichnyj-kabinet-wendora) со статусом **Draft**. Разработчик проверяет и отлаживает работу приложения на своем аккаунте. Когда приложение готово, разработчик передает его на публикацию. Статус приложения меняется на **Ready**.
2. Сотрудник МоегоСклада проверяет, затем публикует приложение на витрине. Статус приложения меняется на **Published**. Приложение становится доступно пользователю МоегоСклада для установки.
3. Пользователь МоегоСклада устанавливает (подключает) приложение на свой аккаунт, настраивает и использует. Если приложение не нужно, пользователь может удалить (отключить) приложение на аккаунте. 
4. Чтобы убрать приложение с витрины приложений, его нужно перевести в статус **Hidden**. Установленные до этого момента экземпляры приложения на аккаунтах пользователей продолжают работать и отображаться на UI МоегоСклада, пока пользователи их не удалят. Для аккаунтов, удаливших приложение, и аккаунтов, на которых оно не было установлено, приложение скрывается. Установка приложения становится невозможной. Так можно скрыть только бесплатные приложения.

#### Создание черновика приложения

1. В личном кабинете разработчика нажмите на кнопку **Создать приложение**. Откроется форма создания черновика приложения. 
2. Укажите **Псевдоним приложения**. Псевдоним — уникальный идентификатор. Невозможно создать два приложения с одинаковыми псевдонимами. 
3. Создайте приложение подходящего типа: Серверное приложение, Телефония, Приложение лояльности. Тип приложения влияет на его платность, наличие/отсутствие Пробного периода, особенности заполнения [Дескриптора](#deskriptor-prilozheniq):  
- **Серверное приложение**: 
  - При создании Серверного приложения выберите, будет  приложение [платным](#uslowiq-oplaty-prilozhenij) или бесплатным. Для выбора используйте чекбокс **Платное**.
  - Если приложение платное, укажите его стоимость в рублях.<br>Если приложение платное, для него можно установить [Пробный период](#probnyj-period-platnyh-prilozhenij). Для этого после того, как уставновили отметку в чекбоксе **Платное**, укажите длительность Пробного периода. Максимальная длительность — 14 дней. Пробный период можно не назначать. 
  - Дескриптор приложения обязателен для заполнения. Правила заполнения дескриптора смотрите в разделе [Дескриптор приложения](#deskriptor-prilozheniq).

- **Телефония**. При создании приложения с типом Телефония нельзя сделать его платным, нельзя выбрать Пробный период, не нужно заполнять Дескриптор. Телефония оплачивается пользователем отдельно через опцию CRM.
- **Приложение лояльности**. При создании Приложения лояльности нельзя делать его платным, нельзя выбрать Пробный период, не нужно заполнять Дескриптор.

#### Редактирование черновика приложения

Если после создания приложения его настройки нужно изменить, выберите приложение в списке приложений и нажмите на кнопку **Редактировать приложение**.

Особенности редактирования приложений:

- Редактировать можно только приложения в статусе **Черновик**. После того, как приложение отправлено на модерацию, его нельзя редактировать. Можно просматривать данные приложения, нажав на кнопку **Редактировать приложение**. Редактирование становится доступным снова, если модератор возвращает приложение на доработку. Если после публикации приложения необходимо внести изменения, обратитесь к модератору.
- В форме редактирования доступны те же поля, что и в форме создания черновика приложения. Подробнее смотрите предыдущий пункт **Создание черновика приложений**.
- Доступны просмотр и перегенерация [Секретного ключа](#sekretnyj-kluch-secretkey). Для просмотра нажмите на кнопку «глаз» у скрытого точками поля, для генерации нового ключа — кнопку **Сгенерировать**. Кнопка **Сгенерировать** доступна только для приложений в статусе **Черновик**.
- В форме редактирования отображаются поля, доступные только для чтения («Read-Only»), с техническими параметрами и статусом публикации приложения.

#### Отправка на модерацию 

Перед публикацией на витрине МоегоСклада новое приложение должно пройти модерацию.

Чтобы отправить приложение на модерацию, выберите нужное приложение в статусе **Черновик** из списка и нажмите на кнопку **Отправить на модерацию**.

Обязательно заполните поле **Электронная почта для уведомлений** в разделе [Реквизиты / Информация о разработчике](https://lk.moysklad.ru/vendor/vendordetails). Это позволяет получать оповещения и следить за процессом прохождения модерации.

#### Ручная приостановка приложения 
 
В личном кабинете разработчик может тестировать и отлаживать приложение при приостановке и возобновлении на аккаунте.

Чтобы протестировать приложение при приостановке:

1. Привяжите аккаунт в МоемСкладе к аккаунту разработчика в личном кабинете разработчика (создайте аккаунт разработчика).
2. Заведите платное приложение в личном кабинете разработчика.
3. Установите приложение на аккаунте разработчика.
4. Выберите приложение в списке и нажмите на кнопку **Приостановить на аккаунте**. Работа приложения будет приостановлена.
5. Чтобы отладить приложение при возобновлении работы, нажмите на кнопку **Активировать** в карточке приложения на витрине МоегоСклада.

Приостановка возможна только для приложений, которые уже установлены или устанавливаются. 

#### Продление пробного периода платного приложения

В личном кабинете разработчика можно [продлить пробный период](#prodlenie-probnogo-perioda) приложения. Продление на выбранном аккаунте пользователя доступно один раз и только для платных опубликованных приложений. Для этого:

1. В Списке приложений выберите платное опубликованное приложение.
1. Нажмите на кнопку **Предоставить пробный период**.
1. В окне **Предоставление пробного периода** заполните поля **Аккаунт** и **Количество дней**. 
1. Если поля заполнены корректно, откроется окно **Подтверждение пробного периода**. 
1. Проверьте указанный пробный период и нажмите на кнопку **Да, предоставить**. 

### Редактирование информации о разработчике

Чтобы отредактировать информацию о разработчике приложения, в меню личного кабинета перейдите на вкладку [Реквизиты / Информация о разработчике](https://lk.moysklad.ru/vendor/vendordetails).

Функция доступна, пока на аккаунте отсутствуют приложения или есть только Черновики. В остальных случаях данные доступны 
только для просмотра, для изменения обратитесь к модератору МоегоСклада.

Также можно внести или отредактировать реквизиты для выплат денежных средств за платные приложения. Для этого в меню перейдите на вкладку [Реквизиты / Реквизиты компании](https://lk.moysklad.ru/vendor/bankdetails).

### Привязка аккаунта к разработчику

Отладить приложение для магазина приложений можно на аккаунте разработчика. Чтобы сделать аккаунт в МоемСкладе аккаунтом разработчика, свяжите аккаунт с нужным разработчиком. Для этого в личном кабинете разработчика, в верхнем меню нажмите на кнопку **Привязать**.

**Важно:** Для привязки необходим доступ к электронной почте сотрудника, указанного в аккаунте МоегоСклада на странице 
Подписка. По умолчанию это администратор, зарегистрировавший аккаунт. Однако далее вместо администратора можно указать другого сотрудника.

Чтобы изменить уже существующую привязку, нажмите на имя текущей привязки. Предыдущая привязка будет удалена, установленные на отвязанном аккаунте приложения в статусах **Черновик (Draft)** и **Готово, отправлено на модерацию (Ready)** будут деинсталлированы.

### Отладка приложений на аккаунтах разработчика

Отладить неопубликованное приложение можно в аккаунте разработчика. Неопубликованные приложения разработчика находятся на витрине приложений в блоке **Приложения в разработке**. Неопубликованные приложения видит только разработчик, для пользователей они не видны. 

Неопубликованные приложения можно подключать и отключать так же, как и обычные опубликованные приложения. 

### Отчеты в личном кабинете разработчика

#### Сводный отчет по установкам приложений

В данном отчете можно посмотреть сколько активных установок есть у приложений, сколько из них пробных и оплачиваемых. Также можно посмотреть сколько приостановленных установок.

Для просмотра отчета по установкам необходимо перейти в раздел **Отчеты** в верхнем меню и выбрать вкладку **Установки**.

В отчет включаются:

 - Все приложения независимо от платности и наличия установок
 - В статусе **Опубликовано** и **Снято с публикации**.

#### Отчет по выручке платных приложений

Отчет предоставляет информацию о том, сколько приложение заработало денежных средств. Учитываются только реально оплачиваемые установки. Установки приложений на Пробном тарифе и с Пробным периодом не учитываются.

Для просмотра отчета по выручке необходимо в разделе **Отчеты** верхнего меню выбрать вкладку **Выручка**.

В отчет включаются:

  - Приложения во всех [статусах](#zhiznennyj-cikl-prilozheniq). 
  - Платные приложения, у которых есть хотя бы одна успешная установка.
  - Бесплатные приложения, если ранее они были платными и имели успешные установки.

#### Отчет об использовании приложений

Отчет об использовании приложений является основанием для выплаты разработчику денежных средств за использование приложения пользователями МоегоСклада. Отчет содержит информацию о том, сколько денег заработало каждое приложение в отдельности и все приложения разработчика вместе за месяц.

Для просмотра и согласования отчета в разделе **Отчеты** верхнего меню выберите вкладку **Выплаты**.

Отчет формируется раз в месяц, доступен для скачивания в формате PDF. Процесс работы с отчетом:

1. Чтобы отчет сформировался, заполните реквизиты.
2. Отчет поступает в статусе **Сформировано**. На почту приходит оповещение.
3. Просмотрите и согласуйте отчет (кнопка **Согласовать**). Статус отчета меняется на **Согласовано**.
4. Вознаграждение разработчика выплачивается согласно банковским реквизитам. В отчете появляется отметка **Выплачено**.

Если по отчету есть вопросы или возражения, не согласовывайте его и обратитесь к сотруднику МоегоСклада.

#### Отчет по причинам удаления приложений

При удалении приложения на витрине МоегоСклада пользователю предлагается оставить отзыв о приложении:

![useful image](removal-feedback.png)

Если пользователь указывает одну и более причин удаления и нажимает на кнопку **Отправить отзыв**, разработчик получает этот отзыв. На email разработчика, указанный на вкладке [Разработчик](#redaktirowanie-informacii-o-wendore), приходит сообщение с причинами удаления.

Список всех отзывов пользователей отображается в отчете **Причины удаления приложений**. Чтобы просмотреть его, в разделе **Отчеты** верхнего меню выберите вкладку **Причины удаления**.

Чтоба настроить отправку писем, отметьте флагом "Отправлять уведомления о причинах удаления приложений на email". Если функция отключена, отзывы продолжают собираться в данный отчет.

**Ограничение:** В отчете выводятся только 1000 последних отзывов за выбранный период.

### Права доступа для приложений

Чтобы серверное приложение получило доступ к JSON API, в дескрипторе приложения нужно указать желаемый уровень доступа к JSON API. Можно запросить следующие уровни доступа:

* **admin** — соответствует пользовательской роли `Системный администратор`. Приложение получает полный доступ ко всем отчетам, сущностям и документам в МоемСкладе. Уровень в перспективе будет устранен.

* **custom** — соответствует пользовательской роли `Индивидуальная роль`. Приложение получает доступ только к указанным в дескрипторе отчетам, сущностям и документам. Уровень рекомендуется для использования всеми приложениями кроме тех, которые работают с вебхуками и задачами.
 
Права приложения на аккаунте фиксируются на момент установки приложения. При последующем обновлении дескриптора приложения права приложения на аккаунте сохраняются. 

При разработке приложений одновременно могут существовать и работать установки приложений с разными правами. Необходимо в том или ином виде поддерживать работу приложения с несколькими наборами прав. 

Предоставление приложению новых дополнительных прав должно происходить через явное согласие пользователя. Этот механизм будет реализован в будущем. Сейчас пользователь может обновить права через переустановку. Нужно следить, чтобы при удалении приложения данные аккаунта сохранялись некоторое время. 

Подробнее о ролях пользователей смотрите в [документации JSON API](https://dev.moysklad.ru/doc/api/remap/1.2/dictionaries/#sushhnosti-sotrudnik-rabota-s-pravami-sotrudnika).

Подробнее о правах доступа для приложений смотрите в разделе [Информация о правах доступа](#blok-access).

### Прямая ссылка на приложение

Разработчик может получить прямую ссылку на приложение. 

Для этого в [личном кабинете разработчика](#lichnyj-kabinet-wendora) перейдите в режим просмотра или редактирования приложения и скопируйте прямую ссылку на приложение. 

Также прямую ссылку можно получить в витрине приложений из адресной строки браузера, если открыть карточку приложения на витрине.

При переходе по короткой ссылке открывается витрина с карточкой приложения. Если пользователь авторизован, витрина с карточкой открывается сразу. Если нет, для просмотра необходимо авторизаваться.

Если приложение было удалено или недоступно по прямой ссылке, при переходе по ссылке открывается витрина и появляется сообщение о том, что приложение не найдено.
 
Если приложение снято с публикации, но уже установлено некоторыми пользователями, оно будет отображаться для этих пользователей по ссылке как на витрине. Для остальных пользователей приложение будет недоступно. Так как витрина приложений доступна только администраторам аккаунтов, карточка приложения будет доступна только им.
