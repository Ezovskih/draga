from django.urls import path

from security.views import SendCodeView


urlpatterns = [
    path('send_code', SendCodeView.as_view(), name='send_code'),
]
