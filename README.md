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
[/active_polls](#active_polls)  
[/poll](#poll)  
[/poll/&lt;int id опроса&gt;](#pollint-id-опроса)  
[/question](#question)  
[/question/&lt;int id&gt;](#questionint-id)  
[/choice](#choice)  
[/choice/&lt;int id&gt;](#choiceint-id)  
[/text_response](#text_response)  
[/single_choice_response](#single_choice_response)  
[/multiple_choices_response](#multiple_choices_response)  
[/finished_polls?user=<int id пользователя>](#finished_pollsuserint-id-пользователя)  
[/unfinished_polls?user=<int id пользователя>](#unfinished_pollsuserint-id-пользователя)

Разрешения делятся на две группы: администраторы (*IsAdminUser*) (`user.is_staff = True`) и анонимные пользователи (*AllowAny*)

## /token
### POST:
Возвращает токен для авторизации админа через http хедер: `Authorization: Token <token>`  
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
Создает запись анонимного пользователя в базе и возвращает его `id` для дальнейшего использования при прохождении опроса и получении пройденных опросов с детализацией по ответам.  
#### request:
Тело запроса отсутствует.  
#### response:

```
{
    "id": <int id>
}
```

## /polls
*permissions*: **IsAdminUser**
### GET
Cписок всех опросов.  
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

## /active_polls
### GET
Список активных опросов.  
#### response:
Аналогичный `/polls`

## /poll
*permissions*: **IsAdminUser**
### POST
Cоздание опроса. Дата старта должна быть не в прошлом, дата окончания должна быть в будущем. С даты окончания опрос не активен. Изменение опроса после старта запрещено. Дата старта не может быть изменена.  
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
Возвращает объект опроса.

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
см. POST

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
Создание вопроса. В одном опросе не могут быть вопросы с одинаковым текстом. Добавить вопрос к опросу с даты старта нельзя.  
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
Получение вопроса. Анонимные пользователи могут просматривать только вопросы в активных опросах. Если тип вопроса предполагает варианты ответа, то они включены в возвращаемый объект.

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
Изменение вопросов в опросе с даты старта нельзя. Если тип меняется на текстовый то варианты принадлежащие ему удаляются.

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
Создание варианта ответа для вопросов с типом `2` и `3`. Добавлять вопросы к опросу с даты старта нельзя. Добавить вопросы с одинаковы текстом к одному вопросу нельзя.

*permissions*: **IsAdminUser**  
#### request:

```
{
    "question": <int id вопроса>,
    "text": <str текст варианта>
}
```

## /choice/&lt;int id&gt;  
*permissions*: **IsAdminUser**

### GET:
#### response:

```
{
    "id": <int id>,
    "question": <int id вопроса>,
    "text": <str текст варианта>
}
```

### PUT/PATCH
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

## Прохождение опроса:
В поле `user` вводится `id` анонимного пользователя который сгенерирован по адресу `/user`. Проходить неактивные опросы нельзя.

## /text_response
### POST
Ввод ответа на вопрос с типом текст (тип `1`)  
#### request:

```
{
    "user": <int id пользователя>,
    "question": <int id вопроса>,
    "text": <str текст ответа>
}
```

## /single_choice_response
### POST
Ввод ответа на вопрос с выбором одного варианта (тип `2`)  
#### request:

```
{
    "user": <int id пользователя>,
    "choice": <int id варианта>
}
```

## /multiple_choices_response
### POST
Ввод ответа на вопрос с выбором нескольких вариантов (тип `3`). `choices` не может быть пустым списком. Все варианты должны принадлежать одному вопросу.  
#### request:

```
{
    "user": <int id пользователя>,
    "choices": [<int id варианта>, ...]
}
```

## Получение пройденных опросов:
Параметр запроса `user` - id анонимного пользователя который сгенерирован по адресу `/user`

## /finished_polls?user=<int id пользователя>
### GET
Получение полностью пройденных пользователем опросов с детализацией по ответам.  
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

## /unfinished_polls?user=<int id пользователя>
### GET
Получение частично пройденных пользователем опросов с детализацией по ответам.
#### response:
Аналогичный `/finished_polls?user=<int id пользователя>`, но в поле `response` у вопросов без ответа значение `null`.
