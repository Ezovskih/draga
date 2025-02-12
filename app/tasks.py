import requests
from django_rq import job

from app import settings


@job
def send_code_task(address, code):
    try:
        response = requests.post(
            settings.API_ADDRESS_URL,
            json={
                'user': settings.API_USER_NAME,
                'pass': settings.API_PASS_WORD,
                'target': address,
                'message': f"Ваш проверочный код: {code}"
            }
        )

        if response.status_code != 200:
            raise Exception(f"На запрос к {settings.API_ADDRESS_URL} получен код ответа {response.status_code}!")
    except:
        raise  # TODO реализовать логирование ошибок
