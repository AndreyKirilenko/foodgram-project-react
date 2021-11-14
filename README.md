# in develop
о проекте
    название (желательно и его изображение тоже. Отредактировать можно на canva.com, если вы не специалист по графическому дизайну);
    описание (с использованием слов и изображений);
    демо (изображения, ссылки на видео, интерактивные демо-ссылки);
    технологии в проекте;
    что-то характерное для проекта (проблемы, с которыми пришлось столкнуться, уникальные составляющие проекта);
    техническое описание проекта (установка, настройка, как помочь проекту).
запуск
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py loaddata fixtures/base_dump.json --app foodgram.ingredients

Технологии

кнопка работы