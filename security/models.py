from django.db import models


class VerifyCode(models.Model):
    address = models.CharField(max_length=255)
    transport_type = models.CharField(max_length=10)
    who_called = models.IntegerField()
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # TODO PyCharm Professional

    def __str__(self):
        return f"Код {self.code} из приложения {self.who_called} отправлен как {self.transport_type} на {self.address}"
