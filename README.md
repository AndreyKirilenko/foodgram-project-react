# Продуктовый помощник. (In develop)
## Описание
Приложение позволяющее просматривать и создавать, рецепты, редактировать, добавлять их в избранное и свою  продуктовую корзину.
Так же доступна подписка на авторов понравившихся рецептов
После добавления в корзину доступно скачивание файла со списком ингредиентов.

Картинка

* Демо 
Демо версию можно посмотреть <a href ='http://51.250.27.63/recipes'>здесь</a>


## Локальная установка. 
Для установки: 
* скачайте проект к себе на компьютер 
```bash
    git clone <url repo>
```
* Установите Docker 
```https://www.docker.com/get-started```
* установите виртуальное окружение
```bash
    py -m venv venv
```
* Активируйте виртуальное окружение
```bash
    source venv/Scripts/activate
```
* создайте в ```/backend``` файл ```.env``` с переменными окружения
```python
    DB_NAME=<db_name> # имя базы данных
    POSTGRES_USER=<db_login> # логин для подключения к базе данных
    POSTGRES_PASSWORD=<db_password> # пароль для подключения к БД
    DB_HOST=<db> # название сервиса
    DB_PORT=<5432> # порт для подключения к БД
    SECRET_KEY=<l!2ej4o@bh947h+ac&3okup!ms-zq9#5&7ahlu0p+i!0*w!2ql>
    DJANGO_DEBUG=<True>
    ALLOWED_HOSTS=<localhost 127.0.0.1 web>

```
Перейдите в папку ```/infra``` и выполните следующие комманды

* Выполните сборку образов и запуск контейнеров
```bash
    docker-compose up -d --build
```
* Выполните миграции
```bash
    docker-compose exec web python manage.py migrate --noinput
```
* Создайте пользователя
```bash
    docker-compose exec web python manage.py createsuperuser
```
* Соберите статику
```bash
    docker-compose exec web python manage.py collectstatic
```
* Импортируйте дамп в базу данных
```bash
    docker-compose exec web python manage.py loaddata fixtures/base_dump.json
```

## Технологии
Python, Django, DRF, Docker, Git

## Автор
Кириленко Андрей

Развернутый на сервере проект можно посмотреть <a href='http://84.201.179.146/api/v1/'>здесь</a>
![example workflow](https://github.com/Akirosan/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)