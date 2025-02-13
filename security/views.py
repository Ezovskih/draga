import json
from http import HTTPStatus
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from app.forms import RequestCodeForm
from app.tasks import send_code_task

from security.models import VerifyCode


def get_code(minimum = 1000, maximum = 9999) -> str:
    """Генерация (строки) числового кода"""
    from secrets import choice
    return str(choice(range(minimum, maximum + 1)))


class SendCodeView(View):

    def get(self, request):
        form = RequestCodeForm()  # создаем пустую форму
        return render(request, 'request_code_form.html', {'form': form})


    def post(self, request):
        try:
            data = json.loads(request.body)
            address = data['address']
            transport_type = data['transport_type']
            who_called = data['who_called']
        except KeyError:
            return JsonResponse({'error': "Некорректные параметры запроса!"}, status=HTTPStatus.BAD_REQUEST)  # 400

        code = get_code()  # генерируем проверочный код

        # Отправляем код выбранным способом
        if transport_type == 'sms':
            job = send_code_task.delay(address, code)  # ставим в очередь задачу
            print("CREATED JOB ID: ", job.id)
        elif transport_type == 'email':
            pass  # TODO реализовать отправку e-mail
        else:
            return JsonResponse({'error': "Некорректный тип транспорта!"}, status=HTTPStatus.BAD_REQUEST)

        # Сохраняем код в базу данных
        VerifyCode.objects.create(
            address=address,
            transport_type=transport_type,
            who_called=who_called,
            code=code
        )

        return JsonResponse({'code': code}, status=HTTPStatus.ACCEPTED)  # 202
