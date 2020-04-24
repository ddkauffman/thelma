import os
import requests
from django.conf import settings

from celery.decorators import task
# from celery.decorators import shared_task

from .celery import app


@task
def get_new_token():

    API_URL = f'{settings.HTTP_PROTOCOL}://{settings.TELEMETRY_API_HOST}{settings.TELEMETRY_API_PORT}/api/token/'

    API_TOKENS = requests.post(API_URL, json={
            'username': settings.API_USER,
            'password': settings.API_PASSWORD
        }
    ).json()

    os.environ['API_ACCESS_TOKEN'] = API_TOKENS['access']
    # os.environ['API_REFRESH_TOKEN'] = API_TOKENS['refresh']
    print('New Access Token Set')


if __name__ == '__main__':
    get_new_token()
