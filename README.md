# DRF_CRUD_test_task
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://docs.djangoproject.com/en/4.2/)
[![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-v3.14-green)](https://www.django-rest-framework.org/)

API для CRUD операций на базе Django REST Framework.

## Задача
Требуется разработать простое API приложения на Django REST Framework,
для работы с которым используются API endpoints по принципу CRUD.

Допустим это будет личный блог, с одной моделью у которой есть поля:
- пользователь,
- имя записи,
- текст,
- дата создания,
- опубликована ли запись.

Важно: не использовать ModelViewSet и viewsets,  допускается использование generics APIView, но в приоритете базовое APIView.

Желательно, но не обязательно:
- Предусмотреть права, чтобы только пользователь или администратор мог удалять или изменять запись.
- Написать тесты для разработанного API.
- Добавить OpenAPI описание с помощью drf-spectacular.

## Стек проекта
* Python 3.10
* Django 4.2
* Django REST Framework 3.14
* SQLite
* drf-spectacular
* pytest

## Запуск проекта в dev-режиме

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/dmitrii-r/DRF_CRUD_test_task.git
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Перейти в каталог приложения:
```
cd simple_crud_api
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```

### Документация API
Документация API доступна после запуска проекта по адресам:
- schema
```
http://127.0.0.1:8000/api/schema/
```
- redoc
```
http://127.0.0.1:8000/api/schema/redoc/
```
- swagger
```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

### Запуск автоматического тестирования
Ввести команду для запуска тестирования основанного на Pytest:
```
pytest
```
