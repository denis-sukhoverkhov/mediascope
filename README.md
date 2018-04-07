# How it use
1) Install dependencies
2) Install db `python3.6 install_db.py --path ./tmp/dbs.zip` where `./tmp/dbs.zip` is a path to archive with database.
3) Start unittests
```bash
python3.6 -m unittest
``` 
3) run the server `python3.6 app.py `
4) Test query `http://127.0.0.1:5000/logs?from=1.383253541E12&to=1.383334735E12&page=1&items=20`

# Task
Необходимо реализовать web-сервис на Python.

На входе есть архив с двумя файлами БД SQLite:
1. logs.db - содержит таблицу logs (date real, event text) с обезличенными логами событий с участием некоторых людей. Поле event содержит описание события, где имена и фамилии людей обезличены и заменены на идентификаторы вида <p=1>.
2. people.db - содержит таблицу people (id integer, first_name text, last_name text, gender text) со справочником людей.

Сервис должен реализовать вызов API.

`/logs` - возвращает логи в формате json.

Например,

`http:/localhost:8000/logs?from=1520414609803&to=1520414659803&page=1&items=20`

Где параметры фильтрации:

`from` и `to` - начало и конец периода выборки логов,

`page` - номер страницы в выборке,

`items` - количество элементов в выборке.

Соответственно, если нужно выбрать элементы с 20 по 40 элементов, то вид будет такой `page=2&items=20`.

Результатом этого вызова должны быть логи, обогащённые данными справочника, где идентификаторы заменены на имена в формате "Имя Фамилия".

Например,

```
[
        {
               "date": 1520414609803,
               "event": "Elen Farmer hug Peter Jenkins"
        },
        ...
        {
               ...
        }
]
```

Предполагается использование модулей Flask и SQLAlchemy. Также допускается использование любых модулей на свое усмотрение. 
Базы данных при необходимости допускается модифицировать.

На выходе - Python-проект, реализующий web api, а так же файл dependencies.txt с зависимостями проекта.