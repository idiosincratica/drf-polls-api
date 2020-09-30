# drf-polls-api
# Инструкция по разворачиванию приложения локально (Windows)
Установить *Python*.  
Создать виртуальное пространство.  
Установить *Django*, *Django REST framework* (можно из `requirements.txt` или с помощью *Poetry*).  
Запустить миграцию БД (приложение создавалось и тестировалось на *SQLite*).

    python manage.py migrate

Создать суперпользователя:

    python manage.py createsuperuser --username=<username> --email=<email>

Для администратора используется *token authentication*. Получить токен:

    python manage.py drf_create_token <username>
    
Или через API:

    POST: /token, body: {"username": <username>, "password": <password>}

Для авторизации админа в каждом запросе к API используется http хедер `Authorization`:

    Authorization: Token <token>

# Документация по API:
[/token](#token)  
[/user](#user)  
[/polls](#polls)  
[/active-polls](#active-polls)  
[/poll](#poll)  
[/poll/&lt;int id опроса&gt;](#pollint-id-опроса)  
[/question](#question)  
[/question/&lt;int id&gt;](#questionint-id)  
[/choice](#choice)  
[/choice/&lt;int id&gt;](#choiceint-id)  
[/text-response](#text-response)  
[/single-choice-response](#single-choice-response)  
[/multiple-choices-response](#multiple-choices-response)  
[/finished-polls?user=<int id пользователя>](#finished-pollsuserint-id-пользователя)  
[/unfinished-polls?user=<int id пользователя>](#unfinished-pollsuserint-id-пользователя)

Разрешения делятся на две группы: администраторы (*IsAdminUser*) (`user.is_staff = True`)
и анонимные пользователи (*AllowAny*)

## /token
### POST:
Возвращает токен для авторизации админа через http хедер: `Authorization: Token <token>`

*permissions*: **AllowAny**

#### request:

```
{"username": <username>, "password": <password>}
```

#### response:

```
{
    "token": <str токен>
}
```


## /user
### POST
Создает запись анонимного пользователя БД и возвращает его `id` для дальнейшего
использования при прохождении опросов и получении пройденных опросов с детализацией по ответам.

*permissions*: **AllowAny**

#### request:
Тело запроса отсутствует.  
#### response:

```
{
    "id": <int id>
}
```

## /polls
### GET
Cписок всех опросов.

*permissions*: **IsAdminUser**

#### response:

```
[
    {
        "id": <int id>,
        "name": <str название>,
        "description": <str описание>,
        "start": <str дата старта (гггг-мм-чч)>,
        "end": <str дата окончания (гггг-мм-чч)>
    },
    ...
]
```

## /active-polls
### GET
Список активных опросов.

*permissions*: **AllowAny**

#### response:
Аналогичный `/polls`

## /poll

### POST
Cоздание опроса. Дата старта должна быть в будущем, дата окончания должна быть больше даты старта.
С даты окончания опрос не активен. Изменение опроса с даты старта запрещено. Дата старта не может быть изменена.

*permissions*: **IsAdminUser**

#### request:

```
{
    "name": <str название>,
    "description": <str описание>,
    "start": <str дата старта (гггг-мм-чч)>,
    "end": <str дата окончания (гггг-мм-чч)>
}
```

## /poll/&lt;int id опроса&gt;
### GET
Возвращает объект опроса. Анонимным пользователям можно просматривать только активные опросы.

*permissions*: **AllowAny**

```
{
    "id": <int id>,    
    "name": <str название>,
    "description": <str описание>,
    "start": <str дата старта (гггг-мм-чч)>,
    "end": <str дата окончания (гггг-мм-чч)>,
    "questions": [<int id вопроса>, ...]
}
```

### PUT/PATCH

*permissions*: **IsAdminUser**

#### request:

```
{
    "name": <str название>,
    "description": <str описание>,
    "start": <str дата старта (гггг-мм-чч)>,
    "end": <str дата окончания (гггг-мм-чч)>
}
```

### DELETE

*permissions*: **IsAdminUser**

## /question

### POST
Создание вопроса. В одном опросе не могут быть вопросы с одинаковым текстом.
Добавить вопрос к опросу с даты старта нельзя.

*permissions*: **IsAdminUser**

#### request:

```
{
    "poll": <int id опроса>,
    "text": <str текст вопроса>,
    "type": <int тип вопроса>
}
```

**Типы вопросов**:  
1 - текстовый  
2 - с выбором одного варианта  
3 - с выбором нескольких вариантов  

## /question/&lt;int id&gt;

### GET
Получение вопроса. Анонимные пользователи могут просматривать только вопросы в активных опросах.
Если тип вопроса предполагает варианты ответа, то они включены в возвращаемый объект.

*permissions*: **AllowAny**

#### response:

```
{
    "id": <int id>,
    "poll": <int id опроса>,
    "text": <str текст вопроса>,
    "type": <int тип вопроса>,
    "choices": [
        {
            "id": <int id варианта>,
            "text": <str текст варианта>
        },
        ...
    ]
}
```

### PUT/PATCH
Изменение вопросов в опросе с даты старта нельзя.
Если тип меняется на текстовый то варианты принадлежащие ему удаляются.

*permissions*: **IsAdminUser**

#### request:

```
{
    "id": <int id>,
    "poll": <int id опроса>,
    "text": <str текст вопроса>,
    "type": <int тип вопроса>
}
```

### DELETE
Удалять вопросы с даты старта опроса нельзя.

*permissions*: **IsAdminUser**

## /choice
### POST
Создание варианта ответа для вопросов с типом `2` и `3`. Добавлять вопросы к опросу с даты старта нельзя.
Добавить вопросы с одинаковы текстом к одному вопросу нельзя.

*permissions*: **IsAdminUser**

#### request:

```
{
    "question": <int id вопроса>,
    "text": <str текст варианта>
}
```

## /choice/&lt;int id&gt;

### GET:

*permissions*: **IsAdminUser**

#### response:

```
{
    "id": <int id>,
    "question": <int id вопроса>,
    "text": <str текст варианта>
}
```

### PUT/PATCH

*permissions*: **IsAdminUser**

Измененять вариант у опроса с даты старта нельзя.

#### request:

```
{
    "question": <int id вопроса>,
    "text": <str текст варианта>
}
```

### DELETE
Удалять вариант у опроса с даты старта нельзя.

*permissions*: **IsAdminUser**

## Прохождение опроса:
В поле `user` вводится `id` анонимного пользователя который сгенерирован по адресу `/user`.
Проходить неактивные опросы нельзя.

## /text-response

### POST
Ввод ответа на вопрос с типом текст (тип `1`)

*permissions*: **AllowAny**

#### request:

```
{
    "user": <int id пользователя>,
    "question": <int id вопроса>,
    "text": <str текст ответа>
}
```

## /single-choice-response

### POST
Ввод ответа на вопрос с выбором одного варианта (тип `2`)

*permissions*: **AllowAny**

#### request:

```
{
    "user": <int id пользователя>,
    "choice": <int id варианта>
}
```

## /multiple-choices-response

### POST
Ввод ответа на вопрос с выбором нескольких вариантов (тип `3`). `choices` не может быть пустым списком.
Все варианты должны принадлежать одному вопросу. На один вопрос можно ответить только один раз.

*permissions*: **AllowAny**

#### request:

```
{
    "user": <int id пользователя>,
    "choices": [<int id варианта>, ...]
}
```

## Получение пройденных опросов:
Параметр запроса `user` - id анонимного пользователя который сгенерирован по адресу `/user`

## /finished-polls?user=<int id пользователя>

### GET
Получение полностью пройденных пользователем опросов с детализацией по ответам.

*permissions*: **AllowAny**

#### response:

```
[
    {
        "id": <int id>,
        "name": <str название>,
        "description": <str описание>,
        "start": <str дата старта (гггг-мм-чч)>,
        "end": <str дата окончания (гггг-мм-чч)>,
        "questions": [
            {
                "id": <int id вопроса>,
                "text": <str текст вопроса>,
                "type": 1,
                "response": <str текст ответа>
            },
            {
                "id": <int id вопроса>,
                "text": <str текст вопроса>,
                "type": 2,
                "response": <str текст выбранного варианта>
            },
            {
                "id": <int id вопроса>,
                "text": <str текст вопроса>,
                "type": 3,
                "response": [
                    <str текст выбранного варианта>,
                    ...
                ]
            },
            ...
        ]
    },
    ...
]
```

## /unfinished-polls?user=<int id пользователя>

### GET
Получение частично пройденных пользователем опросов с детализацией по ответам.

*permissions*: **AllowAny**

#### response:
Аналогичный `/finished-polls?user=<int id пользователя>`, но в поле `response` у вопросов без ответа значение `null`.
