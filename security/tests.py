from django.test import TestCase, Client
from django.urls import reverse

from unittest.mock import patch

from security.models import VerifyCode


class SendCodeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('send_code')

    @patch('security.views.requests.post')
    def test_send_sms_code_success(self, mock_post):
        # Настройка мок-ответа
        mock_post.return_value.status_code = 200

        data = {
            'address': '1234567890',
            'transport_type': 'sms',
            'who_called': 1,
        }
        response = self.client.post(self.url, data, content_type='application/json')

        # Проверка ответа
        self.assertEqual(response.status_code, 200)
        self.assertIn('code', response.json())

        # Проверка сохранения в базе данных
        self.assertEqual(VerifyCode.objects.count(), 1)
        code_entry = VerifyCode.objects.first()
        self.assertEqual(code_entry.address, '1234567890')
        self.assertEqual(code_entry.transport_type, 'sms')
        self.assertEqual(code_entry.who_called, 1)

    def test_send_email_code_success(self):
        # TODO реализовать тест для отправки e-mail
        print("Тест для отправки e-mail не реализован!")

    def test_send_code_invalid_transport_type(self):
        data = {
            'address': '1234567890',
            'transport_type': 'invalid_type',
            'who_called': 1,
        }
        response = self.client.post(self.url, data, content_type='application/json')

        # Проверка ответа
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_send_code_missing_field(self):
        data = {
            'address': '1234567890',
            'transport_type': 'sms',
            # 'who_called' пропущен
        }
        response = self.client.post(self.url, data, content_type='application/json')

        # Проверка ответа
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
