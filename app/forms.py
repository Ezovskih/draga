from django import forms


class RequestCodeForm(forms.Form):
    address = forms.CharField(label="Номер телефона или эл. почта", max_length=100)
    transport_type = forms.ChoiceField(
        label="Тип транспорта",
        choices=[('sms', 'SMS'), ('email', 'E-mail')],
        initial='sms', disabled=True,
    )
    who_called = forms.ChoiceField(
        label="Тип клиентского приложения",
        choices=[(1, 'Приложение 1'), (2, 'Приложение 2'), (3, 'Приложение 3')],
        initial=1, disabled=True,
    )
