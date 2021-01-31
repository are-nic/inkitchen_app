"""
Старая версия
Добавление тегов в БД
Для запуска скрипта - python manage.py ingredients
"""

import requests
from requests.auth import AuthBase
from django.core.management.base import BaseCommand
import time
from ...models import TagIngredient


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


def get_token():
    """
    Делает POST запрос для получения токена
    :return: токен
    """
    body = {"LoginForm": {"username": "repair-cat", "password": "records0"}}

    token_request = requests.post('https://api.kitchenhub.club/v1/staff/login', json=body)
    if token_request.status_code == 200:
        data = token_request.json()
        token = data["data"]["access_token"]
        print(token)
        return token


def get_ingredients():
    """
    Для получения Тэгов ингридиентов от kithenhub.club API
    :return:
    """
    max_retries = 5     # кол-во попыток запроса
    attempt_num = 0     # кол-во попыток запроса для отслеживания
    while attempt_num < max_retries:
        ingredients_tags = requests.get(
            'https://api.kitchenhub.club/v1/tags/public',
            auth=BearerAuth(get_token()),
            timeout=10
        )

        if ingredients_tags.status_code == 200:
            data = ingredients_tags.json()
            return data['data']['rows']
        else:
            attempt_num += 1
            time.sleep(2)  # ждать 2 сек перед повторным запросом
    print('Запрос для ингридиентов не выполнен')
    return


def seed_ingredients():
    """
    Наполняем нашу БД тегами ингридиентов
    """
    for ingredient in get_ingredients():
        tag_ingredient = TagIngredient(
            id=ingredient['id'],
            name=ingredient['name']
        )
        tag_ingredient.save()


def clear_data():
    TagIngredient.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        seed_ingredients()
        print("complete")