import json
import requests
from django.http import JsonResponse
from django.views import View

from app import settings
from security.models import VerifyCode


def get_code(minimum = 1000, maximum = 9999) -> str:
    """Генерация (строки) числового кода"""
    from random import randint
    return str(randint(minimum, maximum))


class SendCodeView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            address = data['address']
            transport_type = data['transport_type']
            who_called = data['who_called']
        except KeyError:
            return JsonResponse({'error': "Некорректные параметры запроса!"}, status=400)

        code = get_code()  # генерируем проверочный код

        # Отправка кода на сторонний API
        if transport_type == 'sms':
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
            except json.JSONDecodeError:
                return JsonResponse({'error': "Некорректный JSON!"}, status=400)

            if response.status_code != 200:
                return JsonResponse({'error': "Ошибка отправки СМС-сообщения!"}, status=500)
        elif transport_type == 'email':
            pass  # TODO реализовать отправку e-mail
        else:
            return JsonResponse({'error': "Некорректный тип транспорта!"}, status=400)

        # Сохраняем код в базу данных
        VerifyCode.objects.create(
            address=address,
            transport_type=transport_type,
            who_called=who_called,
            code=code
        )

        return JsonResponse({'code': code})
